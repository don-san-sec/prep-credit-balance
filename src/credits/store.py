"""In-memory credit storage."""

from __future__ import annotations

from credits.models import Credit


class CreditStore:
    """Stores credits in memory.

    The production service backs this with Postgres; the billing run reads a
    customer's credits through this interface.
    """

    def __init__(self) -> None:
        self._credits: list[Credit] = []

    def save(self, credit: Credit) -> None:
        self._credits.append(credit)

    def list_for_customer(self, customer_id: str) -> list[Credit]:
        return [credit for credit in self._credits if credit.customer_id == customer_id]