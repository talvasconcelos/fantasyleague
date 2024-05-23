import asyncio

from fastapi import APIRouter
from lnbits.db import Database
from lnbits.tasks import create_permanent_unique_task
from loguru import logger

db = Database("ext_fantasyleague")

scheduled_tasks: list[asyncio.Task] = []

fantasyleague_ext: APIRouter = APIRouter(
    prefix="/fantasyleague", tags=["fantasyleague"]
)

fantasyleague_static_files = [
    {
        "path": "/fantasyleague/static",
        "name": "fantasyleague_static",
    }
]

from .tasks import wait_for_paid_invoices
from .views import fantasyleague_ext_generic
from .views_api import fantasyleague_ext_api

fantasyleague_ext.include_router(fantasyleague_ext_generic)
fantasyleague_ext.include_router(fantasyleague_ext_api)

from .scheduler import FantasyLeagueScheduler

scheduler = FantasyLeagueScheduler()


def fantasyleague_stop():
    for task in scheduled_tasks:
        try:
            task.cancel()
        except Exception as ex:
            logger.warning(ex)


def fantasyleague_start():
    async def start_scheduler():
        await asyncio.sleep(10)
        await scheduler.run_forever()

    task_1 = create_permanent_unique_task("ext_fantasyleague", wait_for_paid_invoices)
    task_2 = create_permanent_unique_task("fantasyleague_scheduler", start_scheduler)
    scheduled_tasks.extend([task_1, task_2])
