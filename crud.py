import json
from typing import List, Optional, Union

from lnbits.helpers import urlsafe_short_hash
from loguru import logger

from . import db
from .models import (
    CreateFantasyLeague,
    CreateParticipant,
    CreatePrizeDistribution,
    CreateTransfer,
    FantasyLeague,
    FreeTransfer,
    LineUp,
    Participant,
    Player,
    Players,
    PlayersBulk,
    PrizeDistribution,
    Settings,
    Transfer,
)

## SETTINGS


async def get_settings() -> Optional[Settings]:
    row = await db.fetchone("SELECT * FROM fantasyleague.api_settings")
    return Settings(**row) if row else None


async def create_settings(data: Settings) -> Settings:
    await db.execute(
        """
        INSERT INTO fantasyleague.api_settings (api_key)
        VALUES (?)
        """,
        (data.api_key,),
    )
    settings = await get_settings()
    assert settings, "Newly created settings couldn't be retrieved"
    return settings


async def update_settings(data: Settings) -> Settings:
    await db.execute(
        "UPDATE fantasyleague.api_settings SET api_key = ?", (data.api_key,)
    )
    settings = await get_settings()
    assert settings, "Newly updated settings couldn't be retrieved"
    return settings


## LEAGUES


async def get_leagues(wallet_ids: Union[str, List[str]]) -> List[FantasyLeague]:
    if isinstance(wallet_ids, str):
        wallet_ids = [wallet_ids]

    q = ",".join(["?"] * len(wallet_ids))
    rows = await db.fetchall(
        f"SELECT * FROM fantasyleague.competitions WHERE wallet IN ({q})",
        (*wallet_ids,),
    )
    return [FantasyLeague(**row) for row in rows]


async def get_league(league_id: str) -> Optional[FantasyLeague]:
    row = await db.fetchone(
        "SELECT * FROM fantasyleague.competitions WHERE id = ?", (league_id,)
    )
    return FantasyLeague(**row) if row else None


async def get_active_leagues():
    rows = await db.fetchall(
        "SELECT * FROM fantasyleague.competitions WHERE has_ended = false"
    )
    return [FantasyLeague(**row) for row in rows]


async def create_league(data: CreateFantasyLeague) -> FantasyLeague:
    league_id = urlsafe_short_hash()
    await db.execute(
        """
        INSERT INTO fantasyleague.competitions (
            id, wallet, name, description, competition_type, competition_code, competition_logo,
            season_start, season_end, season, matchday, buy_in, fee, first_place, second_place,
            third_place, matchday_winner
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            league_id,
            data.wallet,
            data.name,
            data.description,
            data.competition_type,
            data.competition_code,
            data.competition_logo,
            data.season_start,
            data.season_end,
            data.season,
            data.matchday,
            data.buy_in,
            data.fee,
            data.first_place,
            data.second_place,
            data.third_place,
            data.matchday_winner,
        ),
    )
    league = await get_league(league_id)
    assert league, "Newly created league couldn't be retrieved"
    return league


async def update_league(league_id: str, **kwargs) -> FantasyLeague:
    q = ", ".join([f"{field[0]} = ?" for field in kwargs.items()])
    await db.execute(
        f"UPDATE fantasyleague.competitions SET {q} WHERE id = ?",
        (*kwargs.values(), league_id),
    )
    row = await db.fetchone(
        "SELECT * FROM fantasyleague.competitions WHERE id = ?", (league_id,)
    )
    assert row, "Newly updated league couldn't be retrieved"
    return FantasyLeague(**row)


async def delete_league(league_id: str):
    # delete all participants, players and league
    await db.execute(
        "DELETE FROM fantasyleague.participants WHERE fantasyleague_id = ?",
        (league_id,),
    )
    await db.execute(
        "DELETE FROM fantasyleague.players WHERE league_id = ?", (league_id,)
    )
    await db.execute(
        "DELETE FROM fantasyleague.competitions WHERE id = ?", (league_id,)
    )


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


async def get_participant_by_wallet(
    wallet: str, league_id: str
) -> Optional[Participant]:
    row = await db.fetchone(
        "SELECT * FROM fantasyleague.participants WHERE wallet = ? AND fantasyleague_id = ?",
        (wallet, league_id),
    )
    return Participant(**row) if row else None


async def get_participant(participant_id: str) -> Optional[Participant]:
    row = await db.fetchone(
        "SELECT * FROM fantasyleague.participants WHERE id = ?", (participant_id,)
    )
    return Participant(**row) if row else None


async def get_participant_competitions(wallet_ids: List[str]):
    q = ",".join(["?"] * len(wallet_ids))
    rows = await db.fetchall(
        f"SELECT * FROM fantasyleague.participants WHERE wallet IN ({q})",
        (*wallet_ids,),
    )
    return [Participant(**row) for row in rows]


async def create_participant(data: CreateParticipant) -> Participant:
    participant_id = urlsafe_short_hash()

    participants = await get_participants(data.fantasyleague_id)

    # get a median value, or average, of the total points of all participants
    # to set the new participant's total points to the median value
    # this is to prevent new participants from having an unfair disadvantage
    points = 0
    total_points = [participant.total_points for participant in participants]
    
    if(len(total_points) < 5):
        # calculate average points
        points = sum(total_points) // len(total_points) if len(total_points) > 0 else 0
    else:
        total_points.sort()
        points = total_points[len(total_points) // 2]

    await db.execute(
        """
        INSERT INTO fantasyleague.participants (id, fantasyleague_id, wallet, name, total_points)
        VALUES (?, ?, ?, ?, ?)
        """,
        (participant_id, data.fantasyleague_id, data.wallet, data.name, points),
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


async def get_participants_by_players(player_ids: List[str]) -> List[Participant]:
    q = ",".join(["?"] * len(player_ids))
    rows = await db.fetchall(
        f"""
        SELECT DISTINCT p.*
        FROM fantasyleague.participants p
        JOIN fantasyleague.participant_players pp ON p.id = pp.participant_id
        WHERE pp.player_id IN ({q})
        """,
        (*player_ids,),
    )
    return [Participant(**row) for row in rows]


async def update_participant_formation(participant_id: str, formation: str):
    await db.execute(
        "UPDATE fantasyleague.participants SET formation = ? WHERE id = ?",
        (formation, participant_id),
    )
    return


async def update_participant_lineup(participant_id: str, lineup: LineUp):
    # convert lineup list to a string of comma-separated values
    string_lineup = ",".join(lineup.lineup)
    await db.execute(
        "UPDATE fantasyleague.participants SET lineup = ? WHERE id = ?",
        (string_lineup, participant_id),
    )
    return


async def update_participant_points(participant_id: str, points: int):
    await db.execute(
        "UPDATE fantasyleague.participants SET total_points = total_points + ? WHERE id = ?",
        (points, participant_id),
    )
    return


async def create_participant_team(participant_id: str, player_ids: List[str]):
    await db.execute(
        """
        INSERT INTO fantasyleague.participant_players (participant_id, player_id)
        VALUES
        (?, ?)
        """,
        tuple((participant_id, player_id) for player_id in player_ids),
    )
    return


async def update_participant_team(participant_id: str, player_ids: List[str]):
    await db.execute(
        "DELETE FROM fantasyleague.participant_players WHERE participant_id = ?",
        (participant_id,),
    )
    await create_participant_team(participant_id, player_ids)
    return


## PLAYERS
async def create_players_bulk(data: PlayersBulk):
    await db.execute(
        """
        INSERT INTO fantasyleague.players (id, league_id, api_id, name, position, team, photo)
        VALUES
        (?, ?, ?, ?, ?, ?, ?)
        """,
        tuple(
            (
                urlsafe_short_hash(),
                player.league_id,
                player.api_id,
                player.name,
                player.position,
                player.team,
                player.photo,
            )
            for player in data.players
        ),
    )


async def get_players_by_league(league_id: str) -> List[Player]:
    rows = await db.fetchall(
        "SELECT * FROM fantasyleague.players WHERE league_id = ?", (league_id,)
    )
    return [Player(**row) for row in rows]


async def update_league_players(league_id: str, data: PlayersBulk):
    # add new players if they don't exist
    # (API may not have all players when creating a league, so we need to update them later)
    players = await get_players_by_league(league_id)
    player_ids = [player.api_id for player in players]
    new_players = [player for player in data.players if player.api_id not in player_ids]
    if new_players:
        await create_players_bulk(PlayersBulk(players=new_players))
    return


async def get_player(player_id: str) -> Optional[Player]:
    row = await db.fetchone(
        "SELECT * FROM fantasyleague.players WHERE id = ?", (player_id,)
    )
    return Player(**row) if row else None


async def get_player_by_api_id(api_id: str) -> Optional[Player]:
    row = await db.fetchone(
        "SELECT * FROM fantasyleague.players WHERE api_id = ?", (api_id,)
    )
    return Player(**row) if row else None

async def get_players_by_api_id(api_ids: List[int]) -> List[Player]:
    q = ",".join(["?"] * len(api_ids))
    rows = await db.fetchall(
        f"SELECT * FROM fantasyleague.players WHERE api_id IN ({q})", (*api_ids,)
    )
    return [Player(**row) for row in rows]


async def get_players(player_ids: List[str]) -> List[Player]:
    if len(player_ids) == 0:
        return []

    q = ",".join(["?"] * len(player_ids))
    rows = await db.fetchall(
        f"SELECT * FROM fantasyleague.players WHERE id IN ({q})", (*player_ids,)
    )
    return [Player(**row) for row in rows]


async def update_player_points(player_id: str, points: int):
    await db.execute(
        "UPDATE fantasyleague.players SET points = points + ? WHERE api_id = ?",
        (points, player_id),
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

## TRANSFERS
async def update_transfer_window(league_id: str, timestamp: int):
    await db.execute(
        "UPDATE fantasyleague.competitions SET transfer_window_close = ? WHERE id = ?",
        (timestamp, league_id),
    )
    return

async def get_transfers_participant(participant_id: str):
    rows = await db.fetchall(
        "SELECT * FROM fantasyleague.participant_transfers WHERE participant_id = ?", (participant_id,)
    )
    return [Transfer(**row) for row in rows]

async def get_transfer(transfer_id: str):
    row = await db.fetchone(
        "SELECT * FROM fantasyleague.participant_transfers WHERE id = ?", (transfer_id,)
    )
    return Transfer(**row) if row else None

async def create_transfer(data: CreateTransfer, free_transfers: int, saved_transfers: int = 0):
    participant = await get_participant(data.participant_id)
    cost = 0
    if free_transfers > 0:
        await update_free_transfers(data.participant_id, free_transfers - 1, saved_transfers)
    else:
        cost = 4
        await update_participant_points(data.participant_id, -cost)
        
    transfer_id = urlsafe_short_hash()

    await db.execute(
        """
        INSERT INTO fantasyleague.participant_transfers (id, participant_id, player_out_id, player_in_id, gameweek, cost)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (transfer_id, data.participant_id, data.player_out_id, data.player_in_id, data.gameweek, cost),
    )

    #replace new player with old player
    await db.execute(
        """
        UPDATE fantasyleague.participant_players SET player_id = ? WHERE participant_id = ? AND player_id = ?
        """,
        (data.player_in_id, data.participant_id, data.player_out_id),
    )

    # replace player in lineup
    lineup = participant.lineup.split(",")
    lineup[lineup.index(data.player_out_id)] = data.player_in_id
    await update_participant_lineup(data.participant_id, LineUp(lineup=lineup))
    
    return await get_transfer(transfer_id)

async def update_free_transfers(participant_id: str, free_transfers: int, saved_transfers: int):
    await db.execute(
        "UPDATE fantasyleague.participant_free_transfers SET free_transfers = ?, saved_transfers = ? WHERE participant_id = ?",
        (free_transfers, saved_transfers, participant_id),
    )
    return

async def get_free_transfers(participant_id: str):
    row = await db.fetchone(
        "SELECT * FROM fantasyleague.participant_free_transfers WHERE participant_id = ?", (participant_id,)
    )
    return FreeTransfer(**row) if row else None

async def get_free_transfers_participants(participants: List[str]):
    q = ",".join(["?"] * len(participants))
    rows = await db.fetchall(
        f"SELECT * FROM fantasyleague.participant_free_transfers WHERE participant_id IN ({q})", (*participants,)
    )
    return [FreeTransfer(**row) for row in rows]

async def reset_free_transfers(participant_id: str):
    await db.execute(
        "UPDATE fantasyleague.participant_free_transfers SET free_transfers = 1, saved_transfers = 0 WHERE participant_id = ?",
        (participant_id,),
    )
    return