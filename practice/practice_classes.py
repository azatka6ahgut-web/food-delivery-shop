class Wallet:
    def __init__(self, owner_name, balance, uni):
        self.owner_name = owner_name
        self.balance = balance

    def add_money(self, amount):
        self.balance = self.balance + amount

    def show_balance(self):
        print(f"У {self.owner_name} на счету {self.balance} рублей")

my_wallet = Wallet('Azat', 500)
print(my_wallet.show_balance)
print(my_wallet.add_money(500))
print(my_wallet.show_balance)

