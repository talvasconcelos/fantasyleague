from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from lnbits.core.models import User
from lnbits.decorators import check_user_exists, check_admin
from lnbits.helpers import template_renderer

from .api_football import get_competitions
from .crud import get_active_leagues

fantasyleague_ext_generic = APIRouter(tags=["fantasyleague"])

mock_competitions = [
    {
        "id": 2013,
        "area": {
            "id": 2032,
            "name": "Brazil",
            "code": "BRA",
            "flag": "https://crests.football-data.org/764.svg",
        },
        "name": "Campeonato Brasileiro Série A",
        "code": "BSA",
        "type": "LEAGUE",
        "emblem": "https://crests.football-data.org/bsa.png",
        "plan": "TIER_ONE",
        "currentSeason": {
            "id": 2257,
            "startDate": "2024-04-13",
            "endDate": "2024-12-08",
            "currentMatchday": 7,
            "winner": None,
        },
        "numberOfAvailableSeasons": 8,
        "lastUpdated": "2024-05-08T14:08:14Z",
    },
    {
        "id": 2001,
        "area": {
            "id": 2077,
            "name": "Europe",
            "code": "EUR",
            "flag": "https://crests.football-data.org/EUR.svg",
        },
        "name": "UEFA Champions League",
        "code": "CL",
        "type": "CUP",
        "emblem": "https://crests.football-data.org/CL.png",
        "plan": "TIER_ONE",
        "currentSeason": {
            "id": 1630,
            "startDate": "2023-09-19",
            "endDate": "2024-06-01",
            "currentMatchday": 6,
            "winner": None,
        },
        "numberOfAvailableSeasons": 44,
        "lastUpdated": "2022-03-20T09:20:44Z",
    },
    {
        "id": 2018,
        "area": {
            "id": 2077,
            "name": "Europe",
            "code": "EUR",
            "flag": "https://crests.football-data.org/EUR.svg",
        },
        "name": "European Championship",
        "code": "EC",
        "type": "CUP",
        "emblem": "https://crests.football-data.org/ec.png",
        "plan": "TIER_ONE",
        "currentSeason": {
            "id": 1537,
            "startDate": "2024-06-14",
            "endDate": "2024-07-14",
            "currentMatchday": 1,
            "winner": None,
        },
        "numberOfAvailableSeasons": 17,
        "lastUpdated": "2024-05-08T14:14:52Z",
    },
    {
        "id": 2019,
        "area": {
            "id": 2114,
            "name": "Italy",
            "code": "ITA",
            "flag": "https://crests.football-data.org/784.svg",
        },
        "name": "Serie A",
        "code": "SA",
        "type": "LEAGUE",
        "emblem": "https://crests.football-data.org/SA.png",
        "plan": "TIER_ONE",
        "currentSeason": {
            "id": 1600,
            "startDate": "2023-08-19",
            "endDate": "2024-05-26",
            "currentMatchday": 37,
            "winner": None,
        },
        "numberOfAvailableSeasons": 92,
        "lastUpdated": "2022-03-20T09:16:43Z",
    },
    {
        "id": 2152,
        "area": {
            "id": 2220,
            "name": "South America",
            "code": "SAM",
            "flag": "https://crests.football-data.org/CLI.svg",
        },
        "name": "Copa Libertadores",
        "code": "CLI",
        "type": "CUP",
        "emblem": "https://crests.football-data.org/CLI.svg",
        "plan": "TIER_ONE",
        "currentSeason": {
            "id": 1644,
            "startDate": "2024-02-07",
            "endDate": "2024-05-31",
            "currentMatchday": 6,
            "winner": None,
        },
        "numberOfAvailableSeasons": 4,
        "lastUpdated": "2023-03-16T16:22:43Z",
    },
    {
        "id": 2014,
        "area": {
            "id": 2224,
            "name": "Spain",
            "code": "ESP",
            "flag": "https://crests.football-data.org/760.svg",
        },
        "name": "Primera Division",
        "code": "PD",
        "type": "LEAGUE",
        "emblem": "https://crests.football-data.org/PD.png",
        "plan": "TIER_ONE",
        "currentSeason": {
            "id": 1577,
            "startDate": "2023-08-13",
            "endDate": "2024-05-26",
            "currentMatchday": 37,
            "winner": None,
        },
        "numberOfAvailableSeasons": 93,
        "lastUpdated": "2022-03-20T09:20:08Z",
    },
]


@fantasyleague_ext_generic.get(
    "/admin", description="fantasyleague admin endpoint", response_class=HTMLResponse
)
async def admin(
    request: Request,
    user: User = Depends(check_admin),
):
    competitions = mock_competitions  # await get_competitions()

    return template_renderer(["fantasyleague/templates"]).TemplateResponse(
        request,
        "fantasyleague/admin.html",
        {"user": user.dict(), "competitions": competitions},
    )


@fantasyleague_ext_generic.get(
    "/", description="fantasyleague generic endpoint", response_class=HTMLResponse
)
async def index(
    request: Request,
    user: User = Depends(check_user_exists),
):
    competitions = await get_active_leagues()
    return template_renderer(["fantasyleague/templates"]).TemplateResponse(
        request,
        "fantasyleague/index.html",
        {
            "user": user.dict(),
            "competitions": [competition.dict() for competition in competitions],
        },
    )
