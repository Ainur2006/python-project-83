# Анализатор страниц

**Page Analyzer** — веб-приложение на Python и Flask для анализа SEO-параметров веб-страниц. Приложение позволяет добавлять URL, просматривать список сайтов и запускать проверки, которые извлекают основные SEO-данные страницы.

**Демо:** https://page-analyzer-bx20.onrender.com

## Стек технологий

* Python
* Flask
* PostgreSQL
* Psycopg
* BeautifulSoup
* Requests
* Tailwind CSS
* Ruff

## Установка и запуск

### 1. Клонирование репозитория

Убедитесь, что у вас установлены Git, Python 3.13 или новее, `uv`, Node.js и npm.

```bash
git clone https://github.com/Ainur2006/python-project-83.git
cd python-project-83
```

### 2. Установка зависимостей

Установите Python- и Node.js-зависимости:

```bash
make install
```

### 3. Настройка PostgreSQL

Создайте базу данных PostgreSQL. Например, можно назвать её `page_analyzer`.

Создайте файл `.env` в корне проекта и добавьте настройки подключения:

```dotenv
DATABASE_URL=postgresql://username:password@localhost:5432/page_analyzer
SECRET_KEY=your-secret-key
```

Замените `username` и `password` на данные своего пользователя PostgreSQL.

`SECRET_KEY` используется Flask для защиты сессий и flash-сообщений. Для локальной разработки укажите собственное случайное значение.

### 4. Создание таблиц

Выполните SQL-скрипт, который создаёт необходимые таблицы:

```bash
psql "$DATABASE_URL" -f database.sql
```

Команда предполагает, что PostgreSQL запущен, а утилита `psql` установлена.

### 5. Сборка CSS

Скомпилируйте стили Tailwind CSS:

```bash
make build-css
```

### 6. Запуск приложения

Запустите Flask в режиме разработки:

```bash
make dev
```

После запуска откройте в браузере:

http://127.0.0.1:5000

## Возможности

* Добавление URL и просмотр списка сайтов.
* Просмотр информации о конкретном сайте.
* Запуск SEO-проверок веб-страниц.
* Извлечение HTTP-статуса, заголовка H1, тега Title и метаописания Description.
* Хранение результатов проверок в PostgreSQL.

## Проверка кода

Для запуска линтера Ruff выполните:

```bash
make lint
```

## Деплой

Приложение развёрнуто на Render:

https://page-analyzer-bx20.onrender.com
