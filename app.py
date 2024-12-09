from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
DATA_FILE = 'data.json'

# Функция для чтения данных из JSON-файла
def read_data():
    if not os.path.exists(DATA_FILE):
        return {"classes": []}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Функция для записи данных в JSON-файл
def write_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Эндпоинт для получения списка занятий (GET)
@app.route('/api/classes', methods=['GET'])
def get_classes():
    data = read_data()
    return jsonify(data)

# Обработчик главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# Эндпоинт для записи на занятие (POST)
@app.route('/api/classes/book', methods=['POST'])
def book_class():
    data = read_data()
    req_data = request.get_json()

    # Валидация входных данных
    if 'id' not in req_data:
        return jsonify({"error": "Не указан ID занятия"}), 400

    class_id = req_data['id']
    for item in data['classes']:
        if item['id'] == class_id:
            if item['booked'] >= item['capacity']:
                return jsonify({"error": "Нет доступных мест"}), 400
            item['booked'] += 1
            write_data(data)
            return jsonify({"message": "Запись успешна"}), 200

    return jsonify({"error": "Занятие с таким ID не найдено"}), 404

if __name__ == '__main__':
    # Создаем пример данных при первом запуске
    if not os.path.exists(DATA_FILE):
        write_data({
            "classes": [
                {"id": 1, "name": "Йога", "instructor": "Анна", "time": "10:00", "capacity": 10, "booked": 0},
                {"id": 2, "name": "Пилатес", "instructor": "Иван", "time": "12:00", "capacity": 8, "booked": 0},
                {"id": 3, "name": "Кардио", "instructor": "Мария", "time": "18:00", "capacity": 15, "booked": 0},
            ]
        })
    app.run(debug=True)
