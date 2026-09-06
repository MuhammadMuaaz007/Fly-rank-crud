# Task API

A simple in-memory CRUD API for managing to-do tasks.  
Built with **Python 3.11** and **FastAPI**.

> Data lives only in memory — restarting the server resets the list back to the 3 seed tasks.  
> This is intentional. A database (Week 3) is the fix.

---

## How to run

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 2. Install dependencies
pip install fastapi==0.115.0 "uvicorn[standard]==0.30.6"

# 3. Start the server
uvicorn main:app --reload --port 8000
```

- API: http://localhost:8000  
- Interactive docs (Swagger UI): http://localhost:8000/docs

---

## Endpoints

| Method   | Path              | Status codes    | What it does                        |
|----------|-------------------|-----------------|-------------------------------------|
| GET      | `/`               | 200             | API name, version, endpoint list    |
| GET      | `/health`         | 200             | Liveness probe → `{"status":"ok"}`  |
| GET      | `/tasks`          | 200             | List all tasks                      |
| GET      | `/tasks/{id}`     | 200, 404        | Get one task by id                  |
| POST     | `/tasks`          | 201, 400, 422   | Create a task (`title` required)    |
| PUT      | `/tasks/{id}`     | 200, 400, 404   | Update `title` and/or `done`        |
| DELETE   | `/tasks/{id}`     | 204, 404        | Delete a task                       |

---

## curl -i examples

### List all tasks
```
curl -i http://localhost:8000/tasks
```
```
HTTP/1.1 200 OK
content-type: application/json

[{"id":1,"title":"Buy groceries","done":false},{"id":2,"title":"Read a book","done":true},{"id":3,"title":"Go for a walk","done":false}]
```

### Get one task
```
curl -i http://localhost:8000/tasks/1
```
```
HTTP/1.1 200 OK
content-type: application/json

{"id":1,"title":"Buy groceries","done":false}
```

### Task not found
```
curl -i http://localhost:8000/tasks/99
```
```
HTTP/1.1 404 Not Found
content-type: application/json

{"detail":{"error":"Task 99 not found"}}
```

### Create a task
```
curl -i -X POST http://localhost:8000/tasks \
     -H "Content-Type: application/json" \
     -d '{"title":"Buy milk"}'
```
```
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

### Update a task
```
curl -i -X PUT http://localhost:8000/tasks/4 \
     -H "Content-Type: application/json" \
     -d '{"done":true}'
```
```
HTTP/1.1 200 OK
content-type: application/json

{"id":4,"title":"Buy milk","done":true}
```

### Delete a task
```
curl -i -X DELETE http://localhost:8000/tasks/4
```
```
HTTP/1.1 204 No Content
```

---

## Swagger UI

Open **http://localhost:8000/docs** after starting the server.  
Every endpoint is listed with its description and a **Try it out** button.

![Swagger UI](swagger-screenshot.png)

*(Take a screenshot of `/docs` and save it as `swagger-screenshot.png` in this folder.)*

---

## Git history

| # | Commit message |
|---|----------------|
| 1 | Stage 0: hello server |
| 2 | Stage 1: root and health endpoints |
| 3 | Stage 2: read endpoints with 404 |
| 4 | Stage 3: create with validation |
| 5 | Stage 4: full CRUD |
| 6 | Stage 5: Swagger UI |
| 7 | Stage 6: publish and docs |
