"""Charging for customer invoices."""

from __future__ import annotations

from credits.models import Invoice


def charge_for_invoice(invoice: Invoice) -> int:
    """The amount to charge the customer's payment method for this invoice.

    Credits are NOT applied yet (BILL-152 is open): the customer is charged
    the full invoice total.
    """
    return invoice.total_pence