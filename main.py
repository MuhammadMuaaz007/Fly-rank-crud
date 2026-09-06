from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory "database" — 3 starter tasks
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Read a book",   "done": True},
    {"id": 3, "title": "Go for a walk", "done": False},
]

next_id = 4  # increments with every new task


# --- Request body model ---
class TaskCreate(BaseModel):
    title: str


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
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})


@app.post("/tasks", status_code=201)
def create_task(body: TaskCreate):
    global next_id

    # Validate: title must not be blank
    if not body.title.strip():
        raise HTTPException(status_code=400, detail={"error": "title must not be empty"})

    new_task = {"id": next_id, "title": body.title.strip(), "done": False}
    tasks.append(new_task)
    next_id += 1
    return new_task
