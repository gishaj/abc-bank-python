from transaction import Transaction
import datetime

class Account(object):
    def __init__(self):
        self.transactions = []

    #Added account argument to allow deposit from another account
    # but no withdraw from another account;
    def deposit(self, amount, account=None):
        if (amount <= 0):
            raise ValueError("amount must be greater than zero")
        else:
            if account:
                account.transactions.append(Transaction(amount))
            else:
                self.transactions.append(Transaction(amount))

    def withdraw(self, amount):
        if (amount <= 0):
            raise ValueError("amount must be greater than zero")
        else:
            self.transactions.append(Transaction(-amount))

    #To allow a customer to transfer from one of his account to another
    def transfer(self, amount, toAccount):
        if (amount <= 0):
            raise ValueError("amount must be greater than zero")
        else:
            self.withdraw(amount)
            self.deposit(amount, toAccount)

    def interestEarned(self):
        pass

    def sumTransactions(self, checkAllTransactions=True):
        return sum([t.amount for t in self.transactions])

    def recentWithdrawal(self):
        lastWithdrawal = None
        for i in self.transactions:
            if i.amount < 0:
                if not lastWithdrawal:
                    lastWithdrawal = i.transactionDate
                elif lastWithdrawal < i.transactionDate:
                    lastWithdrawal = i.transactionDate
        if lastWithdrawal:
            last = lastWithdrawal - datetime.datetime.now()
            return ((last - 10) < 10)
        else:
            return False

class SavingsAc(Account):
    def interestEarned(self):
        amount = self.sumTransactions()
        if (amount <= 1000):
            return amount * 0.001
        else:
            return 1 + (amount - 1000) * 0.002

class CheckingAc(Account):
    def interestEarned(self):
        amount = self.sumTransactions()
        return amount * 0.001

class MaxiSavingsAc(Account):
    def interestEarned(self):
        amount = self.sumTransactions()
        if self.recentWithdrawal():
            return amount * 0.001
        else:
            return amount * 0.05
        # if (amount <= 1000):
        #     return amount * 0.02
        # elif (amount <= 2000):
        #     return 20 + (amount - 1000) * 0.05
        # else:
        #     return 70 + (amount - 2000) * 0.1
