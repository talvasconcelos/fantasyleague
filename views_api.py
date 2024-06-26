import time
from http import HTTPStatus

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from lnbits.core.crud import get_user
from lnbits.core.services import create_invoice
from lnbits.core.views.api import api_payment
from lnbits.decorators import (
    WalletTypeInfo,
    check_admin,
    require_admin_key,
    require_invoice_key,
)
from loguru import logger

from .api_football import (
    get_competitions,
    get_league_players,
    get_round,
    get_team_players,
    get_teams,
)
from .crud import (
    create_league,
    create_participant,
    create_participant_team,
    create_players_bulk,
    create_prize_distribution,
    create_settings,
    create_transfer,
    delete_league,
    get_active_leagues,
    get_free_transfers,
    get_league,
    get_leagues,
    get_participant,
    get_participant_by_wallet,
    get_participant_team,
    get_participants,
    get_player,
    get_players,
    get_players_by_league,
    get_prize_distributions,
    get_settings,
    get_transfers_participant,
    update_league,
    update_league_players,
    update_participant_formation,
    update_participant_lineup,
    update_participant_team,
    update_settings,
)
from .models import (
    CreateFantasyLeague,
    CreateParticipant,
    CreatePlayer,
    CreateTransfer,
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
        data.matchday = matchday[0]
        league = await create_league(data)
        assert league
        # season = league.season_start.split("-")[0]
        # teams = await get_teams(
        #     api_key=api_key.api_key,
        #     competition_code=league.competition_code,
        #     season=league.season,
        # )

        # players = [
        #     CreatePlayer(**player)
        #     for player in await get_league_players(
        #         api_key=api_key.api_key,
        #         league_id=league.id,
        #         competition_code=league.competition_code,
        #         season=league.season,
        #     )
        # ]
        # players = [
        #     CreatePlayer(**player)
        #     for player in await get_team_players(
        #         api_key=api_key.api_key,
        #         team_ids=[team["team"]["id"] for team in teams],
        #         league_id=league.id,
        #     )
        # ]
        # await create_players_bulk(PlayersBulk(players=players))
        await api_update_league_players(league.id, wallet.wallet.adminkey)
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


@fantasyleague_ext_api.delete(
    "/competition/{league_id}", description="Delete a Fantasy League"
)
async def api_delete_league(
    league_id: str, wallet: WalletTypeInfo = Depends(require_admin_key)
):
    league = await get_league(league_id)
    if not league:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Fantasy League not found."
        )
    await delete_league(league_id)
    return "", HTTPStatus.NO_CONTENT


## PARTICIPANTS

@fantasyleague_ext_api.get("/participant/{participant_id}", description="Get a participant")
async def api_get_participant(participant_id: str, wallet: WalletTypeInfo = Depends(require_admin_key)):
    participant = await get_participant(participant_id)
    if not participant:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Participant not found."
        )
    if participant.wallet != wallet.wallet.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Unauthorized.")
    
    return participant.dict()


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
    return await get_participant(participant_id)


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
    return await get_participant(participant_id)


@fantasyleague_ext_api.put("/participants/{participant_id}/lineup")
async def api_update_participant_lineup(
    participant_id: str,
    data: LineUp,
    formation: str = Query(None),
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
    if formation:
        await update_participant_formation(participant_id, formation)

    await update_participant_lineup(participant_id, data)
    return await get_participant(participant_id)


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


@fantasyleague_ext_api.get(
    "/competition/{league_id}/players/update",
    description="Update players",
    dependencies=[Depends(check_admin)],
)
async def api_update_league_players(
    league_id: str, wallet: WalletTypeInfo = Depends(require_admin_key)
):
    league = await get_league(league_id)
    if not league:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Fantasy League not found."
        )
    api_key = await get_settings()
    assert api_key, "Please add your API key first."
    teams = await get_teams(
        api_key=api_key.api_key,
        competition_code=league.competition_code,
        season=league.season,
    )
    players = [
        CreatePlayer(**player)
        for player in await get_team_players(
            api_key=api_key.api_key,
            team_ids=[team["team"]["id"] for team in teams],
            league_id=league.id,
        )
    ]
    # players = [
    #     CreatePlayer(**player)
    #     for player in await get_league_players(
    #         api_key=api_key.api_key,
    #         league_id=league.id,
    #         competition_code=league.competition_code,
    #         season=league.season,
    #     )
    # ]
    await update_league_players(league_id, PlayersBulk(players=players))
    return {"message": "Players updated."}


## TRANSFERS

@fantasyleague_ext_api.get('/transfers/{participant_id}', description='Get all transfers')
async def api_get_transfers(participant_id: str, wallet: WalletTypeInfo = Depends(require_invoice_key)):
    participant = await get_participant(participant_id)
    if not participant:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Participant not found."
        )
    if participant.wallet != wallet.wallet.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Unauthorized.")
    
    transfers = await get_transfers_participant(participant_id)
    return transfers

@fantasyleague_ext_api.post('/transfers', description='Create a new transfer')
async def api_create_transfer(data: CreateTransfer, wallet: WalletTypeInfo = Depends(require_admin_key)):
    participant = await get_participant(data.participant_id)
    if not participant:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Participant not found."
        )
    if participant.wallet != wallet.wallet.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Unauthorized.")
    
    league = await get_league(participant.fantasyleague_id)
    assert league, "League not found."

    if league.transfer_window_close < int(time.time()):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Transfer window closed."
        )
    free_transfers = await get_free_transfers(participant.id)
    # if free_transfers.free_transfers < 1:
    #     raise HTTPException(
    #         status_code=HTTPStatus.BAD_REQUEST, detail="No free transfers available."
    #     )
    
    data.gameweek = league.matchday
    transfer = await create_transfer(data, free_transfers.free_transfers)
    
    return transfer.dict()
