import asyncio
from datetime import datetime, timedelta, timezone

from loguru import logger

from .api_football import get_matches, get_player_stats_by_match, get_round
from .crud import (
    get_active_leagues,
    get_participant_team,
    get_participants,
    get_participants_by_players,
    get_players_by_api_id,
    get_settings,
    update_league,
    update_participant_points,
    update_player_points,
)
from .helpers import calculate_player_points
from .models import FantasyLeague
from .services import pay_rewards_overall


class FantasyLeagueScheduler:
    def __init__(self, interval_hours=12):
        self.interval_hours = interval_hours
        self.now = datetime.now(timezone.utc)
        self.next_run_time = self.now + timedelta(hours=self.interval_hours)
        self.running = False

    async def run_forever(self):
        logger.debug("FantasyLeagueScheduler started.")
        self.running = True
        while self.running:
            try:
                self.now = datetime.now(timezone.utc)
                logger.debug(f"Will run: {self.now >= self.next_run_time}")
                if self.now >= self.next_run_time:
                    self.next_run_time = self.now + timedelta(hours=self.interval_hours)
                    await self.collect_and_process_data()
                # await asyncio.sleep(60 * 5)  # Testing
                await asyncio.sleep(60 * 60 * 4)  # Check every 4 hours
            except Exception as ex:
                logger.warning(ex)
                await asyncio.sleep(60)  # Wait a bit before retrying

    async def collect_and_process_data(self):
        api_key = await get_settings()
        if not api_key:
            logger.error("API key not set.")
            return
        self.api_key = api_key.api_key
        leagues = await get_active_leagues()
        logger.debug(f"Active leagues: {leagues}")
        for league in leagues:
            logger.info("Collecting data and processing...")
            assert league.matchday
            matches = await self.fetch_data(
                competition=league.competition_code,
                matchday=league.matchday,
                season=league.season,
            )
            logger.debug(f"Matches: {matches}")
            if matches is None or len(matches) == 0:
                logger.info("Not all matches played yet.")
                continue

            statistics = await get_player_stats_by_match(self.api_key, matches)
            points = await self.calculate_points(statistics)
            player_ids = list(points.keys())
            players = await get_players_by_api_id(player_ids)
            await self.update_participants_total_points([player.id for player in players])
            await self.check_competitions(league)
            # logger.info("Updating league matchday...")
            # await update_league(league.id, matchday=league.matchday + 1)

    async def fetch_data(self, competition, matchday: str, season: int):
        # Replace with actual function to fetch data from the API
        logger.info("Fetching matches from API...")
        return await get_matches(self.api_key, competition, season, matchday)

    async def calculate_points(self, stats):
        # Replace with actual function to calculate player points
        logger.info("Calculating player points...")
        points = calculate_player_points(stats)
        for player_id, score in points.items():
            # Update player points in the database
            await update_player_points(player_id, score)
        return points

    async def update_participants_total_points(self, player_ids: list[str]):
        # Replace with actual function to update participants' total points
        logger.info("Updating participants' total points...")
        participants = await get_participants_by_players(player_ids)
        for participant in participants:
            participant_team = await get_participant_team(participant.id)
            total_points = sum([player.points for player in participant_team])
            await update_participant_points(participant.id, points=total_points)

    async def check_competitions(self, league: FantasyLeague):
        # Replace with actual function to check if competitions are over and distribute prizes
        logger.info("Checking competitions and distributing prizes...")
        participants = await get_participants(league.id)
        league_type = league.competition_type

        if league.season_end < self.now.strftime("%Y-%m-%d"):
            # league has ended
            await update_league(league.id, has_ended=True)
            logger.info("League has ended.")
            # distribute prizes
            winners = sorted(participants, key=lambda x: x.total_points, reverse=True)[
                :3
            ]
            await pay_rewards_overall(league.id, winners)
        else:
            # Upddate matchday
            matchday = await get_round(
                self.api_key, league.competition_code, league.season, current=False
            )
            # matchday is a list of matchaday strings, check if there's a matchday next to the current one
            # get index of current matchday, add 1 to get next matchday
            next_matchday = matchday[matchday.index(league.matchday) + 1] or matchday[0]
            await update_league(league.id, matchday=next_matchday)

            logger.info("League still running.")

    async def stop(self):
        self.running = False
        logger.info("FantasyLeagueScheduler stopped.")
