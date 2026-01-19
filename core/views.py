from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from decimal import Decimal
from .models import CustomUser, Wallet, Transaction, InventoryItem

def index(request):
    return render(request, 'index.html')

@login_required
@transaction.atomic
def purchase_item(request, item_id):
    """Handle item purchase with financial safety"""
    user = request.user
    
    try:
        # Lock the item row to prevent concurrent stock modifications
        item = InventoryItem.objects.select_for_update().get(id=item_id)
        
        # Lock the wallet row to prevent concurrent balance modifications
        # We need to explicitly select the wallet here to lock it
        wallet = Wallet.objects.select_for_update().get(user=user)
        
        # Validate purchase conditions
        if not item.is_in_stock():
            messages.error(request, f"{item.name} is out of stock.")
            return redirect('student_dashboard')
        
        if not wallet.has_sufficient_balance(item.price):
            messages.error(request, "Insufficient balance.")
            return redirect('student_dashboard')
        
        # 1. Deduct tokens from wallet
        wallet.balance -= item.price
        wallet.save()
        
        # 2. Reduce inventory stock
        item.stock_quantity -= 1
        item.save()
        
        # 3. Record transaction
        Transaction.objects.create(
            sender=user,
            receiver=None,  # System purchase
            amount=item.price,
            transaction_type='PURCHASE',
            description=f"Purchased {item.name}"
        )
        
        messages.success(request, f"Successfully purchased {item.name}!")
        return redirect('student_dashboard')
    
    except InventoryItem.DoesNotExist:
        messages.error(request, "Item not found.")
        return redirect('student_dashboard')
    except Wallet.DoesNotExist:
        messages.error(request, "Wallet not found.")
        return redirect('student_dashboard')
    except Exception as e:
        messages.error(request, f"Purchase failed: {str(e)}")
        return redirect('student_dashboard')


@login_required
def student_dashboard(request):
    """Student wallet and recent transactions"""
    if request.user.role != 'STUDENT':
        return redirect('admin_dashboard')
    
    # Ensure wallet exists
    wallet, created = Wallet.objects.get_or_create(user=request.user)

    # Get transactions where user is sender OR receiver
    recent_transactions = Transaction.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-timestamp')[:10]
    
    # Get active inventory items
    inventory_items = InventoryItem.objects.filter(is_active=True)
    
    context = {
        'wallet': wallet,
        'transactions': recent_transactions,
        'inventory_items': inventory_items,
    }
    return render(request, 'student/dashboard.html', context)

@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        return redirect('student_dashboard')
    return render(request, 'admin/dashboard.html')

@login_required
def admin_users(request):
    if request.user.role != 'ADMIN':
        return redirect('student_dashboard')
    return render(request, 'admin/users.html')

@login_required
def admin_inventory(request):
    if request.user.role != 'ADMIN':
        return redirect('student_dashboard')
    return render(request, 'admin/shop.html') # Using shop.html as inventory management

@login_required
def admin_logs(request):
    if request.user.role != 'ADMIN':
        return redirect('student_dashboard')
    return render(request, 'admin/logs.html')

@login_required
def admin_settings(request):
    if request.user.role != 'ADMIN':
        return redirect('student_dashboard')
    return render(request, 'admin/settings.html')
