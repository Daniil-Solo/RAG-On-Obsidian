# Rag-On-Obsidian

A web application for using RAG based on Obsidian Notes

## Сборка Docker-образа

```bash
docker build -f Dockerfile -t ragobs:latest .
```
## Запуск Docker-образа
Для директории с заметками Obsidian нужно использовать полный путь в системе
```bash
docker run --rm -it -p 5000:5000 -v ./obsidian:/obsidian -e OBSIDIAN_PATH='/obsidian' -e ORIGINS='http://localhost:5173' --name ragobs -d ragobs:latest
```