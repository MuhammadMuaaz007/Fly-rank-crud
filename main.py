from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

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


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return find_task(task_id)


@app.post("/tasks", status_code=201)
def create_task(body: TaskCreate):
    global next_id

    if not body.title.strip():
        raise HTTPException(status_code=400, detail={"error": "title must not be empty"})

    new_task = {"id": next_id, "title": body.title.strip(), "done": False}
    tasks.append(new_task)
    next_id += 1
    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, body: TaskUpdate):
    # Must send at least one field
    if body.title is None and body.done is None:
        raise HTTPException(status_code=400, detail={"error": "send at least one of: title, done"})

    # title cannot be blank if provided
    if body.title is not None and not body.title.strip():
        raise HTTPException(status_code=400, detail={"error": "title must not be empty"})

    task = find_task(task_id)

    if body.title is not None:
        task["title"] = body.title.strip()
    if body.done is not None:
        task["done"] = body.done

    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    task = find_task(task_id)
    tasks.remove(task)
