from nose.tools import assert_equals

from abcbank.account import SavingsAc, CheckingAc, MaxiSavingsAc
from abcbank.bank import Bank
from abcbank.customer import Customer

from datetime import datetime

# The following module is only available from python 3.3
# but can be used to mock today's date so that all tests 
# complete successfully
#
#
# import mock

# def mocked_get_now(timezone):
#     dt = datetime.strptime('May 10 2016  11:00PM', '%b %d %Y %I:%M%p')
#     return timezone.localize(dt)

#     @mock.patch('path.to.your.models.MyClass.get_now', side_effect=mocked_get_now)

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
        # is calculated on a daily basis, this result will change
        # assert_equals(self.bank.totalInterestPaid(), 0.1)
        assert_equals(self.bank.totalInterestPaid(), 0.00410958904109589)


    def test_savings_account(self):
        savingsAccount = SavingsAc()
        self.bank.addCustomer(Customer("Bill").openAccount(savingsAccount))
        txnDate = datetime.strptime('May 1 2012  10:14AM', '%b %d %Y %I:%M%p')
        savingsAccount.deposit(100.0, txnDate)
        assert_equals(self.bank.totalInterestPaid(), 0.40273972602739727)

    def test_maxi_savings_account(self):
        maxiSavingsAccount = MaxiSavingsAc()
        self.bank.addCustomer(Customer("Bill").openAccount(maxiSavingsAccount))
        txnDate = datetime.strptime('Feb 5 2012  4:21PM', '%b %d %Y %I:%M%p')
        maxiSavingsAccount.deposit(3000.0,txnDate)
        # Different interest after maxi interst calculation logic is changed
        # assert_equals(self.bank.totalInterestPaid(), 170.0)
        assert_equals(self.bank.totalInterestPaid(), 639.4520547945206)

    def test_maxi_savings_account_recent_withdrawal(self):
        maxiSavingsAccount = MaxiSavingsAc()
        self.bank.addCustomer(Customer("Bill").openAccount(maxiSavingsAccount))
        txnDate = datetime.strptime('Feb 5 2012  3:21PM', '%b %d %Y %I:%M%p')
        maxiSavingsAccount.deposit(200.0, txnDate)
        txnDate = datetime.strptime('Feb 5 2012  4:21PM', '%b %d %Y %I:%M%p')
        maxiSavingsAccount.deposit(3000.0, txnDate)
        # Putting a date in the future, which should fail elsewhere in the ideal
        # scenario, but this is to ensure that this test case passes for a longtime
        txnDate = datetime.strptime('May 9 2016  3:21PM', '%b %d %Y %I:%M%p')
        maxiSavingsAccount.withdraw(100.0, txnDate)
        assert_equals(self.bank.totalInterestPaid(), 0.008493150684931507)

    def test_maxi_savings_account_nonrecent_withdrawal(self):
        maxiSavingsAccount = MaxiSavingsAc()
        self.bank.addCustomer(Customer("Bill").openAccount(maxiSavingsAccount))
        txnDate = datetime.strptime('Feb 5 2012  3:21PM', '%b %d %Y %I:%M%p')
        maxiSavingsAccount.deposit(200.0, txnDate)
        txnDate = datetime.strptime('Feb 5 2012  4:21PM', '%b %d %Y %I:%M%p')
        maxiSavingsAccount.deposit(3000.0, txnDate)
        txnDate = datetime.strptime('Mar 19 2012  3:21PM', '%b %d %Y %I:%M%p')
        maxiSavingsAccount.withdraw(100.0, txnDate)
        assert_equals(self.bank.totalInterestPaid(), 642.5068493150685)
