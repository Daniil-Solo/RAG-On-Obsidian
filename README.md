# Rag-On-Obsidian

A web application for using RAG based on Obsidian Notes
![image](https://github.com/user-attachments/assets/83606546-a0a7-454e-88c2-19c9cf726acc)
![image](https://github.com/user-attachments/assets/09cea54f-99bc-4b7b-87a1-f2a657d2f042)



## Сборка Docker-образа

```bash
docker build -f Dockerfile -t ragobs:latest .
```
## Запуск Docker-образа
Для директории с заметками Obsidian нужно использовать полный путь в системе
```bash
docker-compose up -d
```
