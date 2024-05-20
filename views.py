from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from lnbits.core.models import User
from lnbits.decorators import check_user_exists
from lnbits.helpers import template_renderer

from . import football_data

fantasyleague_ext_generic = APIRouter(tags=["fantasyleague"])


@fantasyleague_ext_generic.get(
    "/", description="fantasyleague generic endpoint", response_class=HTMLResponse
)
async def index(
    request: Request,
    user: User = Depends(check_user_exists),
):
    competitions = await football_data.get_competitions()
    return template_renderer(["fantasyleague/templates"]).TemplateResponse(
        request,
        "fantasyleague/index.html",
        {"user": user.dict(), "competitions": competitions},
    )
