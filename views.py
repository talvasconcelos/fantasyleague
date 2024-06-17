import json

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from lnbits.core.models import User
from lnbits.decorators import check_admin, check_user_exists
from lnbits.helpers import template_renderer
from loguru import logger

from .crud import (
    get_active_leagues,
    get_league,
    get_participant,
    get_participant_competitions,
    get_participant_team,
    get_settings,
)

fantasyleague_ext_generic = APIRouter(tags=["fantasyleague"])


@fantasyleague_ext_generic.get(
    "/", description="fantasyleague generic endpoint", response_class=HTMLResponse
)
async def index(
    request: Request,
    user: User = Depends(check_user_exists),
):
    competitions = await get_active_leagues()
    wallet_ids = [wallet.id for wallet in user.wallets]
    user_competitions = await get_participant_competitions(wallet_ids)
    logger.debug(f"User competitions: {user_competitions}")
    return template_renderer(["fantasyleague/templates"]).TemplateResponse(
        request,
        "fantasyleague/index.html",
        {
            "user": user.dict(),
            "competitions": [competition.dict() for competition in competitions],
            "user_competitions": [p.dict() for p in user_competitions],
        },
    )


@fantasyleague_ext_generic.get(
    "/admin", description="fantasyleague admin endpoint", response_class=HTMLResponse
)
async def admin(
    request: Request,
    user: User = Depends(check_admin),
):
    # competitions = mock_competitions
    # competitions = await get_competitions()

    return template_renderer(["fantasyleague/templates"]).TemplateResponse(
        request,
        "fantasyleague/admin.html",
        {"user": user.dict()},
    )


@fantasyleague_ext_generic.get(
    "/{participant_id}",
    description="fantasyleague competition endpoint",
    response_class=HTMLResponse,
)
async def competition(
    request: Request,
    participant_id: str,
    user: User = Depends(check_user_exists),
):
    participant = await get_participant(participant_id)
    assert participant, "Participant not found"

    league = await get_league(participant.fantasyleague_id)
    assert league, "League not found"
    team = [p.dict() for p in await get_participant_team(participant_id)]
    return template_renderer(["fantasyleague/templates"]).TemplateResponse(
        request,
        "fantasyleague/competition.html",
        {
            "user": user.dict(),
            "participant": participant.dict(),
            "league": league.dict(),
            "team": team,
        },
    )
