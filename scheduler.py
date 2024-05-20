import asyncio
from datetime import datetime, timedelta, timezone

from loguru import logger

from . import football_data
from .crud import (
    get_league,
    get_participants,
    get_participant_team,
    get_participants_by_players,
    update_league,
    update_participant_points,
    update_player_points,
)
from .helpers import calculate_player_points


class FantasyLeagueScheduler:
    def __init__(self, interval_hours=12):
        self.interval_hours = interval_hours
        self.next_run_time = self.now + timedelta(hours=self.interval_hours)
        self.running = False

    async def run_forever(self):
        self.running = True
        while self.running:
            try:
                self.now = datetime.now(timezone.utc)
                if self.now >= self.next_run_time:
                    self.next_run_time = self.now + timedelta(hours=self.interval_hours)
                    await self.collect_and_process_data()
                await asyncio.sleep(60 * 60 * 4)  # Check every 4 hours
            except Exception as ex:
                logger.warning(ex)
                await asyncio.sleep(60)  # Wait a bit before retrying

    async def collect_and_process_data(self, league_id=None):
        if not league_id:
            return
        logger.info("Collecting data and processing...")
        self.league = await get_league(league_id)
        if not self.league:
            logger.error("League not found.")
            return
        matches = await self.fetch_data(
            competition=self.league.competition_code, matchday=self.league.matchday
        )
        if matches is None:
            logger.info("Not all matches played yet.")
            return

        points = await self.calculate_points(matches)
        player_ids = list(points.keys())
        await self.update_participants_total_points(player_ids)
        await self.check_competitions()

    async def fetch_data(self, competition, matchday=1):
        # Replace with actual function to fetch data from the API
        logger.info("Fetching data from API...")
        return await football_data.get_matches(competition, matchday)

    async def calculate_points(self, matches):
        # Replace with actual function to calculate player points
        logger.info("Calculating player points...")
        points = calculate_player_points(matches)
        for player_id, score in points.items():
            # Update player points in the database
            await update_player_points(player_id, score)
        return points

    async def update_participants_total_points(self, player_ids: list):
        # Replace with actual function to update participants' total points
        logger.info("Updating participants' total points...")
        participants = await get_participants_by_players(player_ids)
        for participant in participants:
            participant_team = await get_participant_team(participant.id)
            total_points = sum([player.points for player in participant_team])
            await update_participant_points(participant.id, points=total_points)

    async def check_competitions(self):
        # Replace with actual function to check if competitions are over and distribute prizes
        logger.info("Checking competitions and distributing prizes...")
        assert self.league
        participants = await get_participants(self.league.id)
        league_type = self.league.competition_type

        if self.league.season_end < self.now.strftime("%Y-%m-%d"):
            # league has ended
            await update_league(self.league.id, has_ended=True)
            logger.info("League has ended.")
            # distribute prizes
            winners = sorted(participants, key=lambda x: x.total_points, reverse=True)[
                :3
            ]

            return
        # check what competition type it is, check what stage it's in and distribute prizes accordingly
        if league_type == "CUP":
            calculate_rewards(participants, league_type, "matchday")
        elif league_type == "LEAGUE":
            # distribute prizes for head to head league
            pass
        else:
            logger.error("Unknown competition type.")

    async def stop(self):
        self.running = False
        logger.info("FantasyLeagueScheduler stopped.")
