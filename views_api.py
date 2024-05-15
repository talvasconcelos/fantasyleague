from http import HTTPStatus

import httpx
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from lnbits.decorators import WalletTypeInfo, get_key_type

from .models import fantasyleague

# views_api.py is for you API endpoints that could be hit by another service

fantasyleague_ext_api = APIRouter(
    prefix="/api/v1",
    tags=["fantasyleague"],
)


@fantasyleague_ext_api.get("/test/{fantasyleague_data}", description="fantasyleague API endpoint")
async def api_fantasyleague(fantasyleague_data: str) -> fantasyleague:
    # Do some python things and return the data
    return fantasyleague(id="1", wallet=fantasyleague_data)


@fantasyleague_ext_api.get("/vetted", description="Get the vetted extension readme")
async def api_get_vetted(wallet: WalletTypeInfo = Depends(get_key_type)):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://raw.githubusercontent.com/lnbits/lnbits-extensions/main/README.md"
            )
            return resp.text
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e
