# Бэкенд часть проекта

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

### Контейнеризация приложения в Docker

```bash
docker build -f Dockerfile.prod -t rag-on-obsidian:latest .
```

### Запуск приложения из Docker-образа
```bash
docker run --rm -it -p 5000:5000 -v ./obsidian:/app/obsidian -e OBSIDIAN_PATH='/app/obsidian' -e ORIGINS='http://localhost:5173' --name rag-on-obsidian -d rag-on-obsidian:latest
```