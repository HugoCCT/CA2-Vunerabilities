"""Intentionally racy in-memory account used for the CA2 TOCTOU demo."""

import time


class Account:
    def __init__(self, initial_balance: int = 100) -> None:
        self.balance = initial_balance

    def withdraw(self, amount: int) -> bool:
        # Check and use are separate: another thread can spend the same balance
        # after this check but before this thread writes its calculated balance.
        observed_balance = self.balance
        if amount <= 0 or observed_balance < amount:
            return False
        time.sleep(0.005)
        self.balance = observed_balance - amount
        return True
