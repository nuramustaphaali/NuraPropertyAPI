# apps/finance/admin.py
from django.contrib import admin
from .models import Transaction, Deal

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'user', 'amount', 'payment_method', 'status']
    list_filter = ['status', 'payment_method']
    search_fields = ['transaction_id', 'user__email']

class DealAdmin(admin.ModelAdmin):
    list_display = ['property', 'agent', 'final_price', 'commission_amount', 'date_closed']

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Deal, DealAdmin)