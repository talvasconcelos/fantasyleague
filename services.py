from typing import List

from lnbits.core.services import create_invoice, pay_invoice
from loguru import logger

from .crud import create_prize_distribution, get_league, get_participant_by_wallet
from .models import CreatePrizeDistribution, Participant


async def create_internal_payment(league_id, league_wallet, user_wallet, amount):
    try:
        _, payment_request = await create_invoice(
            wallet_id=user_wallet,
            amount=amount,
            internal=True,
            memo="Fantasy League Reward",
        )

        await pay_invoice(
            payment_request=payment_request,
            wallet_id=league_wallet,
            extra={"tag": "fantasyleague", "league_id": league_id, "reward": amount},
        )

    except Exception as e:
        logger.error(f"Error creating internal payment: {e}")
        return



async def pay_rewards_overall(league_id: str, winners: List[Participant]):
    league = await get_league(league_id)
    assert league, "League not found"

    assert (
        league.first_place and league.second_place and league.third_place
    ), "Prize distribution not set"

    total_pool, _ = league.prize_distribution

    for idx, winner in enumerate(winners):
        amount = 0
        prize = 'reward'
        if idx == 0:
            amount = int(total_pool * league.first_place)
            prize = "first_place"
        elif idx == 1:
            amount = int(total_pool * league.second_place)
            prize = "second_place"
        else:
            amount = int(total_pool * league.third_place)
            prize = "third_place"

        await create_internal_payment(league.id, league.wallet, winner.wallet, amount)
        await create_prize_distribution(
            CreatePrizeDistribution(
                league_id=league_id,
                participant_id=winner.id,
                prize_type=prize,
                prize_amount=amount,
            )
        )
    return


async def pay_matchday_reward(league_id: str, winner: Participant, reward_type: str = "matchday_winner"):
    league = await get_league(league_id)
    assert league, "League not found"

    _, total_matchday = league.prize_distribution
    amount = int(total_matchday * league.matchday_winner)

    await create_internal_payment(league.id, league.wallet, winner.wallet, amount)
    await create_prize_distribution(
            CreatePrizeDistribution(
                league_id=league_id,
                participant_id=winner.id,
                prize_type=reward_type,
                prize_amount=amount,
            )
        )
