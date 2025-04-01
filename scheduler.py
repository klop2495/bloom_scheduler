from datetime import datetime, timedelta

# Пример текущих событий (можно заменить загрузкой из календаря)
current_events = [
    {
        "id": "event_001",
        "title": "Съёмка в Музее Орсе",
        "start": "2025-04-05T08:00:00",
        "end": "2025-04-05T09:30:00"
    }
]

BUFFER_MINUTES = 120

def check_schedule(new_event):
    new_start = datetime.fromisoformat(new_event["start"])
    for evt in current_events:
        existing_end = datetime.fromisoformat(evt["end"])
        diff = (new_start - existing_end).total_seconds() / 60
        if 0 <= diff < BUFFER_MINUTES:
            return {
                "status": "conflict",
                "conflict_with": {
                    "id": evt["id"],
                    "title": evt["title"],
                    "end": evt["end"]
                },
                "reason": f"Недостаточно времени на дорогу: только {int(diff)} минут при минимуме {BUFFER_MINUTES}."
            }
    return {"status": "confirmed"}
