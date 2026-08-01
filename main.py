from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task API", version="1.0")

tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Finish assignment", "done": False},
    {"id": 3, "title": "Read a book", "done": True},
]
next_id = 4


class TaskCreate(BaseModel):
    title: str = ""


class TaskUpdate(BaseModel):
    title: str = ""
    done: bool = False


@app.get("/", summary="API info")
def root():
    """Basic info about this API and its available endpoints."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", summary="Health check")
def health():
    """Simple check to confirm the server is alive."""
    return {"status": "ok"}


@app.get("/tasks", summary="List all tasks")
def list_tasks():
    """Return every task currently in memory."""
    return tasks


@app.get("/tasks/{task_id}", summary="Get a single task")
def get_task(task_id: int):
    """Return one task by id, or 404 if it doesn't exist."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.post("/tasks", status_code=201, summary="Create a task")
def create_task(new_task: TaskCreate):
    """Create a new task. Requires a non-empty title."""
    global next_id
    if not new_task.title or not new_task.title.strip():
        raise HTTPException(status_code=400, detail="title is required")

    task = {"id": next_id, "title": new_task.title, "done": False}
    tasks.append(task)
    next_id += 1
    return task


@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, update: TaskUpdate):
    """Replace a task's title and done status. 404 if the task doesn't exist."""
    if not update.title or not update.title.strip():
        raise HTTPException(status_code=400, detail="title is required")

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = update.title
            task["done"] = update.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    """Remove a task by id. 404 if the task doesn't exist."""
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")