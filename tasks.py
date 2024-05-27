import asyncio

from lnbits.core.models import Payment
from lnbits.tasks import register_invoice_listener
from loguru import logger

from .crud import get_league, create_participant, update_league
from .models import CreateParticipant


async def wait_for_paid_invoices():
    invoice_queue = asyncio.Queue()
    register_invoice_listener(invoice_queue, "fantasyleague")

    while True:
        payment = await invoice_queue.get()
        await on_invoice_paid(payment)


async def on_invoice_paid(payment: Payment) -> None:
    if (
        payment.extra.get("tag") == "fantasyleague"
    ):  # Will grab any payment with the tag "fantasyleague"
        if payment.extra.get("reward"):
            logger.debug("Reward payment received")
            return
        if (
            payment.extra.get("id")
            and payment.extra.get("wallet")
            and payment.extra.get("name")
        ):
            fantasyleague_id = payment.extra.get("id")
            wallet = payment.extra.get("wallet")
            name = payment.extra.get("name")
            assert fantasyleague_id and wallet and name

            league = await get_league(fantasyleague_id)
            assert league

            if payment.amount == league.buy_in * 1000:
                participant = CreateParticipant(
                    fantasyleague_id=fantasyleague_id,
                    wallet=wallet,
                    name=name,
                )
                await payment.set_pending(False)
                await create_participant(participant)
                await update_league(
                    fantasyleague_id, num_participants=league.num_participants + 1
                )
                logger.debug("Payment for league buy-in received")
