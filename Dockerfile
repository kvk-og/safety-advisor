FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py system_prompt.txt ./
RUN mkdir -p /app/knowledge /app/data

ENV PYTHONUNBUFFERED=1 \
    KNOWLEDGE_DIR=/app/knowledge \
    DATA_DIR=/app/data \
    SYSTEM_PROMPT_PATH=/app/system_prompt.txt

CMD ["python", "bot.py"]
