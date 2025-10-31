from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Wallet: {self.balance}"

    def deposit(self, amount):
        """Add money to the wallet."""
        self.balance += amount
        self.save()
        WalletTransaction.objects.create(wallet=self, transaction_type='DEPOSIT', amount=amount)

    def withdraw(self, amount):
        """Remove money from the wallet if enough balance."""
        if self.balance < amount:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        self.save()
        WalletTransaction.objects.create(wallet=self, transaction_type='WITHDRAW', amount=amount)


class WalletTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdraw'),
    ]
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.wallet.user.username} - {self.transaction_type}: {self.amount}"
