from datetime import date

from credits.models import Credit
from credits.store import CreditStore


def credit(customer_id: str = "cus_0001", amount_pence: int = 2000) -> Credit:
    return Credit("crd_0001", customer_id, amount_pence, date(2026, 8, 1))


def test_save_and_list_for_customer() -> None:
    store = CreditStore()
    store.save(credit("cus_0001", 2000))
    store.save(credit("cus_0002", 5000))
    store.save(credit("cus_0001", 1500))

    listed = store.list_for_customer("cus_0001")
    assert [c.amount_pence for c in listed] == [2000, 1500]


def test_lists_nothing_for_an_unknown_customer() -> None:
    store = CreditStore()
    store.save(credit("cus_0001"))

    assert store.list_for_customer("cus_9999") == []
