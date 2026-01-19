from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from decimal import Decimal

class CustomUser(AbstractUser):
    """Extended user model with role-based access"""
    ROLE_CHOICES = [
        ('STUDENT', 'Student'),
        ('ADMIN', 'Administrator'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    grade = models.CharField(max_length=10, blank=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Wallet(models.Model):
    """Financial account for each user"""
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='wallet'
    )
    balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]  # Prevent negative balance
    )
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
    
    def __str__(self):
        return f"{self.user.username}'s Wallet (₹{self.balance})"
    
    def has_sufficient_balance(self, amount):
        """Check if user can afford a transaction"""
        return self.balance >= Decimal(str(amount))


class Transaction(models.Model):
    """Immutable ledger of all financial operations"""
    TRANSACTION_TYPES = [
        ('CREDIT', 'Admin Credit'),
        ('PURCHASE', 'Item Purchase'),
        ('REFUND', 'Refund'),
        ('PENALTY', 'Penalty Deduction'),
    ]
    
    sender = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='sent_transactions'
    )
    receiver = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='received_transactions'
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-timestamp']  # Newest first
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['receiver', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - ₹{self.amount} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class InventoryItem(models.Model):
    """Products available in the campus shop"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    stock_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(upload_to='inventory/', blank=True, null=True)
    category = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Inventory Item'
        verbose_name_plural = 'Inventory Items'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} (₹{self.price}) - Stock: {self.stock_quantity}"
    
    def is_in_stock(self):
        """Check if item is available for purchase"""
        return self.stock_quantity > 0 and self.is_active
