# 🤖 Telegram Bot Template

Шаблон асинхронного Telegram-бота на базе **Aiogram 3**, **Pydantic Settings** и **SQLAlchemy + aiomysql**.

---

## 🚀 Стек технологий

- 🧠 **Aiogram 3** — современный асинхронный Telegram-фреймворк
- ⚙️ **Pydantic v2 + pydantic-settings** — безопасная работа с `.env`
- 🗃 **SQLAlchemy 2 (async)** — ORM для работы с MySQL
- 🔌 **aiomysql** — асинхронный драйвер для MySQL
- 📊 Структурированный код (middlewares, filters, routers, FSM, handlers)

---

## 📂 Структура проекта

```bash
project/
│
├── .env                   # Переменные окружения
├── requirements.txt       # Зависимости проекта
├── README.md              # Документация проекта
├── main.py                # Точка входа в бота
├── create_bot.py          # Создание экземпляра бота и диспатчера
├── config.py              # Настройки через pydantic-settings
├── middlewares/           # Middleware (например, для db-сессии)
│   └── db_session_middleware.py
│
├── filters/               # Кастомные фильтры (например, IsAdmin)
│   ├── is_admin.py
│   └── callback_data_filter.py
│
├── keyboards/             # Клавиатуры
│   └── admin/
│   │    └── utm.py        # Панель управления UTM ссылками
│   │    └── panel.py      # Админ панель
│   └── client/
│
├── services/              # Сервисы
│   └── logger.py          # Логирование
│
│
├── states/                # Состояния FSM
│   └── admin/
│   │    └── spam.py       # States для рассылки
│   │    └── utm.py        # States для добавления и удаления UTM
│   └── client/
│
├── database/
│   ├── db.py              # Инициализация подключения и создания таблиц
│   ├── models.py          # SQLAlchemy модели (User, Payment, UTM)
│   ├── session.py         # Фабрика асинхронных сессий
│   └── crud/
│       ├── user.py        # CRUD-операции для пользователей
│       ├── utm.py         # CRUD-операции для UTM-ссылок
│
└── handlers/
    ├── admin/
    │   └── utm.py         # Хендлеры для UTM меню
    │   └── spam.py        # Хендлеры для рассылки
    │   └── panel.py       # Хендлер получения панели
    └── user/
        └── start.py       # Хендлеры для пользователей
```
## ⚙️ Установка

```bash
git clone https://github.com/username/your-bot.git
cd your-bot

# Установить зависимости
python -m venv .venv
source .venv/bin/activate      # или .venv\Scripts\activate для Windows
pip install -r requirements.txt
```

## 📄 Создай .env файл

```bash
BOT__TOKEN=1231
BOT__ADMINS=[123, 1234, 3432]

DB__MYSQL_HOST=localhost
DB__MYSQL_PORT=3306
DB__MYSQL_USER=root
DB__MYSQL_PASSWORD=password
DB__MYSQL_DB=database

CRYPTOBOT__API_KEY=your_crypto_api_key


YOOKASSA__SHOP_ID=56789
YOOKASSA__API_KEY=youkassa_api_key_here

```

## 🏁 Запуск
```bash
python main.py
```
## 📚 Возможности (включённые)
 - Асинхронная БД (MySQL)
 - FSM состояния
 - UTM ссылки
 - Рассылка
 - Middleware для сессий
 - Inline-кнопки с пагинацией
 - Статистика пользователей
 - Кастомные фильтры (админ, callback)

## 🧠 TODO
 - Интеграция с Redis
 - Админ-панель (web)