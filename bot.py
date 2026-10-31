#!/usr/bin/env python3
"""
Safety — a cracked workplace-safety advisor Telegram bot for WA industrial & mining workers.

Design:
  * Telegram front-end (python-telegram-bot v21, async long-polling).
  * OpenAI-compatible LLM layer with an ORDERED list of models per role (text / vision):
    local first, cloud fallback. Health-checked with sticky back-off so a churning local
    model never adds latency to every message; it re-probes periodically.
  * Hindsight long-term memory (REST): a dedicated bank stores each user's profile and
    the conversation; per-message semantic recall injects prior context.
  * A citable knowledge corpus (markdown standards/regulations) retrieved with BM25 and
    injected into the prompt. The system prompt enforces citation discipline: cite the
    exact instrument + clause, and append "(unable to recall reference, not verified)"
    when no reference supports the answer.

Everything is env-driven; secrets live in a mode-600 env file, never in code.
"""

import asyncio
import base64
import json
import logging
import os
import re
import time
from pathlib import Path

import httpx
from rank_bm25 import BM25Okapi
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
log = logging.getLogger("safety")

# --------------------------------------------------------------------------- #
# Config
# --------------------------------------------------------------------------- #
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

HINDSIGHT_BANK_URL = os.environ.get(
    "HINDSIGHT_BANK_URL", "http://127.0.0.1:8897/v1/default/banks/safety"
)
KNOWLEDGE_DIR = os.environ.get("KNOWLEDGE_DIR", "/app/knowledge")
DATA_DIR = os.environ.get("DATA_DIR", "/app/data")
SYSTEM_PROMPT_PATH = os.environ.get("SYSTEM_PROMPT_PATH", "/app/system_prompt.txt")

# Text model chain (first healthy wins).
LOCAL_TEXT_URL = os.environ.get("LOCAL_TEXT_URL", "http://127.0.0.1:8141/v1")
LOCAL_TEXT_MODEL = os.environ.get("LOCAL_TEXT_MODEL", "muse-glimmer-30b")
LOCAL_TEXT_KEY = os.environ.get("LOCAL_TEXT_KEY", "")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
DEEPSEEK_URL = os.environ.get("DEEPSEEK_URL", "https://api.deepseek.com/v1")

# Vision model chain (first healthy wins).
LOCAL_VISION_URL = os.environ.get("LOCAL_VISION_URL", "http://127.0.0.1:8109/v1")
LOCAL_VISION_MODEL = os.environ.get("LOCAL_VISION_MODEL", "qwen3.8-27b-uncensored")
LOCAL_VISION_KEY = os.environ.get("LOCAL_VISION_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_VISION_MODEL = os.environ.get("OPENAI_VISION_MODEL", "gpt-4o")
OPENAI_URL = os.environ.get("OPENAI_URL", "https://api.openai.com/v1")

TEXT_CHAIN = [
    {"name": LOCAL_TEXT_MODEL, "base_url": LOCAL_TEXT_URL, "key": LOCAL_TEXT_KEY},
    {"name": DEEPSEEK_MODEL, "base_url": DEEPSEEK_URL, "key": DEEPSEEK_API_KEY},
]
VISION_CHAIN = [
    {"name": LOCAL_VISION_MODEL, "base_url": LOCAL_VISION_URL, "key": LOCAL_VISION_KEY},
    {"name": OPENAI_VISION_MODEL, "base_url": OPENAI_URL, "key": OPENAI_API_KEY},
]

# Tuneables.
TEXT_TIMEOUT_S = int(os.environ.get("TEXT_TIMEOUT_S", "180"))
VISION_TIMEOUT_S = int(os.environ.get("VISION_TIMEOUT_S", "180"))
TEXT_MAX_TOKENS = int(os.environ.get("TEXT_MAX_TOKENS", "1800"))
VISION_MAX_TOKENS = int(os.environ.get("VISION_MAX_TOKENS", "1400"))
BACKOFF_S = int(os.environ.get("BACKOFF_S", "300"))  # sticky back-off for a failed model
RETRIEVE_TOP_K = int(os.environ.get("RETRIEVE_TOP_K", "6"))
RECALL_TIMEOUT_S = int(os.environ.get("RECALL_TIMEOUT_S", "12"))

# --------------------------------------------------------------------------- #
# Model layer (OpenAI-compatible chat/completions with failover)
# --------------------------------------------------------------------------- #
_health = {m["name"]: {"ok": True, "until": 0.0} for m in TEXT_CHAIN + VISION_CHAIN}


def _clean_response(content: str) -> str:
    """Extract the final user-facing answer from a model that emits agentic /
    reasoning markers inline in ``content`` (e.g. 'to=self' … 'to=user')."""
    if not content:
        return ""
    for marker in ("Follow.assistant to=user", "to=user"):
        idx = content.rfind(marker)
        if idx != -1:
            tail = content[idx + len(marker):].lstrip(": \t\n")
            if tail:
                return tail.strip()
    return content.strip()


def _model_available(model: dict) -> bool:
    if not model["key"]:
        return False
    st = _health[model["name"]]
    if not st["ok"] and time.time() < st["until"]:
        return False
    return True


async def _chat_once(client: httpx.AsyncClient, model: dict, messages, max_tokens, timeout):
    url = model["base_url"].rstrip("/") + "/chat/completions"
    payload = {
        "model": model["name"],
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.4,
    }
    r = await client.post(
        url,
        json=payload,
        headers={"Authorization": f"Bearer {model['key']}"},
        timeout=timeout,
    )
    r.raise_for_status()
    data = r.json()
    choice = data["choices"][0]["message"]
    content = choice.get("content")
    if not content and choice.get("reasoning_content"):
        content = choice.get("reasoning_content")  # thinking-model fallback
    return _clean_response(content or ""), model["name"]


async def generate(messages, chain, max_tokens, timeout) -> tuple[str, str]:
    """Return (text, model_name) from the first healthy model in `chain`."""
    last_err = "no models configured"
    async with httpx.AsyncClient() as client:
        for model in chain:
            if not _model_available(model):
                continue
            try:
                text, name = await _chat_once(client, model, messages, max_tokens, timeout)
                _health[model["name"]] = {"ok": True, "until": 0.0}
                return text, name
            except Exception as exc:
                last_err = f"{model['name']}: {type(exc).__name__}: {exc}"
                _health[model["name"]] = {"ok": False, "until": time.time() + BACKOFF_S}
                log.warning("model failed, backing off: %s", last_err)
    raise RuntimeError(last_err)


def model_status() -> str:
    lines = []
    for m in TEXT_CHAIN + VISION_CHAIN:
        st = _health[m["name"]]
        state = "ready" if st["ok"] else f"backed-off until {int(st['until'] - time.time())}s"
        lines.append(f"  {m['name']}: {state}")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Knowledge corpus (BM25 retrieval over markdown standards/regulations)
# --------------------------------------------------------------------------- #
_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


class KnowledgeBase:
    def __init__(self, directory: str):
        self.directory = directory
        self.chunks: list[dict] = []
        self.bm25 = None
        self.loaded_at = 0.0
        self.reload()

    def reload(self):
        chunks = []
        for path in sorted(Path(self.directory).glob("*.md")):
            try:
                text = path.read_text(encoding="utf-8")
            except Exception as exc:
                log.warning("could not read %s: %s", path, exc)
                continue
            source = path.stem.replace("_", " ")
            for section in re.split(r"\n(?=#{1,4}\s)", text):
                section = section.strip()
                if not section:
                    continue
                for piece in self._chunk(section, 1800):
                    chunks.append({"source": source, "text": piece})
        self.chunks = chunks
        self.bm25 = BM25Okapi([_tokenize(c["text"]) for c in chunks]) if chunks else None
        self.loaded_at = time.time()
        log.info("knowledge base loaded: %d chunks from %s", len(chunks), self.directory)

    @staticmethod
    def _chunk(text: str, max_chars: int) -> list[str]:
        if len(text) <= max_chars:
            return [text]
        paras = re.split(r"\n\s*\n", text)
        out, cur = [], ""
        for p in paras:
            if len(cur) + len(p) + 1 > max_chars and cur:
                out.append(cur.strip())
                cur = p
            else:
                cur = f"{cur}\n\n{p}" if cur else p
        if cur.strip():
            out.append(cur.strip())
        return out

    def retrieve(self, query: str, top_k: int = RETRIEVE_TOP_K) -> list[dict]:
        if not self.bm25:
            return []
        scores = self.bm25.get_scores(_tokenize(query))
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        return [self.chunks[i] for i in ranked[:top_k] if scores[i] > 0]


KB = KnowledgeBase(KNOWLEDGE_DIR)


def build_reference_block(query: str) -> str:
    hits = KB.retrieve(query)
    if not hits:
        return ""
    lines = [
        "REFERENCE MATERIAL (retrieved from the safety standards/regulations corpus). "
        "Cite these precisely — instrument name, year, clause — and do NOT invent numbers.",
    ]
    for i, h in enumerate(hits, 1):
        lines.append(f"[{i}] (source: {h['source']})\n{h['text']}")
    return "\n\n".join(lines)


# --------------------------------------------------------------------------- #
# Hindsight memory (REST)
# --------------------------------------------------------------------------- #
async def hindsight_recall(query: str) -> list[str]:
    url = f"{HINDSIGHT_BANK_URL}/memories/recall"
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                url,
                json={"query": query, "budget": "low", "max_tokens": 900},
                timeout=RECALL_TIMEOUT_S,
            )
        r.raise_for_status()
        results = r.json().get("results", [])
        out = []
        for item in results[:8]:
            text = item.get("text") or item.get("content") or ""
            if text:
                out.append(" ".join(text.split()))
        return out
    except Exception as exc:
        log.warning("hindsight recall failed: %s", exc)
        return await hindsight_recent()


async def hindsight_recent(limit: int = 8) -> list[str]:
    url = f"{HINDSIGHT_BANK_URL}/memories/list?limit={limit}"
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=5)
        r.raise_for_status()
        items = r.json().get("items", [])
        out = []
        for item in items[:limit]:
            text = item.get("text") or item.get("content") or ""
            if text:
                out.append(" ".join(text.split()))
        return out
    except Exception as exc:
        log.warning("hindsight recent-list failed: %s", exc)
        return []


async def hindsight_retain(content: str, context: str, tags: list[str]):
    url = f"{HINDSIGHT_BANK_URL}/memories"
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                url,
                json={"items": [{"content": content, "context": context, "tags": tags}],
                      "async": True},
                timeout=20,
            )
        r.raise_for_status()
    except Exception as exc:
        log.warning("hindsight retain failed: %s", exc)


# --------------------------------------------------------------------------- #
# Per-user profile (local JSON, fast; mirrored into Hindsight)
# --------------------------------------------------------------------------- #
def _profile_path(chat_id) -> Path:
    return Path(DATA_DIR) / f"profile_{chat_id}.json"


def load_profile(chat_id) -> dict:
    try:
        return json.loads(_profile_path(chat_id).read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_profile(chat_id, profile: dict):
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    _profile_path(chat_id).write_text(json.dumps(profile), encoding="utf-8")


def has_profile(chat_id) -> bool:
    return bool(load_profile(chat_id))


# --------------------------------------------------------------------------- #
# Prompt / persona
# --------------------------------------------------------------------------- #
def _system_prompt() -> str:
    try:
        return Path(SYSTEM_PROMPT_PATH).read_text(encoding="utf-8").strip()
    except Exception:
        return "You are a knowledgeable workplace safety advisor. Cite your references."


def _split_send(text: str, limit: int = 4000) -> list[str]:
    return [text[i : i + limit] for i in range(0, len(text), limit)]


# --------------------------------------------------------------------------- #
# Handlers
# --------------------------------------------------------------------------- #
INTRO = (
    "G'day, I'm **Safety** — your on-call workplace safety advisor for WA industry.\n\n"
    "I cover general work health & safety, mining safety, and electrical standards: "
    "the WA WHS Act and Regulations, the AS/NZS electrical and PPE standards, and the "
    "practical hazard controls (isolation/lock-out, confined space, working at height, "
    "atmosphere testing, guarding, PPE, and more).\n\n"
    "So I can give you the most useful answers, tell me a bit about you:\n"
    "1. What industry / site are you in? (mining, construction, electrical, manufacturing, …)\n"
    "2. What's your role? (operator, sparky, supervisor, safety rep, …)\n"
    "3. What safety topics do you most want help with?\n\n"
    "Just reply with those details, or fire a question at me now — either way works. "
    "I always cite my references, and where I can't, I'll say so plainly."
)


async def _send(update: Update, text: str):
    for part in _split_send(text):
        await update.message.reply_text(part)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not has_profile(chat_id):
        await _send(update, INTRO)
    else:
        p = load_profile(chat_id)
        await _send(
            update,
            f"Welcome back. I have you down as {p.get('industry', '?')} / "
            f"{p.get('role', '?')}. What do you need today?",
        )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send(
        update,
        "I answer workplace safety questions for WA industry, with references to the "
        "standards and regulations.\n\n"
        "Commands:\n"
        "/start — introduction and setup\n"
        "/reset — forget your stored profile and start over\n"
        "/reload — re-index the standards corpus\n"
        "/status — show which models are in use\n\n"
        "You can also send me a photo (a hazard, an electrical panel, guarding, etc.) "
        "and I'll analyse it.\n\n"
        "General advice only — not a substitute for a site SWMS/JHA, a competent or "
        "licensed person, or the actual legislation. In an emergency call 000.",
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    _profile_path(chat_id).unlink(missing_ok=True)
    await _send(update, "Forgotten. Use /start to set up again.")


async def reload_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    KB.reload()
    await _send(update, f"Re-indexed the standards corpus ({len(KB.chunks)} chunks).")


async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send(update, "Model chain:\n" + model_status())


async def _answer_question(update: Update, question: str, chat_id: int):
    await update.message.chat.send_action(ChatAction.TYPING)

    profile = load_profile(chat_id)
    profile_txt = ""
    if profile:
        profile_txt = (
            f"The user's profile: industry={profile.get('industry', '?')}, "
            f"role={profile.get('role', '?')}, topics={profile.get('topics', '?')}."
        )

    memories = await hindsight_recall(question)
    memory_txt = ""
    if memories:
        memory_txt = "Prior context about this user (from memory):\n- " + "\n- ".join(memories)

    refs = build_reference_block(question)

    messages = [
        {"role": "system", "content": _system_prompt()},
    ]
    if profile_txt:
        messages.append({"role": "system", "content": profile_txt})
    if memory_txt:
        messages.append({"role": "system", "content": memory_txt})
    if refs:
        messages.append({"role": "system", "content": refs})
    messages.append({"role": "user", "content": question})

    try:
        answer, model = await generate(messages, TEXT_CHAIN, TEXT_MAX_TOKENS, TEXT_TIMEOUT_S)
    except Exception as exc:
        log.error("all text models failed: %s", exc)
        await _send(
            update,
            "Sorry — I can't reach a model right now. Please try again in a minute. "
            "(All configured models are unavailable.)",
        )
        return

    await _send(update, answer)

    # Mirror the exchange into memory (best-effort, async).
    await hindsight_retain(
        f"User ({profile.get('industry', 'unknown')}/{profile.get('role', 'unknown')}) "
        f"asked: {question[:1500]}\nSafety answered (via {model}): {answer[:1500]}",
        context="Safety-advisor Q&A",
        tags=["safety", "qa", profile.get("industry", "unknown")],
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = (update.message.text or "").strip()
    if not text:
        return

    if not has_profile(chat_id):
        # First substantive message: treat as the user introducing themselves.
        profile = {
            "industry": "unspecified",
            "role": "unspecified",
            "topics": text,
            "raw": text,
        }
        # Light parsing: if it reads like a question, still answer it after storing.
        save_profile(chat_id, profile)
        await hindsight_retain(
            f"User {chat_id} introduced themselves: {text[:800]}",
            context="Safety-advisor user profile",
            tags=["safety", "user-profile"],
        )
        await _send(
            update,
            "Thanks — noted. I've saved that as your context. If you can tell me your "
            "industry and role too, even better, but for now go ahead and ask me anything.",
        )
        if _looks_like_question(text):
            await _answer_question(update, text, chat_id)
        return

    await _answer_question(update, text, chat_id)


def _looks_like_question(text: str) -> bool:
    return bool(re.search(r"\?|what|how|is |are |should |can |do |does |when |why ", text, re.I))


VISION_PROMPT = (
    "You are a workplace safety advisor. Analyse this image for safety: identify any "
    "hazards, unsafe conditions, missing controls, or non-compliances you can see, and "
    "reference the relevant Australian/New Zealand standard or WA regulation where you "
    "are confident of the number. Be specific and practical. If you cannot confidently "
    "identify something or reference a specific standard, say so plainly instead of guessing."
)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.chat.send_action(ChatAction.TYPING)

    photo = update.message.photo[-1]
    try:
        f = await photo.get_file()
        data = await f.download_as_bytearray()
    except Exception as exc:
        log.error("photo download failed: %s", exc)
        await _send(update, "Couldn't download that image. Try sending it again.")
        return

    b64 = base64.b64encode(bytes(data)).decode()
    mime = "image/jpeg"
    caption = update.message.caption or ""

    messages = [
        {"role": "system", "content": _system_prompt()},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": (VISION_PROMPT + "\n\n" + caption).strip()},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
            ],
        },
    ]

    try:
        answer, model = await generate(messages, VISION_CHAIN, VISION_MAX_TOKENS, VISION_TIMEOUT_S)
    except Exception as exc:
        log.error("all vision models failed: %s", exc)
        await _send(
            update,
            "Sorry — I can't analyse images right now (no vision model available). "
            "Describe what you're looking at and I'll help as best I can.",
        )
        return

    await _send(update, answer)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main():
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("reload", reload_cmd))
    app.add_handler(CommandHandler("status", status_cmd))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    log.info("Safety advisor starting. Text chain: %s", [m["name"] for m in TEXT_CHAIN])
    log.info("Vision chain: %s", [m["name"] for m in VISION_CHAIN])
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
