from nose.tools import assert_equals

from abcbank.account import SavingsAc, CheckingAc, MaxiSavingsAc
from abcbank.bank import Bank
from abcbank.customer import Customer

from datetime import datetime

class TestBank:

    def setUp(self):
        self.bank = Bank()

    def tearDown(self):
        pass

    def test_customer_summary(self):
        john = Customer("John").openAccount(SavingsAc())
        self.bank.addCustomer(john)
        assert_equals(self.bank.customerSummary(),
                      "Customer Summary\n - John (1 account)")

    def test_checking_account(self):
        checkingAccount = CheckingAc()
        bill = Customer("Bill").openAccount(checkingAccount)
        self.bank.addCustomer(bill)
        txnDate = datetime.strptime('May 1 2016  10:14AM', '%b %d %Y %I:%M%p')
        checkingAccount.deposit(100.0, txnDate)
        txnDate = datetime.strptime('May 5 2016  3:21PM', '%b %d %Y %I:%M%p')
        checkingAccount.deposit(200.0, txnDate)
        #since we moved over to daily interest and the total interest
        # is calculated on a daily basis, this value will change
        # assert_equals(self.bank.totalInterestPaid(), 0.1)
        assert_equals(self.bank.totalInterestPaid(), 1.0958904109589042e-05)


    def test_savings_account(self):
        savingsAccount = SavingsAc()
        self.bank.addCustomer(Customer("Bill").openAccount(savingsAccount))
        savingsAccount.deposit(1500.0)
        assert_equals(self.bank.totalInterestPaid(), 2.0)

    def test_maxi_savings_account(self):
        maxiSavingsAccount = MaxiSavingsAc()
        self.bank.addCustomer(Customer("Bill").openAccount(maxiSavingsAccount))
        maxiSavingsAccount.deposit(3000.0)
        # Different interest after maxi interst calculation logic is changed
        # assert_equals(self.bank.totalInterestPaid(), 170.0)
        assert_equals(self.bank.totalInterestPaid(), 150.0)

    def test_maxi_savings_account_recent_withdrawal(self):
        maxiSavingsAccount = MaxiSavingsAc()
        self.bank.addCustomer(Customer("Bill").openAccount(maxiSavingsAccount))
        maxiSavingsAccount.deposit(3000.0)
        maxiSavingsAccount.withdraw(100.0)
        # Different interest after maxi interst calculation logic is changed
        # assert_equals(self.bank.totalInterestPaid(), 170.0)
        assert_equals(self.bank.totalInterestPaid(), 2.9)
