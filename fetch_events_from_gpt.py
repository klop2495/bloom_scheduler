# fetch_events_from_gpt.py

import openai
import os
import datetime
import time
import json

# Загрузка секретов из /etc/secrets (Render Secret Files)
with open("/etc/secrets/OPENAI_API_KEY", "r") as f:
    openai.api_key = f.read().strip()

with open("/etc/secrets/ASSISTANT_ID", "r") as f:
    ASSISTANT_ID = f.read().strip()

# Определяем текущую дату и диапазон
today = datetime.date.today()
end_date = today + datetime.timedelta(days=14)
date_range_str = f"с {today.strftime('%d.%m.%Y')} по {end_date.strftime('%d.%m.%Y')}"

# Формируем запрос
query = f"""Сегодня {today.strftime('%d.%m.%Y')}. Найди 10–20 событий в Париже и ближайших городах, интересных для съёмки в период {date_range_str}. Включай только события с визуальным потенциалом и возможностью аккредитации."""

# Запускаем GPT-ассистента
thread = openai.beta.threads.create()

openai.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=query
)

run = openai.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=ASSISTANT_ID,
)

# Ожидаем завершения работы
print("⏳ Ждём ответ от ассистента...")
while True:
    run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    if run.status == "completed":
        break
    elif run.status == "failed":
        print("❌ Ошибка выполнения")
        exit(1)
    time.sleep(1)

# Получаем и обрабатываем ответ
messages = openai.beta.threads.messages.list(thread_id=thread.id)
gpt_output = ""
for message in reversed(messages.data):
    gpt_output += message.content[0].text.value + "\n"

# Сохраняем результат в файлы
with open("analytics.html", "w") as f:
    f.write(f"<pre>{gpt_output}</pre>")

with open("analytics.json", "w") as f:
    json.dump({"content": gpt_output}, f, ensure_ascii=False, indent=2)

print("✅ События сохранены в analytics.html и analytics.json")

