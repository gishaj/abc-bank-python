from nose.tools import assert_equals

from abcbank.account import Account, CHECKING, MAXI_SAVINGS, SAVINGS
from abcbank.bank import Bank
from abcbank.customer import Customer

class TestAbcBank:

    def setUp(self):
        self.bank = Bank()

    def teatDown(self):
        pass

    def test_customer_summary(self):
        john = Customer("John").openAccount(Account(CHECKING))
        self.bank.addCustomer(john)
        assert_equals(self.bank.customerSummary(),
                      "Customer Summary\n - John (1 account)")


    def test_checking_account(self):
        checkingAccount = Account(CHECKING)
        bill = Customer("Bill").openAccount(checkingAccount)
        self.bank.addCustomer(bill)
        checkingAccount.deposit(100.0)
        assert_equals(self.bank.totalInterestPaid(), 0.1)


    def test_savings_account(self):
        self.bank = Bank()
        checkingAccount = Account(SAVINGS)
        bank.addCustomer(Customer("Bill").openAccount(checkingAccount))
        checkingAccount.deposit(1500.0)
        assert_equals(self.bank.totalInterestPaid(), 2.0)


    def test_maxi_savings_account(self):
        bank = Bank()
        checkingAccount = Account(MAXI_SAVINGS)
        self.bank.addCustomer(Customer("Bill").openAccount(checkingAccount))
        checkingAccount.deposit(3000.0)
        assert_equals(self.bank.totalInterestPaid(), 170.0)
