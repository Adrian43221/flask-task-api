# 📝 Flask Task Manager API

Простой API для управления задачами с JWT авторизацией.  
Позволяет регистрироваться, входить в систему и управлять своими задачами (CRUD).

---

## 🚀 Технологии

- Python 3.11+
- Flask
- SQLAlchemy
- Flask-Migrate
- JWT (JSON Web Tokens)
- SQLite (или другая СУБД)

---

## 🔐 Функции

- Регистрация пользователя `/register`
- Авторизация по email и паролю `/login`
- Создание задач `/tasks [POST]`
- Получение всех задач `/tasks [GET]`
- Обновление задачи `/tasks/<id> [PUT]`
- Удаление задачи `/tasks/<id> [DELETE]`

Все защищённые маршруты требуют JWT-токен в заголовке:

```http
Authorization: Bearer <your_token>
