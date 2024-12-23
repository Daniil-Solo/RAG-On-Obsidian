# Rag-On-Obsidian

A web application for using RAG based on Obsidian Notes
![image](https://github.com/user-attachments/assets/83606546-a0a7-454e-88c2-19c9cf726acc)
![image](https://github.com/user-attachments/assets/09cea54f-99bc-4b7b-87a1-f2a657d2f042)



## Запуск приложения

### Docker (рекомендуемый вариант)
0. Убедитесь, что он установлен и запущен на машине командой `docker -v`
1. Скачиваем файл [docker-compose.yml](https://raw.githubusercontent.com/Daniil-Solo/RAG-On-Obsidian/refs/heads/main/docker-compose.yml)
2. Указываем в web.volumes вместо `./backend/obsidian` абсолютный путь до директории с заметками Obsidian
3. Выполняем в директории с файлом команду `docker-compose up -d`
4. Переходим на http://localhost/ в браузере
3. Вы великолепны!

### Без Docker
- Если у вас Linux/MacOS, то рассмотрите вариант с установкой Docker, а потом вернитесь к запуску из Docker
- Если у вас Windows, то рассмотрите вариант с установкой WSL и поверх него Docker, а потом вернитесь к запуску из Docker

Если предыдущие два варианта не подходят, то поехали запускать без Docker:
1. Устанавливаем PostgreSQL, создаем базу данных, не забываем пароль
2. Устанавливаем расширение pgvector в этой базе данных командой: `CREATE EXTENSION IF NOT EXISTS vector;`
3. Скачиваем репозиторий командой: `git clone https://github.com/Daniil-Solo/RAG-On-Obsidian.git`
4. Создаем виртуальное окружение в директории backend и устанавливаем зависимости: `pip install poetry && poetry install`
5. Скачиваем папку с билдом фронта в директорию backend [папку с Google-диска](https://drive.google.com/drive/folders/13eJsjdyAk7QsPuFDU_Jwq0nZNWYhmWoo?usp=sharing)
6. Создаем в директори backend файл .env и заполняем его:
```env
MODE=production
OBSIDIAN_PATH=<YOUR-ABSOLUTE-PATH-TO-OBSIDIAN-NOTES-DIRECTORY>
STATIC_PATH=<YOUR-ABSOLUTE-PATH-TO-FRONT-BUIKD-DIRECTORY>
DB_HOST=<YOUR-DATABASE-HOST> # default is localhost
DB_PORT=<YOUR-DATABASE-PORT> # default is 5432
DB_USER=<YOUR-USER-NAME-IN-POSTGRES> # default is postgres
DB_PASSWORD=<YOUR-PASSWORD-IN-POSTGRES>
DB_NAME=<YOUR-DATABASE-NAME-IN-POSTGRES> # default is postgres
```
7. Из директории backend запускаем командой: `poetry run uvicorn src.app:app --port 5000`
8. Переходим на http://localhost/ в браузере
9. Вы восхитительны!

### Что-то не получилось?
По всем вопросам запуска можно обращаться к [Даниилу](https://t.me/daniilsolovjev)

