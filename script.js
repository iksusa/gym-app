// Загрузка списка занятий
function loadClasses() {
    fetch('http://127.0.0.1:5000/api/classes')  // Указать адрес сервера явно)
        .then(response => response.json())
        .then(data => {
            renderClasses(data.classes);
        })
        .catch(error => {
            console.error('Ошибка загрузки данных:', error);
        });
}

// Отображение списка занятий
function renderClasses(classes) {
    const classesContainer = document.getElementById('classes');
    classesContainer.innerHTML = '';

    classes.forEach(item => {
        const card = `
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">${item.name}</h5>
                        <p>Инструктор: ${item.instructor}</p>
                        <p>Время: ${item.time}</p>
                        <p>Мест: ${item.booked}/${item.capacity}</p>
                    </div>
                </div>
            </div>`;
        classesContainer.innerHTML += card;
    });
}

// Обработка формы записи
document.getElementById('booking-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const classId = parseInt(document.getElementById('class-id').value.trim(), 10);

    fetch('http://127.0.0.1:5000/api/classes/book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: classId })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`Ошибка: ${data.error}`);
            } else {
                alert('Запись успешна!');
                loadClasses();
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
});

// Инициализация
document.addEventListener('DOMContentLoaded', loadClasses);
