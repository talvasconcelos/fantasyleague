import asyncio

from fastapi import APIRouter
from lnbits.db import Database
from lnbits.tasks import create_permanent_unique_task
from loguru import logger

from .tasks import wait_for_paid_invoices
from .views import fantasyleague_ext_generic
from .views_api import fantasyleague_ext_api
from .api_football import FootballData

db = Database("ext_fantasyleague")

scheduled_tasks: list[asyncio.Task] = []

fantasyleague_ext: APIRouter = APIRouter(
    prefix="/fantasyleague", tags=["fantasyleague"]
)
fantasyleague_ext.include_router(fantasyleague_ext_generic)
fantasyleague_ext.include_router(fantasyleague_ext_api)

fantasyleague_static_files = [
    {
        "path": "/fantasyleague/static",
        "name": "fantasyleague_static",
    }
]

football_data = FootballData()


def fantasyleague_stop():
    for task in scheduled_tasks:
        try:
            task.cancel()
        except Exception as ex:
            logger.warning(ex)


def fantasyleague_start():
    # ignore will be removed in lnbits `0.12.6`
    # https://github.com/lnbits/lnbits/pull/2417
    task = create_permanent_unique_task("ext_fantasyleague", wait_for_paid_invoices)  # type: ignore
    scheduled_tasks.append(task)
