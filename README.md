# Safety — WA workplace-safety advisor (Telegram bot)

A containerised Telegram bot on the AI server (`dualepyc`) that gives industrial and
mining workers referenced safety and electrical-standards advice for Western Australia.

## Architecture

* **Telegram** front-end (`python-telegram-bot`, async long-polling).
* **LLM layer**: ordered model chain per role, local-first with cloud fallback,
  sticky health back-off (a failed model is skipped for 5 min, then re-probed).
  * Text: `muse-glimmer-30b` on `:8141` → DeepSeek cloud.
  * Vision: `qwen3.8-27b-uncensored` on `:8109` → OpenAI `gpt-4o`.
* **Memory**: Hindsight bank `safety` (REST on `:8897`) — per-user profile + Q&A
  retained async; per-message semantic recall injects prior context.
* **Knowledge**: BM25 retrieval over the `knowledge/*.md` corpus (WA WHS legislation,
  AS/NZS electrical + PPE standards, hazard controls) injected into each prompt.
  The system prompt enforces citation discipline and the
  "(unable to recall reference, not verified)" marker.

## Deploy

    # on the server (mat@10.42.0.182), from /home/mat/safety-advisor
    docker build -t safety-advisor:local .
    docker run -d --name safety-advisor --network host --restart unless-stopped \
      --env-file /home/mat/safety-advisor/.env \
      -v /home/mat/safety-advisor/knowledge:/app/knowledge:ro \
      -v /home/mat/safety-advisor/data:/app/data \
      safety-advisor:local

## Env (mode-600 `.env`, never committed)

    TELEGRAM_BOT_TOKEN=...
    LOCAL_TEXT_URL=http://127.0.0.1:8141/v1
    LOCAL_TEXT_MODEL=muse-glimmer-30b
    LOCAL_TEXT_KEY=...
    DEEPSEEK_API_KEY=...
    DEEPSEEK_MODEL=deepseek-chat
    LOCAL_VISION_URL=http://127.0.0.1:8109/v1
    LOCAL_VISION_MODEL=qwen3.8-27b-uncensored
    LOCAL_VISION_KEY=...
    OPENAI_API_KEY=...
    OPENAI_VISION_MODEL=gpt-4o
    HINDSIGHT_BANK_URL=http://127.0.0.1:8897/v1/default/banks/safety

## Bot commands

`/start` · `/help` · `/reset` (forget profile) · `/reload` (re-index corpus) ·
`/status` (show model chain health). Photos are analysed for hazards.

## Ops notes

* The local model landscape is volatile (models are reallocated across the GPUs).
  The bot never depends on any single local model: it health-checks and falls back
  to cloud, re-probing local models periodically, so it keeps working through churn.
* To update the standards corpus, add/replace `*.md` files in `knowledge/`, then
  `/reload` (or restart the container).
* Hindsight bank `safety` is created once via
  `PUT /v1/default/banks/safety` (see the create script).
