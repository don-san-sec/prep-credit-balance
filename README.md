# Account credit on invoices

Customers end up with credit on their Brightwatt Energy account —
overpayments, goodwill credits from complaints — and that credit must be
applied to new invoices before any money is taken from them.

## Context

Brightwatt Energy is an app-first UK domestic energy supplier. About 180,000
customers pay a monthly bill, and every amount is stored in whole pence.

Customers sometimes end up in credit: they overpay a bill, or the complaints
team issues a goodwill credit after a bad experience. Those credits sit on the
account until they are used. Today the monthly billing run ignores them and
charges the payment method in full, which generates refund requests and
complaints.

The ticket for this work is BILL-152:

> "Apply account credit to new invoices automatically."

## The billing handbook's credit rules

These come from the finance team's billing handbook. The monthly billing run
must follow them exactly, or statements stop matching what customers expect
to see.

1. Each credit has an amount (`amount_pence`), a `created_at` date, and an
   optional `expires_at` (a date, or `None` if the credit never expires).
2. When an invoice is issued, available credits are applied **before**
   charging the customer's payment method.
3. Credits are applied **oldest-created first**, one at a time, until the
   invoice is covered.
4. A credit is expired if its `expires_at` is **strictly before** the invoice
   date. A credit expiring **on** the invoice date is still valid.
5. If credits cover the invoice fully, **no payment is taken**; if they cover
   it partly, the payment is the remainder. Leftover credit stays on the
   account.
6. A partially used credit **keeps its remaining amount** (`amount_pence` is
   reduced; the credit is not consumed).

Worked examples from the handbook:

- An invoice of 5000p against credits of 3000p and 4000p (oldest first)
  applies 3000p, then 2000p of the second credit. No payment is taken, and
  the second credit keeps 2000p.
- An invoice of 3000p against a single credit of 5000p takes no payment, and
  the credit keeps 2000p.

## How it works

```
src/credits/
  models.py           Credit, Invoice
  store.py            CreditStore: in-memory credit storage
  billing.py          charge_for_invoice(); charging the payment method
tests/
```

Credit application is not implemented yet: `charge_for_invoice()` charges the
full invoice total and ignores any credit on the account. The monthly billing
run (not part of this service) issues the invoices; this service owns the
credit and invoice models and decides what to charge.

## Running locally

```
uv sync
uv run pytest -q
```

## Your task

A colleague has opened a PR: https://github.com/don-san-sec/prep-credit-balance/pull/1. You are the owner of this feature. Review the PR and decide whether to accept or reject it, and explain why.
