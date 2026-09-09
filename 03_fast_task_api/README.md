# FastAPI task API

An in-memory task API built with FastAPI and Pydantic.

## Run it

```bash
uv run fastapi dev src/fast_task_api/http_server.py
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.

## Routes

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/tasks` | Create a task with `{ "name": "Buy milk" }`. |
| `GET` | `/tasks` | List all tasks. |
| `GET` | `/tasks/{task_id}` | Fetch one task. |
| `PATCH` | `/tasks/{task_id}` | Set completion with `{ "completed": true }`. |
| `DELETE` | `/tasks/{task_id}` | Delete one task. |

Tasks live in memory. Restarting the server clears them.

## How it is organized

- `http_server.py` turns HTTP requests into service calls and turns results into HTTP responses.
- `TaskService` decides what should happen to a task.
- `TaskStorage` saves, finds, lists, and deletes tasks.
- `Task` is the Pydantic model returned by the API.
