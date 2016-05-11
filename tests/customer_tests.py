from nose.tools import assert_equals, nottest

from abcbank.account import SavingsAc, CheckingAc, MaxiSavingsAc
from abcbank.customer import Customer

from datetime import datetime

class TestCustomer:

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_statement(self):
        checkingAccount = CheckingAc()
        savingsAccount = SavingsAc()
        henry = Customer("Henry").openAccount(checkingAccount).openAccount(savingsAccount)
        checkingAccount.deposit(100.0)
        savingsAccount.deposit(4000.0)
        savingsAccount.withdraw(200.0)
        assert_equals(henry.getStatement(),
                      "Statement for Henry" +
                      "\n\nChecking Account\n  deposit $100.00\nTotal $100.00" +
                      "\n\nSavings Account\n  deposit $4000.00\n  withdrawal $200.00\nTotal $3800.00" +
                      "\n\nTotal In All Accounts $3900.00")


    def test_oneAccount(self):
        oscar = Customer("Oscar").openAccount(SavingsAc())
        assert_equals(oscar.numAccs(), 1)


    def test_twoAccounts(self):
        oscar = Customer("Oscar").openAccount(SavingsAc())
        oscar.openAccount(CheckingAc())
        assert_equals(oscar.numAccs(), 2)


    # @nottest
    # Enable this test case
    def test_threeAccounts(self):
        oscar = Customer("Oscar").openAccount(SavingsAc())
        oscar.openAccount(CheckingAc())
        oscar.openAccount(MaxiSavingsAc())
        assert_equals(oscar.numAccs(), 3)

    def test_transfer(self):
        checkingAccount = CheckingAc()
        savingsAccount = SavingsAc()
        oscar = Customer("Oscar").openAccount(checkingAccount)
        oscar.openAccount(savingsAccount)
        checkingAccount.deposit(100.0)
        savingsAccount.deposit(4000.0)
        savingsAccount.withdraw(200.0)
        todayDate = datetime.now()
        savingsAccount.transfer(500.0, checkingAccount, todayDate)
        assert_equals(oscar.getStatement(),
                      "Statement for Oscar" +
                      "\n\nChecking Account\n  deposit $100.00\n  deposit $500.00\nTotal $600.00" +
                      "\n\nSavings Account\n  deposit $4000.00\n  withdrawal $200.00\n  withdrawal $500.00\nTotal $3300.00" +
                      "\n\nTotal In All Accounts $3900.00")
