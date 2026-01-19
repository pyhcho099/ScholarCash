import os
import django
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarcash.settings')
django.setup()

from core.models import CustomUser, Wallet, Transaction, InventoryItem
from django.db.models import Q
from django.db import transaction

def verify_system():
    print("Setting up test data...")
    # Create test user
    user, created = CustomUser.objects.get_or_create(username='test_student', role='STUDENT')
    wallet, _ = Wallet.objects.get_or_create(user=user)
    wallet.balance = Decimal('100.00')
    wallet.save()
    
    # Create test item
    item, created = InventoryItem.objects.get_or_create(
        name='Test Notebook',
        defaults={'price': Decimal('10.00'), 'stock_quantity': 5}
    )
    
    print(f"Initial Balance: {wallet.balance}")
    print(f"Initial Stock: {item.stock_quantity}")
    
    # Simulate Purchase Logic (mimicking views.py)
    print("\nSimulating Purchase...")
    try:
        with transaction.atomic():
            # Lock rows (syntax check + logic)
            item = InventoryItem.objects.select_for_update().get(id=item.id)
            user_wallet = Wallet.objects.select_for_update().get(user=user)
            
            if item.stock_quantity > 0 and user_wallet.balance >= item.price:
                user_wallet.balance -= item.price
                user_wallet.save()
                
                item.stock_quantity -= 1
                item.save()
                
                Transaction.objects.create(
                    sender=user,
                    receiver=None,
                    amount=item.price,
                    transaction_type='PURCHASE',
                    description=f"Purchased {item.name}"
                )
                print("Purchase Successful!")
            else:
                print("Purchase Failed: conditions not met")
                
    except Exception as e:
        print(f"Transaction failed: {e}")

    # Verify Dashboard Query Logic
    print("\nVerifying Dashboard Logic...")
    recent_transactions = Transaction.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).order_by('-timestamp')[:10]
    
    found_purchase = False
    for t in recent_transactions:
        print(f"Found Transaction: {t}")
        if t.transaction_type == 'PURCHASE' and t.sender == user:
            found_purchase = True

    if found_purchase:
        print("SUCCESS: Purchase transaction correctly identified for dashboard.")
    else:
        print("FAILURE: Purchase transaction not found in dashboard query.")

if __name__ == "__main__":
    verify_system()
