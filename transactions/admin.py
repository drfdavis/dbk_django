from django.contrib import admin

# Register your models here.
from .models import Transaction, TransactionItem

admin.site.register(Transaction)
admin.site.register(TransactionItem)