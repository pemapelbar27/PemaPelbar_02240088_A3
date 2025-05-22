import unittest
from PemaPelbar_02240088_A3_PA import BankAccount, TransferError, InvalidInputError

class TestBankApp(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount("001", "Alice", 100.0)

    def test_deposit(self):
        self.account.deposit(50)
        self.assertEqual(self.account.balance, 150)

    def test_deposit_negative(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-20)

    def test_withdraw_valid(self):
        self.account.withdraw(40)
        self.assertEqual(self.account.balance, 60)

    def test_withdraw_over_balance(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(200)

    def test_transfer_valid(self):
        target = BankAccount("002", "Bob", 50)
        self.account.transfer(target, 30)
        self.assertEqual(self.account.balance, 70)
        self.assertEqual(target.balance, 80)

    def test_transfer_invalid_target(self):
        with self.assertRaises(TransferError):
            self.account.transfer("not_account", 10)

    def test_top_up_phone(self):
        msg = self.account.top_up_phone("08123456789", 20)
        self.assertEqual(msg, "Topped up 20 to 08123456789")
        self.assertEqual(self.account.balance, 80)

    def test_top_up_insufficient_balance(self):
        with self.assertRaises(ValueError):
            self.account.top_up_phone("08123456789", 500)

    def test_delete_account(self):
        self.assertEqual(self.account.delete_account(), "Account deleted")


    unittest.main()
