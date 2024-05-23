import datetime

import httpx

from loguru import logger

BASE_URL = "https://api.football-data.org/v4/"


def _get_headers(api_key: str):
    return {
        "X-Auth-Token": api_key,
        "Content-Type": "application/json",
    }


async def get_competitions():
    client = httpx.AsyncClient(base_url=BASE_URL)

    try:
        response = await client.get("competitions")
        r = response.json()
        today = datetime.date.today()

        eligible_competitions = []
        for competition in r["competitions"]:
            if competition["plan"] != "TIER_ONE":
                continue
            end_date = datetime.datetime.strptime(
                competition["currentSeason"]["endDate"], "%Y-%m-%d"
            ).date()
            if today < end_date:
                eligible_competitions.append(competition)

        return eligible_competitions
    except httpx.HTTPStatusError as exc:
        return exc.response.json()


async def get_teams(api_key: str, competition_code: str):
    client = httpx.AsyncClient(base_url=BASE_URL, headers=_get_headers(api_key))

    try:
        response = await client.get(f"competitions/{competition_code}/teams")
        return response.json()["teams"]
    except httpx.HTTPStatusError as exc:
        return exc.response.json()


async def get_players(api_key: str, league_id: str, competition_code: str):
    teams = await get_teams(api_key, competition_code)
    players = []
    for team in teams:
        squad = team["squad"]
        for player in squad:
            players.append(
                {
                    "api_id": player["id"],
                    "league_id": league_id,
                    "name": player["name"],
                    "position": player["position"],
                    "team": team["name"],
                }
            )
    return players


async def get_matches(api_key: str, competition_code: str, matchday: int):
    client = httpx.AsyncClient(base_url=BASE_URL, headers=_get_headers(api_key))

    try:
        response = await client.get(
            f"competitions/{competition_code}/matches?matchday={matchday}"
        )
        r = response.json()
        # logger.debug(r)
        all_matches_played = r["resultSet"]["count"] == r["resultSet"]["played"]
        if not all_matches_played:
            return None
        return r["matches"]
    except httpx.HTTPStatusError as exc:
        return exc.response.json()
