"""Account that makes the balance check and update one locked operation."""

import threading


class Account:
    def __init__(self, initial_balance: int = 100) -> None:
        self.balance = initial_balance
        self._lock = threading.Lock()

    def withdraw(self, amount: int) -> bool:
        with self._lock:
            if amount <= 0 or self.balance < amount:
                return False
            self.balance -= amount
            return True
