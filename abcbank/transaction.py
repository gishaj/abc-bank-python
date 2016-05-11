from datetime import datetime


class Transaction:
    def __init__(self, amount):
        self.amount = amount

    # Constructor to add txns of an older date
    def __init__(self, amount, txnDate=None):
    	self.amount = amount
    	if txnDate:
	    	self.transactionDate = txnDate
    	else:
	        self.transactionDate = datetime.now()
