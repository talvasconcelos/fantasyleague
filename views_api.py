from http import HTTPStatus

from fastapi import APIRouter, Depends, Query, Request
from fastapi.exceptions import HTTPException
from lnbits.core.crud import get_user
from lnbits.core.services import create_invoice
from lnbits.core.views.api import api_payment
from lnbits.decorators import WalletTypeInfo, check_admin, require_admin_key
from loguru import logger
from tests import api

from .api_football import get_competitions, get_league_players, get_round
from .crud import (
    create_league,
    create_participant,
    create_participant_team,
    create_players_bulk,
    create_prize_distribution,
    create_settings,
    get_active_leagues,
    get_league,
    get_leagues,
    get_participant,
    get_participant_by_wallet,
    get_participants,
    get_player,
    get_players,
    get_players_by_league,
    get_prize_distributions,
    get_settings,
    update_league,
    update_participant_formation,
    update_participant_lineup,
    update_participant_team,
    update_settings,
)
from .models import (
    CreateFantasyLeague,
    CreateParticipant,
    CreatePlayer,
    FantasyLeague,
    LineUp,
    Participant,
    Player,
    PlayersBulk,
    PrizeDistribution,
    Settings,
    Team,
)

fantasyleague_ext_api = APIRouter(
    prefix="/api/v1",
    tags=["fantasyleague"],
)


@fantasyleague_ext_api.get(
    "/settings",
    description="Get Fantasy League settings",
    dependencies=[Depends(check_admin)],
)
async def api_get_settings(wallet: WalletTypeInfo = Depends(require_admin_key)):
    settings = await get_settings()
    return settings.dict() if settings else None


@fantasyleague_ext_api.post(
    "/settings",
    response_model=Settings,
    description="Create Fantasy League settings",
    status_code=HTTPStatus.CREATED,
)
async def api_create_settings(
    data: Settings, wallet: WalletTypeInfo = Depends(require_admin_key)
):
    settings = await create_settings(data)
    return settings.dict()


@fantasyleague_ext_api.put(
    "/settings",
    response_model=Settings,
    description="Update Fantasy League settings",
    dependencies=[Depends(check_admin)],
)
async def api_update_settings(
    data: Settings, wallet: WalletTypeInfo = Depends(require_admin_key)
):
    settings = await update_settings(data)
    return settings.dict()


## COMPETITIONS


@fantasyleague_ext_api.get("/eligible", description="Get all eligible competitions")
async def api_get_eligible_leagues():
    api_key = await get_settings()
    assert api_key, "Please add your API key first."
    return await get_competitions(api_key.api_key)


@fantasyleague_ext_api.get("/competition", description="Get all Fantasy Leagues")
async def api_get_leagues(
    all_wallets: bool = Query(False),
    wallet: WalletTypeInfo = Depends(require_admin_key),
):
    wallet_ids = [wallet.wallet.id]
    if all_wallets:
        user = await get_user(wallet.wallet.user)
        wallet_ids = user.wallet_ids if user else []
    return [league.dict() for league in await get_leagues(wallet_ids)]


@fantasyleague_ext_api.get(
    "/competitions/available", description="Get available competitions"
)
async def api_get_active_leagues():
    return [league.dict() for league in await get_active_leagues()]


@fantasyleague_ext_api.post(
    "/competition",
    response_model=FantasyLeague,
    description="Create a new Fantasy League",
    status_code=HTTPStatus.CREATED,
    dependencies=[Depends(check_admin)],
)
async def api_create_league(
    data: CreateFantasyLeague, wallet: WalletTypeInfo = Depends(require_admin_key)
):
    api_key = await get_settings()
    assert api_key, "Please add your API key first."
    try:
        matchday = await get_round(api_key.api_key, data.competition_code, data.season)
        data.matchday = matchday
        league = await create_league(data)
        assert league
        # season = league.season_start.split("-")[0]
        players = [
            CreatePlayer(**player)
            for player in await get_league_players(
                api_key=api_key.api_key,
                league_id=league.id,
                competition_code=league.competition_code,
                season=league.season,
            )
        ]
        await create_players_bulk(PlayersBulk(players=players))
        return league.dict()
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=f"Error creating league: {e}"
        ) from None


@fantasyleague_ext_api.patch(
    "/competition/{league_id}",
    response_model=FantasyLeague,
    description="Update a Fantasy League",
    dependencies=[Depends(check_admin)],
)
async def api_update_league(
    league_id: str,
    data: CreateFantasyLeague,
    wallet: WalletTypeInfo = Depends(require_admin_key),
):
    league = await get_league(league_id)
    if not league:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Fantasy League not found."
        )
    league = await update_league(league_id, **data.dict())
    return league.dict()


## PARTICIPANTS


@fantasyleague_ext_api.get(
    "/participants/{league_id}",
    description="Get all participants in a league",
)
async def api_get_participants(league_id: str):
    return [participant.dict() for participant in await get_participants(league_id)]


@fantasyleague_ext_api.post(
    "/participants/join",
    description="Create a new participant in a league",
)
async def api_create_participant(
    data: CreateParticipant,
    wallet: WalletTypeInfo = Depends(require_admin_key),
):
    # Check if league exists
    league = await get_league(data.fantasyleague_id)
    if not league:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Fantasy League not found."
        )
    # Check if participant already exists
    participant = await get_participant_by_wallet(data.wallet, data.fantasyleague_id)
    if participant:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Participant already exists in this league.",
        )
    extra = {
        "tag": "fantasyleague",
        "id": data.fantasyleague_id,
        "wallet": data.wallet,
        "name": data.name,
    }
    try:
        payment_hash, payment_request = await create_invoice(
            wallet_id=league.wallet,
            amount=league.buy_in,  # type: ignore
            memo=f"Join Competition: {league.name}",
            extra=extra,
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Error creating participant: {e}",
        ) from None

    return {"payment_hash": payment_hash, "payment_request": payment_request}


@fantasyleague_ext_api.get("/participants/join/{league_id}/{payment_hash}")
async def api_check_participant_payment(league_id: str, payment_hash: str):
    league = await get_league(league_id)
    if not league:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Fantasy League not found."
        )
    try:
        status = await api_payment(payment_hash)

    except Exception as exc:
        logger.error(exc)
        return {"paid": False}
    return status


@fantasyleague_ext_api.post("/participants/{participant_id}/team")
async def api_create_participant_team(
    participant_id: str,
    data: Team,
    wallet: WalletTypeInfo = Depends(require_admin_key),
):
    participant = await get_participant(participant_id)
    if not participant:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Participant not found."
        )
    if participant.wallet != wallet.wallet.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Unauthorized.")
    # Check if league exists
    league = await get_league(participant.fantasyleague_id)
    if not league:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Fantasy League not found."
        )
    await create_participant_team(participant_id, data.team)
    await update_participant_formation(participant_id, data.formation)


@fantasyleague_ext_api.put("/participants/{participant_id}/team")
async def api_update_participant_team(
    participant_id: str,
    data: Team,
    wallet: WalletTypeInfo = Depends(require_admin_key),
):
    participant = await get_participant(participant_id)
    if not participant:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Participant not found."
        )
    if participant.wallet != wallet.wallet.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Unauthorized.")
    # Check if league exists
    league = await get_league(participant.fantasyleague_id)
    if not league:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Fantasy League not found."
        )
    await update_participant_team(participant_id, data.team)
    await update_participant_formation(participant_id, data.formation)


@fantasyleague_ext_api.put("/participants/{participant_id}/lineup")
async def api_update_participant_lineup(
    participant_id: str,
    data: LineUp,
    wallet: WalletTypeInfo = Depends(require_admin_key),
):
    participant = await get_participant(participant_id)
    if not participant:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Participant not found."
        )
    if participant.wallet != wallet.wallet.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Unauthorized.")
    # Check if league exists
    league = await get_league(participant.fantasyleague_id)
    if not league:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Fantasy League not found."
        )
    await update_participant_lineup(participant_id, data)


## PLAYERS


@fantasyleague_ext_api.get(
    "/competition/{league_id}/players", description="Get all players in a league"
)
async def api_get_league_players(league_id: str):
    return [player.dict() for player in await get_players_by_league(league_id)]


@fantasyleague_ext_api.get("/players/{player_id}", description="Get a specific player")
async def api_get_player(player_id: str):
    player = await get_player(player_id)
    if not player:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Player not found."
        )
    return player.dict()
