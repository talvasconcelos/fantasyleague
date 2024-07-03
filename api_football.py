import asyncio
import datetime
import re
import time

import httpx
from loguru import logger

from .mock_leagues import mock_competitions, mock_players  # just for testing

BASE_URL = "https://v3.football.api-sports.io/"


def _get_headers(api_key: str):
    return {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "v3.football.api-sports.io",
    }


def _get_sleep_time(response: httpx.Response):
    rate_limit = int(response.headers.get("X-RateLimit-Limit", 10))
    remaining = int(response.headers.get("X-RateLimit-Remaining", 0))
    r = response.json()
    if r["paging"]["total"] < 6 and remaining > 0:
        return 0
    
    if remaining == 0:
        cool_off_seconds = 60  # Cool off for one minute
        logger.debug(f"Rate limit reached. Cooling off for {cool_off_seconds} seconds.")
        return cool_off_seconds
    else:
        # Calculate the sleep time based on remaining requests
        sleep_time = max(60 / rate_limit, 1)
        logger.debug(f"Sleeping for {sleep_time} seconds before fetching next page")
        return sleep_time


async def get_competition(api_key: str, competition_code: str):
    client = httpx.AsyncClient(base_url=BASE_URL, headers=_get_headers(api_key))

    try:
        response = await client.get(f"competitions/{competition_code}")
        return response.json()
    except httpx.HTTPStatusError as exc:
        return exc.response.json()


async def get_competitions(api_key: str):
    client = httpx.AsyncClient(base_url=BASE_URL, headers=_get_headers(api_key))
    try:
        if mock_competitions:
            r = mock_competitions["response"]
            logger.debug("Using mock competitions")
        else:
            response = await client.get("leagues?current=true")
            r = response.json()["response"]
        today = datetime.date.today()
        eligible_competitions = []
        for competition in r:
            season = competition["seasons"][0]
            coverage = season["coverage"]
            if (
                not coverage["players"]
                # or not coverage["fixtures"]["statistics_players"]
                # or not coverage["fixtures"]["lineups"]
            ):
                continue
            end_date = datetime.datetime.strptime(season["end"], "%Y-%m-%d").date()

            # if competition["league"]["type"] != "Cup" and (end_date - today).days < 30:
            # if (end_date - today).days < 15:
            #     continue
            if today < end_date:
                eligible_competitions.append(competition)

        return eligible_competitions
    except httpx.HTTPStatusError as exc:
        return exc.response.json()


async def get_round(api_key: str, competition_code: str, season: int, current=True):
    client = httpx.AsyncClient(base_url=BASE_URL, headers=_get_headers(api_key))

    try:
        response = await client.get(
            f"fixtures/rounds?league={competition_code}&season={season}{'' if not current else '&current=true'}"
        )
        r = response.json()
        return r["response"]
    except httpx.HTTPStatusError as exc:
        return exc.response.json()


async def get_league_players(
    api_key: str, league_id: str, competition_code: str, season: int
):
    client = httpx.AsyncClient(base_url=BASE_URL, headers=_get_headers(api_key))

    players = []
    page = 1
    while True:
        logger.debug(f"Fetching players page {page}")
        try:
            response = await client.get(
                f"players?league={competition_code}&season={season}&page={page}"
            )
            r = response.json()
            players.extend(r["response"])
            logger.debug(f"Players: {len(players)}")
            logger.debug(
                f"Current page: {r['paging']['current']} of {r['paging']['total']}"
            )

            await asyncio.sleep(_get_sleep_time(response))

            if int(r["paging"]["current"]) == int(r["paging"]["total"]):
                logger.debug("All players fetched")
                break
            page += 1
        except httpx.HTTPStatusError as exc:
            logger.error(f"{exc.response.json()}")
        except httpx.RequestError as exc:
            logger.error(f"Request error: {exc}")
            # return {"error": str(exc)}
    return [
        {
            "api_id": player["player"]["id"],
            "league_id": league_id,
            "name": player["player"]["name"],
            "position": player["statistics"][0]["games"]["position"],
            "team": player["statistics"][0]["team"]["name"],
            "photo": player["player"]["photo"],
        }
        for player in players
    ]


async def get_matches(api_key: str, competition_code: str, season: int, matchday: str):
    client = httpx.AsyncClient(base_url=BASE_URL, headers=_get_headers(api_key))

    try:
        response = await client.get(
            f"fixtures?league={competition_code}&season={season}&round={matchday}"
        )
        r = response.json()
        # logger.debug(r)
        all_matches_played = all(
            match["fixture"]["status"]["short"] in ["FT", "AET", "PEN", "PST", "CANC"]
            for match in r["response"]
        )

        logger.debug(f"All matches played: {all_matches_played}")
        if not all_matches_played:
            return []

        return [match["fixture"]["id"] for match in r["response"]]
    except httpx.HTTPStatusError as exc:
        return exc.response.json()

async def get_first_match(api_key: str, competition_code: str, season: int, matchday: str):
    client = httpx.AsyncClient(base_url=BASE_URL, headers=_get_headers(api_key))

    try:
        response = await client.get(
            f"fixtures?league={competition_code}&season={season}&round={matchday}"
        )
        r = response.json()

        # Get the start time of the first fixture
        first_fixture = min(r["response"], key=lambda x: x['fixture']['timestamp'], default=r["response"][0]["fixture"]["timestamp"])
        first_fixture_start = int(first_fixture['fixture']['timestamp'])

        return first_fixture_start
    except httpx.HTTPStatusError as exc:
        return exc.response.json()


async def get_player_stats_by_match(api_key: str, match_ids: list[int]):
    client = httpx.AsyncClient(base_url=BASE_URL, headers=_get_headers(api_key))

    stats = []
    for match_id in match_ids:
        try:
            response = await client.get(f"fixtures/players?fixture={match_id}")
            r = response.json()
            for _ in r["response"]:
                stats.extend(_["players"])

            # account for rate limiting, 10 calls per minute
            await asyncio.sleep(_get_sleep_time(response))

        except httpx.HTTPStatusError as exc:
            return exc.response.json()

    return stats


async def get_teams(api_key: str, competition_code: str, season: int):
    client = httpx.AsyncClient(base_url=BASE_URL, headers=_get_headers(api_key))

    try:
        response = await client.get(f"teams?league={competition_code}&season={season}")
        r = response.json()
        return r["response"]
    except httpx.HTTPStatusError as exc:
        return exc.response.json()


async def get_team_players(api_key: str, team_ids: list[int], league_id: str):
    client = httpx.AsyncClient(base_url=BASE_URL, headers=_get_headers(api_key))

    players = []
    for team_id in team_ids:
        try:
            response = await client.get(f"players/squads?team={team_id}")
            r = response.json()
            team = r["response"][0]["team"]["name"]
            for player in r["response"][0]["players"]:
                players.append(
                    {
                        "api_id": player["id"],
                        "league_id": league_id,
                        "name": player["name"],
                        "position": player["position"],
                        "team": team,
                        "photo": player["photo"],
                    }
                )
            # players.extend(r["response"]["players"])
            await asyncio.sleep(_get_sleep_time(response))
        except httpx.HTTPStatusError as exc:
            return exc.response.json()

    return players
