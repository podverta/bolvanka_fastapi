import os
from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import redis
from fastapi.staticfiles import StaticFiles

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

from tasks import celery_app

if not os.path.exists("screenshots"):
    os.makedirs("screenshots")
app = FastAPI()
app.mount("/app/screenshots", StaticFiles(directory="screenshots"), name="screenshots")


class ScreenshotRequest(BaseModel):
    url: str

@app.get("/")
async def get_all_tasks():
    task_keys = redis_client.keys("task:*")
    tasks = {}
    for key in task_keys:
        tasks[key] = redis_client.get(key)
    return tasks


@app.post("/screenshot/")
async def create_screenshot_task(request: ScreenshotRequest):
    task_id = str(uuid.uuid4())
    task_key = f"task:{task_id}"
    redis_client.set(task_key, "pending")
    celery_app.send_task('tasks.capture_screenshot', args=[request.url, task_id])
    return {"task_id": task_id}


@app.get("/screenshot/{task_id}")
async def get_screenshot_status(task_id: str):
    task_key = f"task:{task_id}"
    status = redis_client.get(task_key)
    if not status:
        return {"error": "Task not found"}
    return {"status": status}
