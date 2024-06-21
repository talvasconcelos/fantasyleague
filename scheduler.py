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
from .models import FantasyLeague, Player
from .services import pay_matchday_reward, pay_rewards_overall


class FantasyLeagueScheduler:
    def __init__(self, interval_hours=6):
        self.interval_hours = interval_hours
        # self.interval_hours = 1 #interval_hours
        self.now = datetime.now(timezone.utc)
        self.next_run_time = self.now + timedelta(hours=self.interval_hours)
        self.running = False

    async def run_forever(self):
        logger.debug("FantasyLeagueScheduler started.")
        self.running = True
        await self.collect_and_process_data()
        while self.running:
            try:
                self.now = datetime.now(timezone.utc)
                logger.debug(f"Will run: {self.now >= self.next_run_time}")
                if self.now >= self.next_run_time:
                    self.next_run_time = self.now + timedelta(hours=self.interval_hours)
                    await self.collect_and_process_data()
                # await asyncio.sleep(60 * 15)  # Testing
                await asyncio.sleep(60 * 60 * 2)  # Check every 2 hour
            except Exception as ex:
                logger.warning(ex)
                # await asyncio.sleep(60)  # Wait a bit before retrying
                continue

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
            # logger.debug(f"Player IDs: {player_ids}")
            players = await get_players_by_api_id(player_ids)
            # logger.debug(f"Players: {players}")
            await self.update_participants_total_points(players, points)
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
        logger.debug(f"Points: {points}")
        for player_id, score in points.items():
            # Update player points in the database (cumulative points for the season)
            await update_player_points(player_id, score)
        return points

    async def update_participants_total_points(self, players: list[Player], points):
        # Replace with actual function to update participants' total points
        logger.info("Updating participants' total points...")
        participants = await get_participants_by_players([player.id for player in players])
        logger.debug(f"Participants: {participants}")
        for participant in participants:
            # Only players in the lineup's starting eleven are considered for points
                        
            if not participant.lineup:
                logger.warning(f"Participant {participant.id} has no lineup.")
                continue
            participant_lineup = participant.lineup.split(",")[:-4]
            participant_team = [player for player in players if player.id in participant_lineup]
            
            # Sum the points of all players in the participant's lineup, for the current matchday
            total_points = sum([points[player.api_id] for player in participant_team])
            logger.info(f"Participant {participant.id} total points: {total_points}")
            
            # Update the participant's total points (cumulative points for the season)
            await update_participant_points(participant.id, points=total_points)

    # async def update_participants_total_points(self, player_ids: list[str], points):
    #     # Replace with actual function to update participants' total points
    #     logger.info("Updating participants' total points...")
    #     participants = await get_participants_by_players(player_ids)
    #     for participant in participants:
    #         participant_team = await get_participant_team(participant.id)
    #         total_points = sum([player.points for player in participant_team])
    #         await update_participant_points(participant.id, points=total_points)

    # async def check_competitions(self, league: FantasyLeague):
    #     # Replace with actual function to check if competitions are over and distribute prizes
    #     logger.info("Checking competitions and distributing prizes...")
    #     participants = await get_participants(league.id)
    #     league_type = league.competition_type

    #     if league.season_end < self.now.strftime("%Y-%m-%d"):
    #         # league has ended
    #         await update_league(league.id, has_ended=True)
    #         logger.info("League has ended.")
    #         # distribute prizes
    #         winners = sorted(participants, key=lambda x: x.total_points, reverse=True)[
    #             :3
    #         ]
    #         await pay_rewards_overall(league.id, winners)
    #     else:
    #         # Upddate matchday
    #         matchday = await get_round(
    #             self.api_key, league.competition_code, league.season, current=False
    #         )
    #         logger.debug(f"Matchday: {matchday}")
    #         # matchday is a list of matchaday strings, check if there's a matchday next to the current one
    #         # get index of current matchday, add 1 to get next matchday
    #         next_matchday = matchday[matchday.index(league.matchday) + 1] or matchday[0]
    #         logger.debug(f"Next matchday: {next_matchday}")
    #         await update_league(league.id, matchday=next_matchday)

    #         if(league_type == "Cup"):
    #             is_group_stage = next_matchday.startswith("Group")


    #         logger.info("League still running.")
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
            winners = sorted(participants, key=lambda x: x.total_points, reverse=True)[:3]
            await pay_rewards_overall(league.id, winners)
        else:
            # Update matchday
            matchday = await get_round(self.api_key, league.competition_code, league.season, current=False)
            logger.debug(f"Matchday: {matchday}")
            
            # matchday is a list of matchday strings, check if there's a matchday next to the current one
            try:
                current_index = matchday.index(league.matchday)
                next_matchday_index = current_index + 1
                next_matchday = matchday[next_matchday_index] if next_matchday_index < len(matchday) else None
            except ValueError:
                logger.error("Current matchday not found in matchdays list.")
                return
            except IndexError:
                next_matchday = None
            
            if next_matchday:
                logger.debug(f"Next matchday: {next_matchday}")
                await update_league(league.id, matchday=next_matchday)

                if league_type == "Cup":
                    is_group_stage = next_matchday.startswith("Group")
                    remaining_group_stages = any(md.startswith("Group") for md in matchday[next_matchday_index + 1:])

                    if is_group_stage and not remaining_group_stages:
                        logger.info("End of group stage reached.")
                        # Distribute group stage rewards
                        group_stage_winner = sorted(participants, key=lambda x: x.total_points, reverse=True)[0]
                        logger.debug(f"Group stage winner: {group_stage_winner}")
                        await pay_matchday_reward(league.id, group_stage_winner, "group_stage_winner")
                        # await pay_group_stage_rewards(league.id, group_stage_winners)
                    elif is_group_stage and remaining_group_stages:
                        logger.debug("Group stage not ended yet.")
                        # Do nothing, waiting for the end of the group stages
                        pass
                    else:
                        # This is for Cup competitions that are not in the group stage
                        logger.info("Cup competition outside of group stage.")
                        # Distribute regular matchday rewards
                        matchday_winner = sorted(participants, key=lambda x: x.total_points, reverse=True)[0]
                        logger.debug(f"Matchday winner: {matchday_winner}")
                        await pay_matchday_reward(league.id, matchday_winner, f"{league.matchday} winner")
                        # await pay_matchday_rewards(league.id, matchday_winners)
                else:
                    # Regular league: Distribute matchday rewards
                    matchday_winner = sorted(participants, key=lambda x: x.total_points, reverse=True)[0]
                    logger.debug(f"Matchday winner: {matchday_winner}")
                    await pay_matchday_reward(league.id, matchday_winner)
                    # await pay_matchday_rewards(league.id, matchday_winners)

                logger.info("League still running.")
            else:
                logger.warning("No next matchday found. The league may have completed all known matchdays.")
                return

            logger.info("League still running.")

    async def stop(self):
        self.running = False
        logger.info("FantasyLeagueScheduler stopped.")

# [1145517, 1189848]