from typing import List, Optional, Union

from lnbits.helpers import urlsafe_short_hash
from loguru import logger

from . import db
from .models import (
    CreateFantasyLeague,
    CreateParticipant,
    FantasyLeague,
    Participant,
    Player,
    Players,
    Settings,
    CreatePrizeDistribution,
    PrizeDistribution,
)

## SETTINGS


async def get_settings() -> Optional[Settings]:
    row = await db.fetchone("SELECT * FROM fantasyleague.settings")
    return Settings(**row) if row else None


async def create_settings(data: Settings) -> Settings:
    await db.execute(
        """
        INSERT INTO fantasyleague.settings (api_key, first_prize, second_prize, third_prize, weekly_prize, monthly_prize, matchday_prize, finals_prize)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.api_key,
            data.first_prize,
            data.second_prize,
            data.third_prize,
            data.weekly_prize,
            data.monthly_prize,
            data.matchday_prize,
            data.finals_prize,
        ),
    )
    settings = await get_settings()
    assert settings, "Newly created settings couldn't be retrieved"
    return settings


## LEAGUES


async def get_leagues(wallet_ids: Union[str, List[str]]) -> List[FantasyLeague]:
    if isinstance(wallet_ids, str):
        wallet_ids = [wallet_ids]

    q = ",".join(["?"] * len(wallet_ids))
    rows = await db.fetchall(
        f"SELECT * FROM fantasyleague.fantasyleague WHERE wallet IN ({q})",
        (*wallet_ids,),
    )
    return [FantasyLeague(**row) for row in rows]


async def get_league(league_id: str) -> Optional[FantasyLeague]:
    row = await db.fetchone(
        "SELECT * FROM fantasyleague.fantasyleague WHERE id = ?", (league_id,)
    )
    return FantasyLeague(**row) if row else None


async def get_active_leagues():
    # get all active leagues from DB and count, if count is 0, return None
    active = await db.execute(
        "SELECT COUNT(id) FROM fantasyleague.fantasyleague WHERE has_ended = 1"
    )
    if active == 0:
        return None
    return active


async def create_league(data: CreateFantasyLeague) -> FantasyLeague:
    league_id = urlsafe_short_hash()
    await db.execute(
        """
        INSERT INTO fantasyleague.fantasyleague (id, wallet, name, description, buy_in, competition_type, competition_code, season_start, season_end)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            league_id,
            data.wallet,
            data.name,
            data.description,
            data.buy_in,
            data.competition_type,
            data.competition_code,
            data.season_start,
            data.season_end,
        ),
    )
    league = await get_league(league_id)
    assert league, "Newly created league couldn't be retrieved"
    return league


async def update_league(league_id: str, **kwargs) -> FantasyLeague:
    q = ", ".join([f"{field[0]} = ?" for field in kwargs.items()])
    await db.execute(
        f"UPDATE fantasyleague.fantasyleague SET {q} WHERE id = ?",
        (*kwargs.values(), league_id),
    )
    row = await db.fetchone(
        "SELECT * FROM fantasyleague.fantasyleague WHERE id = ?", (league_id,)
    )
    assert row, "Newly updated league couldn't be retrieved"
    return FantasyLeague(**row)


## PARTICIPANTS


async def get_participants(league_id: str) -> List[Participant]:
    rows = await db.fetchall(
        "SELECT * FROM fantasyleague.participants WHERE fantasyleague_id = ?",
        (league_id,),
    )
    return [Participant(**row) for row in rows]


async def get_all_participants() -> List[Participant]:
    rows = await db.fetchall("SELECT * FROM fantasyleague.participants")
    return [Participant(**row) for row in rows]


async def get_participant(participant_id: str) -> Optional[Participant]:
    row = await db.fetchone(
        "SELECT * FROM fantasyleague.participants WHERE id = ?", (participant_id,)
    )
    return Participant(**row) if row else None


async def create_participant(data: CreateParticipant) -> Participant:
    participant_id = urlsafe_short_hash()
    await db.execute(
        """
        INSERT INTO fantasyleague.participants (id, fantasyleague_id, wallet, name)
        VALUES (?, ?, ?, ?)
        """,
        (participant_id, data.fantasyleague_id, data.wallet, data.name),
    )
    participant = await get_participant(participant_id)
    assert participant, "Newly created participant couldn't be retrieved"
    return participant


async def get_participant_team(participant_id: str) -> List[Player]:
    rows = await db.fetchall(
        "SELECT * FROM fantasyleague.participant_players WHERE participant_id = ?",
        (participant_id,),
    )
    player_ids = [row["player_id"] for row in rows]
    return await get_players(player_ids)


async def get_participants_by_players(player_ids: List[int]) -> List[Participant]:
    q = ",".join(["?"] * len(player_ids))
    rows = await db.fetchall(
        f"""
        SELECT p.*
        FROM fantasyleague.participants p
        JOIN fantasyleague.participant_players pp ON p.id = pp.participant_id
        WHERE pp.player_id IN ({q})
        """,
        (*player_ids,),
    )
    return [Participant(**row) for row in rows]


async def update_participant_points(participant_id: str, points: int):
    await db.execute(
        "UPDATE fantasyleague.participants SET total_points = ? WHERE id = ?",
        (points, participant_id),
    )
    return


## PLAYERS
async def create_players_bulk(data: Players):
    await db.execute(
        """
        INSERT INTO fantasyleague.players (id, league_id, api_id, name, position, team)
        VALUES
        (?, ?, ?, ?, ?)
        """,
        tuple(
            (
                urlsafe_short_hash(),
                player.league_id,
                player.api_id,
                player.name,
                player.position,
                player.team,
            )
            for player in data.players
        ),
    )


async def get_players_by_league(league_id: str) -> List[Player]:
    rows = await db.fetchall(
        "SELECT * FROM fantasyleague.players WHERE league_id = ?", (league_id,)
    )
    return [Player(**row) for row in rows]


async def get_player(player_id: str) -> Optional[Player]:
    row = await db.fetchone(
        "SELECT * FROM fantasyleague.players WHERE id = ?", (player_id,)
    )
    return Player(**row) if row else None


async def get_players(player_ids: List[int]) -> List[Player]:
    q = ",".join(["?"] * len(player_ids))
    rows = await db.fetchall(
        f"SELECT * FROM fantasyleague.players WHERE id IN ({q})", (*player_ids,)
    )
    return [Player(**row) for row in rows]


async def update_player_points(player_id: str, points: int):
    player = await get_player(player_id)
    if not player:
        return
    player.points += points
    await db.execute(
        "UPDATE fantasyleague.players SET points = ? WHERE id = ?",
        (player.points, player_id),
    )
    return


async def delete_player(player_id: str):
    await db.execute("DELETE FROM fantasyleague.players WHERE id = ?", (player_id,))
    return


async def delete_players_by_league(league_id: str):
    await db.execute(
        "DELETE FROM fantasyleague.players WHERE league_id = ?", (league_id,)
    )
    return


## PRIZE DISTRIBUTION


async def create_prize_distribution(data: CreatePrizeDistribution):
    await db.execute(
        """
        INSERT INTO fantasyleague.prize_distributions (league_id, participant_id, prize_type, prize_amount)
        VALUES (?, ?, ?, ?)
        """,
        (data.league_id, data.participant_id, data.prize_type, data.prize_amount),
    )
    return


async def get_prize_distributions(league_id: str):
    rows = await db.fetchall(
        "SELECT * FROM fantasyleague.prize_distributions WHERE league_id = ?",
        (league_id,),
    )
    return [PrizeDistribution(**row) for row in rows]
