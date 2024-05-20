from http import HTTPStatus

from fastapi import APIRouter, Depends, Query, Request
from fastapi.exceptions import HTTPException
from lnbits.core.crud import get_user
from lnbits.decorators import WalletTypeInfo, get_key_type, require_admin_key

from . import football_data
from .crud import (
    create_league,
    create_participant,
    create_players_bulk,
    create_prize_distribution,
    get_active_leagues,
    get_league,
    get_leagues,
    get_participants,
    get_player,
    get_players,
    get_players_by_league,
    get_prize_distributions,
    update_league,
    create_settings,
)
from .models import (
    CreateFantasyLeague,
    CreateParticipant,
    FantasyLeague,
    Participant,
    Settings,
    Player,
    PrizeDistribution,
    UpdateFantasyLeague,
)

fantasyleague_ext_api = APIRouter(
    prefix="/api/v1",
    tags=["fantasyleague"],
)


@fantasyleague_ext_api.post(
    "/fantasyleague/settings",
    response_model=FantasyLeague,
    description="Create Fantasy League setings",
    status_code=HTTPStatus.CREATED,
)
async def api_create_settings(
    data: Settings, wallet: WalletTypeInfo = Depends(require_admin_key)
):
    settings = await create_settings(data)
    return settings.dict()


@fantasyleague_ext_api.get("/fantasyleague", description="fantasyleague API endpoint")
async def api_fantasyleague(
    all_wallets: bool = Query(False),
    wallet: WalletTypeInfo = Depends(require_admin_key),
):
    wallet_ids = [wallet.wallet.id]
    if all_wallets:
        user = await get_user(wallet.wallet.user)
        wallet_ids = user.wallet_ids if user else []
    return [league.dict() for league in await get_leagues(wallet_ids)]


@fantasyleague_ext_api.post(
    "/fantasyleague",
    response_model=FantasyLeague,
    description="Create a new Fantasy League",
    status_code=HTTPStatus.CREATED,
)
async def api_create_fantasyleague(
    data: CreateFantasyLeague, wallet: WalletTypeInfo = Depends(require_admin_key)
):
    # check if a league is already running
    if await get_active_leagues():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="A league is already running. You can only have one active league at a time.",
        )
    try:
        league = await create_league(data)
        assert league
        # populate DB for the competition
        players = await football_data.get_players(league.id)
        await create_players_bulk(players)
        return league.dict()
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=f"Error creating league: {e}"
        ) from None


@fantasyleague_ext_api.patch(
    "/fantasyleague/{league_id}",
    response_model=FantasyLeague,
    description="Update a Fantasy League",
)
async def api_update_fantasyleague(
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
    "/fantasyleague/{league_id}/participants",
    description="Get all participants in a league",
)
async def api_get_participants(league_id: str):
    return [participant.dict() for participant in await get_participants(league_id)]


@fantasyleague_ext_api.post(
    "/fantasyleague/{league_id}/participant",
    response_model=Participant,
    description="Create a new participant in a league",
)
async def api_create_participant(data: CreateParticipant):
    try:
        participant = await create_participant(data)
        assert participant
        return participant.dict()
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Error creating participant: {e}",
        ) from None


## PLAYERS


@fantasyleague_ext_api.get(
    "/fantasyleague/{league_id}/players", description="Get all players in a league"
)
async def api_get_league_players(league_id: str):
    return [player.dict() for player in await get_players_by_league(league_id)]


@fantasyleague_ext_api.get(
    "/fantasyleague/players/{player_id}", description="Get a specific player"
)
async def api_get_player(player_id: str):
    player = await get_player(player_id)
    if not player:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Player not found."
        )
    return player.dict()
