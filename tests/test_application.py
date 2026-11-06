from datetime import date

from credits.application import apply_credits
from credits.models import Credit, Invoice
from credits.store import CreditStore


def invoice(total_pence: int) -> Invoice:
    return Invoice("inv_0001", "cus_0001", date(2026, 10, 1), total_pence)


def test_partly_covering_credit_charges_the_remainder() -> None:
    store = CreditStore()
    store.save(Credit("crd_0001", "cus_0001", 3000, date(2026, 8, 1)))

    instruction = apply_credits(invoice(5000), store)

    assert instruction.amount_pence == 2000


def test_credit_covering_the_whole_invoice_takes_no_payment() -> None:
    store = CreditStore()
    store.save(Credit("crd_0001", "cus_0001", 5000, date(2026, 8, 1)))

    instruction = apply_credits(invoice(3000), store)

    assert instruction.amount_pence == 0


def test_expired_credit_is_skipped() -> None:
    store = CreditStore()
    store.save(Credit("crd_0001", "cus_0001", 2000, date(2026, 6, 1), date(2026, 9, 1)))

    instruction = apply_credits(invoice(5000), store)

    assert instruction.amount_pence == 5000


def test_non_expiring_credit_is_valid() -> None:
    store = CreditStore()
    store.save(Credit("crd_0001", "cus_0001", 4000, date(2026, 8, 1)))

    instruction = apply_credits(invoice(3000), store)

    assert instruction.amount_pence == 0


def test_customer_without_credit_is_charged_in_full() -> None:
    instruction = apply_credits(invoice(5000), CreditStore())

    assert instruction.amount_pence == 5000
