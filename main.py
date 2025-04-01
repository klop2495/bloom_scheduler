from flask import Flask, request, jsonify

app = Flask(__name__)

# Маршрут для корневого URL: возвращает простое сообщение, что сервис работает
@app.route('/')
def index():
    return "Bloom Scheduler API is running"

# Существующий POST-маршрут для /api/bloom/schedule
@app.route('/api/bloom/schedule', methods=['POST'])
def bloom_schedule():
    # Предполагаем, что клиент отправляет JSON с параметрами расписания.
    data = request.get_json()
    if not data:
        # Если данных нет, возвращаем ошибку 400
        return jsonify({"error": "No data provided"}), 400

    # *** Здесь находится основная логика планирования (schedule) ***
    # Например, получение данных расписания из `data`,
    # выполнение необходимых действий (сохранение задания, запуск процесса и т.д.)
    # В данном шаблоне кода мы просто эмулируем успешный ответ.

    # Формируем ответ (например, подтверждение запланированной задачи)
    response = {
        "message": "Bloom schedule request received",
        "scheduled_data": data
    }
    return jsonify(response), 200

# Запуск приложения на локальном сервере (при необходимости)
# При деплое на Render этот блок обычно не обязателен,
# так как Gunicorn сам подхватывает приложение через переменную `app`.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

