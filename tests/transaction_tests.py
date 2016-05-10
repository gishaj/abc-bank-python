from nose.tools import assert_is_instance

from abcbank.transaction import Transaction

class TestCustomer:

    def setUp(self):
        pass

    def teatDown(self):
        pass

	def test_type():
	    t = Transaction(5)
	    assert_is_instance(t, Transaction, "correct type")