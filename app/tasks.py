from celery import Celery
from pyppeteer import launch
import asyncio
import os
import redis


redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

celery_app = Celery('tasks', broker='redis://redis:6379/0')

async def capture_page(url, task_id):
    os.makedirs("screenshots", exist_ok=True)
    browser = await launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
    page = await browser.newPage()
    await page.goto(url)
    screenshot_path = f"/app/screenshots/{task_id}.png"
    await page.screenshot({'path': screenshot_path})
    await browser.close()
    return screenshot_path

@celery_app.task(name="tasks.capture_screenshot")
def capture_screenshot(url, task_id):
    task_key = f"task:{task_id}"
    try:
        redis_client.set(task_key, "processing")
        loop = asyncio.get_event_loop()
        screenshot_path = loop.run_until_complete(capture_page(url, task_id))
        redis_client.set(task_key, f"completed:{screenshot_path}")
        return {"status": "completed", "screenshot_path": screenshot_path}
    except Exception as e:
        redis_client.set(task_key, f"failed:{str(e)}")
        return {"status": "failed", "error": str(e)}