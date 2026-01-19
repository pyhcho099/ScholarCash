from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Wallet, Transaction, InventoryItem

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Customized user management interface"""
    list_display = ['username', 'email', 'role', 'student_id', 'is_active']
    list_filter = ['role', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'student_id']
    
    fieldsets = UserAdmin.fieldsets + (
        ('ScholarCash Info', {'fields': ('role', 'student_id', 'grade')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('ScholarCash Info', {'fields': ('role', 'student_id', 'grade')}),
    )


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """Wallet management with inline actions"""
    list_display = ['user', 'balance', 'last_updated']
    search_fields = ['user__username', 'user__student_id']
    readonly_fields = ['last_updated']
    list_filter = ['last_updated']
    
    def has_delete_permission(self, request, obj=None):
        # Prevent accidental wallet deletion
        return False


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Read-only transaction ledger"""
    list_display = ['transaction_type', 'sender', 'receiver', 'amount', 'timestamp']
    list_filter = ['transaction_type', 'timestamp']
    search_fields = ['description', 'sender__username', 'receiver__username']
    readonly_fields = ['sender', 'receiver', 'amount', 'transaction_type', 'description', 'timestamp']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        # Transactions should only be created programmatically
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Transactions are immutable
        return False


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    """Product catalog management"""
    list_display = ['name', 'price', 'stock_quantity', 'category', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock_quantity', 'is_active']
