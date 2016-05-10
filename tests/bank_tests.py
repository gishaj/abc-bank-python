from nose.tools import assert_equals

from abcbank.account import SavingsAc, CheckingAc, MaxiSavingsAc
from abcbank.bank import Bank
from abcbank.customer import Customer

class TestBank:

    def setUp(self):
        self.bank = Bank()

    def teatDown(self):
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
        checkingAccount.deposit(100.0)
        assert_equals(self.bank.totalInterestPaid(), 0.1)


    def test_savings_account(self):
        savingsAccount = SavingsAc()
        self.bank.addCustomer(Customer("Bill").openAccount(savingsAccount))
        savingsAccount.deposit(1500.0)
        assert_equals(self.bank.totalInterestPaid(), 2.0)


    def test_maxi_savings_account(self):
        maxiSavingsAccount = MaxiSavingsAc()
        self.bank.addCustomer(Customer("Bill").openAccount(maxiSavingsAccount))
        maxiSavingsAccount.deposit(3000.0)
        assert_equals(self.bank.totalInterestPaid(), 170.0)
