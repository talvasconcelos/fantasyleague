from typing import List

from httpx import get
from lnbits.core.services import create_invoice, pay_invoice

from .crud import get_league, get_participants, get_prize_distributions, get_settings
from .models import CreatePrizeDistribution, Participant


async def get_total_pool(league_id: str):
    league = await get_league(league_id)
    assert league, "League not found"
    participants = await get_participants(league_id)
    rewards = await get_prize_distributions(league_id)
    total_buy_ins = len(participants) * league.buy_in
    total_rewards = sum([reward.prize_amount for reward in rewards])
    return total_buy_ins - total_rewards


async def create_internal_payment(league_id, user_wallet, amount):
    league = await get_league(league_id)
    assert league, "League not found"

    _, payment_request = await create_invoice(
        wallet_id=user_wallet,
        amount=amount,
        internal=True,
        memo="Fantasy League Reward",
    )

    await pay_invoice(
        payment_request=payment_request,
        wallet_id=league.wallet,
        extra={"tag": "fantasyleague", "league_id": league_id, "reward": amount},
    )


async def pay_rewards_overall(league_id: str, winners: List[Participant]):
    total_pool = await get_total_pool(league_id)
    league = await get_league(league_id)
    assert league, "League not found"

    assert (
        league.first_place and league.second_place and league.third_place
    ), "Prize distribution not set"

    for idx, winner in enumerate(winners):
        amount = 0
        if idx == 0:
            amount = int(total_pool * league.first_place)
        elif idx == 1:
            amount = int(total_pool * league.second_place)
        else:
            amount = int(total_pool * league.third_place)

        await create_internal_payment(league_id, winner.wallet, amount)
    return


async def pay_weekly_reward(league_id: str, winner: Participant):
    settings = await get_settings()
    assert settings, "Settings not found"
    if not settings.weekly_prize:
        return
    total_pool = await get_total_pool(league_id)
    amount = int(total_pool * settings.weekly_prize)

    await create_internal_payment(league_id, winner.wallet, amount)


async def pay_monthly_reward(league_id: str, winner: Participant):
    settings = await get_settings()
    assert settings, "Settings not found"
    if not settings.monthly_prize:
        return
    total_pool = await get_total_pool(league_id)
    amount = int(total_pool * settings.monthly_prize)

    await create_internal_payment(league_id, winner.wallet, amount)


async def pay_matchday_reward(league_id: str, winner: Participant):
    settings = await get_settings()
    assert settings, "Settings not found"
    if not settings.matchday_prize:
        return
    total_pool = await get_total_pool(league_id)
    amount = int(total_pool * settings.matchday_prize)

    await create_internal_payment(league_id, winner.wallet, amount)
