import os
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass
from collections import defaultdict, deque

from utils.args import parse_args
from utils.timer import timer

"""
Preprocessing:
- The file has two blocks separated by a blank line, so we split on "\n\n" once: the first block is
  parsed as "codename HAS amount" lines into a dict of balances, the second as "FROM x TO y AMT n" lines
  (grabbed with a regex) into a list of Transaction objects.

Part 1:
- Nothing fancy here: we just replay the transactions in order, moving amount from source to destination,
  and let balances go negative when a transfer exceeds what the sender has. Once every transaction has run,
  we sort the balances and sum the top 3.

Part 2:
- Same as part 1, but a transaction can no longer push a balance below 0. Before applying a transfer we
  clamp the amount to whatever the source currently has, so a sender can never send more than it owns and
  is left at exactly 0 instead of going negative.

Part 3:
- This is part 2 plus bookkeeping for the unpaid remainder. When a transfer gets clamped, the shortfall
  becomes a Debt owed by the source to the destination, stored in a deque per debtor so debts stay ordered
  from oldest (highest priority) to newest.
- The trick is that receiving money should immediately try to clear that receiver's own debts, and clearing
  a debt is itself a payment to someone else, who might have debts of their own. We handle that by calling
  pay_debt recursively: every time balances[destination] changes because of a payoff, we call
  pay_debt(amount, debt.destination) again on the party that just got paid, so a single incoming payment can
  cascade through a whole chain of debts in one go. pay_debt only pops a debt off the front of the deque
  once it can be paid off in full or the debtor runs out of money, and pushes back a partial debt for the
  remainder otherwise, which keeps the FIFO priority order intact.
- Since we only care about the 3 highest balances, we don't bother forcing any leftover negative-looking
  balances to 0 the way the description describes it for debtors: a balance can never actually go negative
  in this version (transfers are clamped), so there's nothing to floor.
"""


TEST_DATA = parse_args()


@dataclass
class Transaction:
    source: str
    destination: str
    amount: int


@dataclass
class Debt:
    destination: str
    amount: int


@timer
def part1():
    balances, transactions = parse_file()

    for tx in transactions:
        balances[tx.source] -= tx.amount
        balances[tx.destination] += tx.amount

    sum_highest_balances = sum(sorted(balances.values())[-3:])

    print(f"Sum of the 3 highest balances: {sum_highest_balances}")


@timer
def part2():
    balances, transactions = parse_file()

    for tx in transactions:
        if tx.amount > balances[tx.source]:
            tx.amount = balances[tx.source]

        balances[tx.source] -= tx.amount
        balances[tx.destination] += tx.amount

    sum_highest_balances = sum(sorted(balances.values())[-3:])

    print(f"Sum of the 3 highest balances: {sum_highest_balances}")


@timer
def part3():
    balances, transactions = parse_file()
    debts = defaultdict(deque)

    def pay_debt(amount: int, destination: str):
        if amount <= 0 or destination not in debts:
            return

        while len(debts[destination]) > 0 and balances[destination] > 0:
            debt = debts[destination].popleft()

            if balances[destination] >= debt.amount:
                amount = debt.amount
            else:
                amount = balances[destination]
                new_debt = Debt(debt.destination, debt.amount - balances[destination])
                debts[destination].appendleft(new_debt)

            balances[destination] -= amount
            balances[debt.destination] += amount

            pay_debt(amount, debt.destination)

    for tx in transactions:
        if tx.amount > balances[tx.source]:
            if balances[tx.source] > 0:
                new_debt = Debt(tx.destination, tx.amount - balances[tx.source])
                tx.amount = balances[tx.source]
            else:
                new_debt = Debt(tx.destination, tx.amount)
                tx.amount = 0
            debts[tx.source].append(new_debt)

        balances[tx.source] -= tx.amount
        balances[tx.destination] += tx.amount

        pay_debt(tx.amount, tx.destination)

    sum_highest_balances = sum(sorted(balances.values())[-3:])

    print(f"Sum of the 3 highest balances: {sum_highest_balances}")


def parse_file() -> Tuple[Dict[str, int], List[Transaction]]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    balances = dict()
    transactions = []
    with open(abs_file_path, "r") as f:
        balances_raw, transactions_raw = f.read().split("\n\n")

        for balance_raw in balances_raw.split("\n"):
            codename, balance = balance_raw.strip().split(" HAS ")
            balances[codename] = int(balance)

        for tx in transactions_raw.split("\n"):
            tx = re.search(r"FROM\s+([-\w]+)\s+TO\s+([-\w]+)\s+AMT\s+(\d+)", tx)
            source, destination, amount = tx.groups()
            transactions.append(Transaction(source, destination, int(amount)))

    return balances, transactions


part1()
part2()
part3()
