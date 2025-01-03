# API

## Локальная разработка

### Старт
1. Создать venv в директории backend
2. Выполнить установку менеджера пакета: `pip install poetry`
3. Выполнить установку библиотек: `poetry install`
4. Создать .env в директории backend со следующим содержимым
```env
OBSIDIAN_PATH=<absolute path to obsidian folder>
MODE=debug
```

### Запуск сервера

```bash
poetry run uvicorn src.app:app --port 5000 --reload
```

### Запуск линтера ruff

```bash
poetry run ruff check src
```

### Сборка Docker-образа для API-сервиса

```bash
docker build -f Dockerfile -t ragobs-api:latest .
```

### Запуск приложения из Docker-образа
```bash
docker run --rm -it -p 5000:5000 -v ./obsidian:/app/obsidian -e OBSIDIAN_PATH='/app/obsidian' -e ORIGINS='http://localhost:5173' --name ragobs-api -d ragobs-api:latest
```

### Запуск Postgres с PgVector в Docker

```bash
docker compose -f pgvector.docker-compose.yml up -d
```