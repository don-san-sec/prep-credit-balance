"""Credit and invoice models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class Credit:
    """Credit on a customer's account.

    From an overpayment or a goodwill credit from the complaints team. The
    amount is whole pence and shrinks as the credit is used. `expires_at` is
    the last date the credit can be applied, or None if it never expires.
    """

    credit_id: str
    customer_id: str
    amount_pence: int
    created_at: date
    expires_at: date | None = None


@dataclass
class Invoice:
    """One customer's monthly invoice. All amounts are whole pence."""

    invoice_id: str
    customer_id: str
    invoice_date: date
    total_pence: int