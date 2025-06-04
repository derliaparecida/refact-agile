# Replace Error Code With Exception
def withdraw(self, amount):
    if amount > self.balance:
        raise Exception("Insufficient funds")
    self.balance -= amount
    return 0
