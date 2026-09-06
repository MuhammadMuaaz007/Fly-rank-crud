from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Task API",
    description="A simple in-memory CRUD API for managing to-do tasks.",
    version="1.0",
)

# In-memory "database" — 3 starter tasks
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Read a book",   "done": True},
    {"id": 3, "title": "Go for a walk", "done": False},
]

next_id = 4  # increments with every new task


# --- Request body models ---
class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


# Helper: find a task by id or raise 404
def find_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})


# --- Meta endpoints ---

@app.get("/", tags=["Meta"], summary="API info")
def root():
    """Returns the API name, version, and available endpoints."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health", tags=["Meta"], summary="Health check")
def health():
    """Returns ok when the server is alive. Used by monitoring tools."""
    return {"status": "ok"}


# --- Task endpoints ---

@app.get("/tasks", tags=["Tasks"], summary="List all tasks")
def list_tasks():
    """Return every task in the in-memory list."""
    return tasks


@app.get("/tasks/{task_id}", tags=["Tasks"], summary="Get one task")
def get_task(task_id: int):
    """Return a single task by id. Returns 404 if not found."""
    return find_task(task_id)


@app.post("/tasks", status_code=201, tags=["Tasks"], summary="Create a task")
def create_task(body: TaskCreate):
    """
    Create a new task.
    - **title** is required and must not be blank → 400 if empty, 422 if missing.
    - Returns the created task with status **201**.
    """
    global next_id

    if not body.title.strip():
        raise HTTPException(status_code=400, detail={"error": "title must not be empty"})

    new_task = {"id": next_id, "title": body.title.strip(), "done": False}
    tasks.append(new_task)
    next_id += 1
    return new_task


@app.put("/tasks/{task_id}", tags=["Tasks"], summary="Update a task")
def update_task(task_id: int, body: TaskUpdate):
    """
    Update a task's **title** and/or **done** status.
    - Send at least one field → 400 if body is empty.
    - Returns 404 if the task doesn't exist.
    """
    if body.title is None and body.done is None:
        raise HTTPException(status_code=400, detail={"error": "send at least one of: title, done"})

    if body.title is not None and not body.title.strip():
        raise HTTPException(status_code=400, detail={"error": "title must not be empty"})

    task = find_task(task_id)

    if body.title is not None:
        task["title"] = body.title.strip()
    if body.done is not None:
        task["done"] = body.done

    return task


@app.delete("/tasks/{task_id}", status_code=204, tags=["Tasks"], summary="Delete a task")
def delete_task(task_id: int):
    """
    Delete a task by id.
    - Returns **204 No Content** on success.
    - Returns 404 if the task doesn't exist.
    """
    task = find_task(task_id)
    tasks.remove(task)
