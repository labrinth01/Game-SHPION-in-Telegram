# 🕵️ Telegram Bot "Шпион" - Руководство по запуску

## 📋 Описание

Telegram бот для игры "Шпион" с Mini App интерфейсом и админ-панелью.

**Возможности:**
- 🎮 Игра "Шпион" через Telegram Mini App
- 👥 Управление пользователями
- 📍 Управление локациями для игры
- 📊 Статистика игр и игроков
- 📢 Рассылка сообщений пользователям
- 🔒 Блокировка пользователей

---

## 🚀 Установка и запуск

### 1. Требования

- Python 3.9+
- Telegram Bot Token (получить у [@BotFather](https://t.me/BotFather))
- Домен с HTTPS для Mini App (можно использовать ngrok для тестирования)

### 2. Клонирование и установка зависимостей

```bash
cd spy_game_bot
pip install -r requirements.txt
```

### 3. Настройка окружения

Скопируйте `.env.example` в `.env`:

```bash
cp .env.example .env
```

Отредактируйте `.env` файл:

```env
# Токен бота от @BotFather
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# ID администраторов (ваш Telegram ID)
ADMIN_IDS=123456789

# URL где будет размещён Mini App
WEBAPP_URL=https://yourdomain.com

# Данные для входа в админ-панель
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password
SECRET_KEY=your-random-secret-key-here

# База данных (SQLite для разработки)
DATABASE_URL=sqlite:///spy_game.db
```

**Как узнать свой Telegram ID:**
- Напишите боту [@userinfobot](https://t.me/userinfobot)

### 4. Инициализация базы данных

База данных создастся автоматически при первом запуске. Для добавления начальных локаций:

```bash
python -c "
from database import init_db, get_db, Location
from config import config

init_db(config.DATABASE_URL)
db = get_db().get_session()

locations = [
    'Больница', 'Школа', 'Ресторан', 'Аэропорт', 'Банк',
    'Полицейский участок', 'Кинотеатр', 'Супермаркет', 'Пляж',
    'Казино', 'Цирк', 'Университет', 'Посольство', 'Отель',
    'Военная база', 'Космическая станция', 'Пиратский корабль',
    'Подводная лодка', 'Театр', 'Музей'
]

for loc_name in locations:
    location = Location(name=loc_name)
    db.add(location)

db.commit()
db.close()
print('Локации добавлены!')
"
```

### 5. Запуск бота

```bash
python -m bot.main
```

Бот должен запуститься и вывести:
```
INFO:__main__:Database initialized
INFO:__main__:Bot started
```

### 6. Запуск админ-панели

В отдельном терминале:

```bash
python admin/app.py
```

Админ-панель будет доступна по адресу: `http://localhost:5000/admin`

---

## 🌐 Настройка Mini App

### Вариант 1: Локальная разработка с ngrok

1. Установите [ngrok](https://ngrok.com/)

2. Запустите ngrok для админ-панели (она будет раздавать статику):

```bash
ngrok http 5000
```

3. Скопируйте HTTPS URL (например: `https://abc123.ngrok.io`)

4. Обновите `.env`:
```env
WEBAPP_URL=https://abc123.ngrok.io
```

5. Перезапустите бота

### Вариант 2: Деплой на хостинг

**Для продакшена рекомендуется:**
- VPS (DigitalOcean, AWS, Hetzner)
- Nginx для раздачи статики
- PostgreSQL вместо SQLite
- Systemd для автозапуска

**Пример nginx конфига:**

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static {
        alias /path/to/spy_game_bot/webapp/static;
    }

    location /game {
        alias /path/to/spy_game_bot/webapp;
        try_files $uri $uri/ /index.html;
    }

    location /admin {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://127.0.0.1:5000;
    }
}
```

---

## 📱 Настройка бота в BotFather

1. Откройте [@BotFather](https://t.me/BotFather)

2. Создайте бота: `/newbot`

3. Настройте Menu Button для Mini App:
```
/setmenubutton
@your_bot_username
Играть
https://yourdomain.com/game
```

4. Настройте описание:
```
/setdescription
@your_bot_username
🕵️ Играй в Шпиона с друзьями! Найди шпиона или останься незамеченным.
```

---

## 🎮 Как играть

1. Пользователь запускает бота: `/start`
2. Нажимает кнопку "🎮 Играть" (открывается Mini App)
3. Создаёт игру или присоединяется по коду
4. Когда собралось 3+ игроков, хост начинает игру
5. Все получают локацию (кроме шпиона)
6. Игроки задают вопросы и голосуют
7. Побеждают мирные (если нашли шпиона) или шпион (если угадал локацию)

---

## 🔧 Структура проекта

```
spy_game_bot/
├── bot/                    # Telegram бот
│   ├── handlers/          # Обработчики команд
│   ├── keyboards/         # Клавиатуры
│   ├── utils/            # Утилиты (рассылка)
│   └── main.py           # Точка входа бота
├── webapp/                # Mini App
│   ├── static/
│   │   ├── css/          # Стили
│   │   └── js/           # Логика игры
│   └── index.html        # Главная страница
├── admin/                 # Админ-панель
│   ├── templates/        # HTML шаблоны
│   ├── static/           # Стили админки
│   └── app.py            # Flask приложение
├── database/             # База данных
│   ├── models.py         # SQLAlchemy модели
│   └── db.py             # Подключение к БД
├── config/               # Конфигурация
│   └── config.py
├── requirements.txt      # Зависимости
├── .env.example         # Пример конфига
└── README.md            # Это руководство
```

---

## 📊 Админ-панель

Доступна по адресу: `http://localhost:5000/admin`

**Возможности:**
- 📊 Дашборд с общей статистикой
- 👥 Управление пользователями (блокировка)
- 📍 Добавление/удаление локаций
- 📢 Рассылка сообщений всем пользователям
- 📈 Статистика игр и топ игроков

**Логин по умолчанию:**
- Username: `admin`
- Password: `admin123` (измените в `.env`!)

---

## 🐳 Docker (опционально)

Создайте `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "bot.main"]
```

Запуск:
```bash
docker build -t spy-bot .
docker run -d --env-file .env spy-bot
```

---

## 🔒 Безопасность

**Для продакшена:**
1. Измените `ADMIN_PASSWORD` и `SECRET_KEY` в `.env`
2. Используйте PostgreSQL вместо SQLite
3. Настройте HTTPS (Let's Encrypt)
4. Ограничьте доступ к админ-панели (IP whitelist)
5. Регулярно делайте бэкапы БД

---

## 🐛 Решение проблем

**Бот не отвечает:**
- Проверьте `BOT_TOKEN` в `.env`
- Убедитесь, что бот запущен: `python -m bot.main`

**Mini App не открывается:**
- Проверьте `WEBAPP_URL` в `.env`
- URL должен быть HTTPS
- Проверьте настройки Menu Button в BotFather

**Ошибка базы данных:**
- Удалите `spy_game.db` и перезапустите бота
- Проверьте права доступа к файлу БД

**Админ-панель не открывается:**
- Проверьте, запущен ли Flask: `python admin/app.py`
- Порт 5000 должен быть свободен

---

## 📝 TODO / Улучшения

- [ ] API для игровой логики (сейчас упрощённая версия в JS)
- [ ] WebSocket для real-time обновлений
- [ ] Рейтинговая система
- [ ] Достижения и награды
- [ ] Кастомные наборы локаций
- [ ] Мультиязычность

---

## 📄 Лицензия

MIT License

---

## 💬 Поддержка

Если возникли вопросы - создайте Issue в репозитории.

**Удачной игры! 🕵️**
