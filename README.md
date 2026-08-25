# Task API

A CRUD API for managing a to-do list, built with FastAPI and backed by PostgreSQL, running in Docker. Built as part of the AI Fluency Backend track (BE-01 → BE-04).

## What this is

A REST API with five endpoints to create, read, update, and delete tasks. Storage moved from an in-memory list (BE-01) to SQLite (BE-02) to PostgreSQL (BE-04), running alongside the app in Docker.

## Architecture: the repository pattern

Storage logic lives entirely inside `repository.py`, behind a consistent interface (`list_all`, `get`, `create`, `update`, `delete`). `main.py` (the routes) only ever calls these methods — it never touches SQL directly.

This means swapping the storage backend from SQLite to Postgres required changing exactly **one place**: the import and the line that creates `repo` in `main.py`. Every route function was left completely untouched. That's the point of this architecture — the API layer doesn't know or care what database is underneath it.

## How to run it

**With Docker (recommended):**
```
docker compose up --build
```
This starts both the Postgres database and the FastAPI app together. The app will be available at `http://localhost:8000`.

**Without Docker (local Postgres required):**
1. Set `DATABASE_URL` in a `.env` file (see `.env.example`)
2. Install dependencies: `py -m pip install -r requirements.txt`
3. Run: `py -m uvicorn main:app --reload --port 8000`

## Environment variables

Connection details are read from `DATABASE_URL`, provided via `.env` (gitignored). See `.env.example` for the expected format:
```
DATABASE_URL=postgresql://taskuser:taskpass@localhost:5432/taskdb
```
When running via `docker compose`, this is set directly in `docker-compose.yml` instead, pointing at the `db` service by name rather than `localhost`.

## Endpoints

| Method | Path            | Description                          | Success | Errors |
|--------|-----------------|---------------------------------------|---------|--------|
| GET    | `/`             | API info                              | 200     | —      |
| GET    | `/health`       | Health check                          | 200     | —      |
| GET    | `/tasks`        | List all tasks                        | 200     | —      |
| GET    | `/tasks/{id}`   | Get a single task                     | 200     | 404 if not found |
| POST   | `/tasks`        | Create a new task                     | 201     | 400 if title missing/empty |
| PUT    | `/tasks/{id}`   | Replace a task's title and done status| 200     | 400 invalid body, 404 if not found |
| DELETE | `/tasks/{id}`   | Remove a task                         | 204     | 404 if not found |

## Proving persistence

Persistence was verified by:
1. Creating a task via `POST /tasks`
2. Confirming it appeared in `GET /tasks`
3. Running `docker compose down` (stopping and removing both containers)
4. Running `docker compose up` again
5. Checking `GET /tasks` — the task was still present

This confirms the Postgres data volume (`task-pg-data`) persists independently of the container lifecycle — restarting or recreating the containers does not erase the database.

## Database setup

The `tasks` table is created automatically the first time the Postgres container starts, via `init.sql`, mounted into Postgres's init directory in `docker-compose.yml`. No manual setup step is required when using `docker compose up`.