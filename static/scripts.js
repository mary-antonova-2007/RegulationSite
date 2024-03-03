// Получение элементов для модального окна
var modal = document.getElementById("myModal");
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");

function openImage(img) {
    modal.style.display = "block";
    modalImg.src = img.src;
    captionText.innerHTML = img.alt;
}

// Получение элемента <span> (кнопка закрыть) и закрытие модального окна при клике на нее
var span = document.getElementsByClassName("close")[0];
span.onclick = function() {
    modal.style.display = "none";
};

// Функция для отображения кнопки прокрутки наверх
window.onscroll = function() { scrollFunction(); };

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("myBtn").style.display = "block";
    } else {
        document.getElementById("myBtn").style.display = "none";
    }
}

// При нажатии на кнопку, прокрутить вверх страницу
function topFunction() {
    document.body.scrollTop = 0; // Для Safari
    document.documentElement.scrollTop = 0; // Для Chrome, Firefox, IE и Opera
}

// Функция для проверки непрочитанных уведомлений
function checkNotifications() {
    var notificationsUrl = document.getElementById('unreadNotificationsUrl').getAttribute('data-url');
    $.ajax({
        url: notificationsUrl,
        success: function(data) {
            console.log("Непрочитанных уведомлений:", data.count);
            $('#notification-count').text(data.count);
        },
        error: function(err) {
            console.log("Ошибка запроса:", err);
        }
    });
}

// Вызов функции при загрузке страницы
checkNotifications();

// Повторение вызова каждые 30 секунд
setInterval(checkNotifications, 30000);

// Функция для перехода по URL
function goToNotifications() {
    window.location.href = '/notifications/notifications/'; // Укажите правильный путь
}

// Добавление обработчика события к контейнеру уведомлений
document.getElementById('notification-container').addEventListener('click', goToNotifications);