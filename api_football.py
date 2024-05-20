import httpx
import asyncio
import datetime
from typing import Optional
from .models import CreatePlayer, Players

BASE_URL = "https://api.football-data.org/v4/"


class FootballData:
    def __init__(self):
        self.api_key: Optional[str] = None
        self.headers = {
            "X-Auth-Token": self.api_key,
            "Content-Type": "application/json",
        }
        self.client = httpx.AsyncClient(base_url=BASE_URL, headers=self.headers)

    def _add_api_key(self, key):
        self.api_key = key
        self.headers["X-Auth-Token"] = self.api_key

    async def get_competitions(self):
        eligible_competitions = []

        try:
            response = await self.client.get("competitions")
            r = response.json()
            today = datetime.date.today()

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

    async def _get_teams(self, competition_code):
        try:
            response = await self.client.get(f"competitions/{competition_code}/teams")
            return response.json()["teams"]
        except httpx.HTTPStatusError as exc:
            return exc.response.json()

    async def get_players(self, league_id) -> Players:
        teams = await self._get_teams(competition_code="PL")
        players = []
        for team in teams:
            squad = team["squad"]
            for player in squad:
                players.append(
                    CreatePlayer(
                        api_id=player["id"],
                        league_id=league_id,
                        name=player["name"],
                        position=player["position"],
                        team=team["name"],
                    )
                )
        return Players(players=players)

    async def get_matches(self, competition_code: str, matchday: int):
        try:
            response = await self.client.get(
                f"competitions/{competition_code}/matches?matchday={matchday}"
            )
            r = response.json()
            all_matches_played = r["resultSet"]["count"] == r["resultSet"]["played"]
            if not all_matches_played:
                return None
            return r["matches"]
        except httpx.HTTPStatusError as exc:
            return exc.response.json()
