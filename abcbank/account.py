from transaction import Transaction
from datetime import datetime

class Account(object):
    def __init__(self):
        self.transactions = []

    #Added account argument to allow deposit from another account
    # but no withdraw from another account;
    def deposit(self, amount, txnDate=None, account=None):
        if (amount <= 0):
            raise ValueError("amount must be greater than zero")
        else:
            if account:
                account.transactions.append(Transaction(amount))
            elif account and txnDate:
                account.transactions.append(Transaction(amount, txnDate))
            elif txnDate:
                self.transactions.append(Transaction(amount, txnDate))
            else:
                self.transactions.append(Transaction(amount))

    def withdraw(self, amount, txnDate=None):
        if (amount <= 0):
            raise ValueError("amount must be greater than zero")
        elif self.sumTransactions() - amount < 0:
            raise ValueError("Insufficient Funds")
        elif txnDate:
            self.transactions.append(Transaction(-amount, txnDate))
        else:
            self.transactions.append(Transaction(-amount))

    #To allow a customer to transfer from one of his account to another
    def transfer(self, amount, toAccount, txnDate=None):
        if (amount <= 0):
            raise ValueError("amount must be greater than zero")
        else:
            self.withdraw(amount, txnDate)
            self.deposit(amount, txnDate, toAccount)

    def interestEarned(self):
        pass

    def sumTransactions(self, tillDate=None):
        if not tillDate:
            return sum([t.amount for t in self.transactions])
        txnSum = 0.0
        for txn in self.transactions:
            if txn.transactionDate < tillDate:
                txnSum += txn.amount;
        return txnSum

    def recentWithdrawal(self):
        lastWithdrawal = None
        for txn in self.transactions:
            if txn.amount < 0:
                if not lastWithdrawal:
                    lastWithdrawal = txn.transactionDate
                elif lastWithdrawal < txn.transactionDate:
                    lastWithdrawal = txn.transactionDate
        if lastWithdrawal:
            last = datetime.now() - lastWithdrawal
            return ((last.days - 10) < 10)
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
        # amount = self.sumTransactions()
        # return amount * 0.001
        totalInterest = 0.0
        
        for txnNum in range(len(self.transactions)):
            if txnNum:      #No interest with first transaction
                continue
            accruedAmt = self.sumTransactions(self.transactions[txnNum].transactionDate)
            # Add interest so far also to the current principal
            accruedAmt += totalInterest
            datesBetween  = self.transactions[txnNum].transactionDate - self.transactions[txnNum-1].transactionDate
            # Need to account for leap year later, 
            # as we need to include interests accrued in days
            # spread between say a leap and non leap year
            totalInterest = accruedAmt * datesBetween.days * 0.001 / 365

        #Calculate the interest from the last txn till today.
        daysLastTxn = (datetime.now() - self.transactions[len(self.transactions) -1].transactionDate).days
        totalInterest += self.sumTransactions() * daysLastTxn * 0.001 / 365

        return totalInterest




class MaxiSavingsAc(Account):
    def interestEarned(self):
        amount = self.sumTransactions()
        # Changing logic to have different interest rates
        # based on recent activity
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
