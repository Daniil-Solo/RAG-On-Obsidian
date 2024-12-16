FROM node:20.11-alpine as react_builder
WORKDIR /frontend
COPY ./frontend /frontend
ENV VITE_APPLICATION_MODE=production
RUN npm install
RUN npm run build

FROM python:3.11-slim AS python_builder
WORKDIR /app
COPY ./backend/pyproject.toml ./
RUN python -m pip install --no-cache-dir poetry && poetry config virtualenvs.in-project true && poetry install --no-interaction --no-ansi

FROM python:3.11-slim as production
WORKDIR /app
COPY --from=python_builder /app /app
COPY --from=react_builder /frontend/dist /react_static
COPY ./backend/src /app/src
ENV MODE=production
ENV STATIC_PATH=/react_static
CMD ["/app/.venv/bin/uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "5000"]
