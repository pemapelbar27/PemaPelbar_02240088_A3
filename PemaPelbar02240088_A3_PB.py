import unittest
from PemaPelbar_02240088_A3_PA import BankAccount, InvalidInputError, InsufficientBalanceError

class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.acc = BankAccount("Alice", 0, 100)
        self.target_acc = BankAccount("Bob", 50)

    # Unusual user input
    def test_deposit_zero(self):
        with self.assertRaises(InvalidInputError):
            self.acc.deposit(0)

    def test_deposit_negative(self):
        with self.assertRaises(InvalidInputError):
            self.acc.deposit(-10)

    def test_withdraw_zero(self):
        with self.assertRaises(InvalidInputError):
            self.acc.withdraw(0)

    def test_withdraw_negative(self):
        with self.assertRaises(InvalidInputError):
            self.acc.withdraw(-5)

    def test_top_up_invalid_phone(self):
        with self.assertRaises(InvalidInputError):
            self.acc.top_up_phone("abc123", 10)

    def test_top_up_short_phone(self):
        with self.assertRaises(InvalidInputError):
            self.acc.top_up_phone("12345", 10)

    def test_top_up_zero_amount(self):
        with self.assertRaises(InvalidInputError):
            self.acc.top_up_phone("0812345678", 0)

    # Invalid usage of functions
    def test_withdraw_insufficient_balance(self):
        with self.assertRaises(InsufficientBalanceError):
            self.acc.withdraw(200)

    def test_top_up_insufficient_balance(self):
        with self.assertRaises(InsufficientBalanceError):
            self.acc.top_up_phone("0812345678", 200)

    # Valid operations
    def test_deposit_valid(self):
        self.acc.deposit(50)
        self.assertEqual(self.acc.balance, 150)

    def test_withdraw_valid(self):
        self.acc.withdraw(40)
        self.assertEqual(self.acc.balance, 60)

    def test_top_up_phone_valid(self):
        msg = self.acc.top_up_phone("0812345678", 20)
        self.assertEqual(msg, "Phone 0812345678 topped up with Nu.20")
        self.assertEqual(self.acc.balance, 80)

if __name__ == "__main__":
    unittest.main()
