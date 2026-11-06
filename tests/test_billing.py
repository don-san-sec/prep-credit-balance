from datetime import date

from credits.billing import charge_for_invoice
from credits.models import Invoice


def test_charge_is_the_full_invoice_total() -> None:
    invoice = Invoice("inv_0001", "cus_0001", date(2026, 10, 1), 5000)

    # Credits are not applied yet (BILL-152): the customer is charged in full.
    assert charge_for_invoice(invoice) == 5000


def test_zero_invoice_charges_nothing() -> None:
    invoice = Invoice("inv_0002", "cus_0002", date(2026, 10, 1), 0)

    assert charge_for_invoice(invoice) == 0
