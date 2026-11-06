"""Apply account credit to new invoices (BILL-152)."""

from __future__ import annotations

from dataclasses import dataclass

from credits.models import Invoice
from credits.store import CreditStore


@dataclass
class PaymentInstruction:
    """What the billing run should charge the customer's payment method."""

    amount_pence: int


def apply_credits(invoice: Invoice, store: CreditStore) -> PaymentInstruction:
    """Apply the customer's available credits to an invoice.

    Walks the customer's credits, applies them against the invoice total one
    at a time until it is covered, and returns a payment instruction for
    whatever is left. Credits that have expired by the invoice date are
    skipped.
    """
    credits = sorted(
        store.list_for_customer(invoice.customer_id),
        key=lambda credit: credit.created_at,
        reverse=True,
    )
    remaining = invoice.total_pence
    for credit in credits:
        if credit.expires_at is not None and credit.expires_at <= invoice.invoice_date:
            continue
        if remaining <= 0:
            break
        applied = min(credit.amount_pence, remaining)
        remaining -= applied
        credit.amount_pence = 0
    return PaymentInstruction(amount_pence=max(remaining, 0))