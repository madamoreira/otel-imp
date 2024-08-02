import random
import time
from fastapi import APIRouter, Request, Response


cookies_router = APIRouter(prefix="/api")

@cookies_router.post("/cookies", status_code=201)
def create_cookie(request: Request):
    print(request)

@cookies_router.get("/cookies", status_code=200)
def fetch_cookies(request: Request):
    print(request)

@cookies_router.get("/cpu_task")
async def cpu_task():
    for i in range(1000):
        _ = i * i * i
    # logging.error("cpu task")
    return "CPU bound task finish!"


@cookies_router.get("/random_status")
async def random_status(response: Response):
    response.status_code = random.choice([200, 200, 300, 400, 500])
    # logging.error("random status")
    return {"path": "/random_status"}


@cookies_router.get("/random_sleep")
async def random_sleep(response: Response):
    time.sleep(random.randint(0, 5))
    # logging.error("random sleep")
    return {"path": "/random_sleep"}


@cookies_router.get("/error_test")
async def error_test(response: Response):
    # logging.error("got error!!!!")
    raise ValueError("value error")
