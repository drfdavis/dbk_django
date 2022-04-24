from django.contrib import admin

# Register your models here.
from .models import Transaction, TransactionItem

admin.site.register(Transaction)



class TransactionItemAdmin(admin.ModelAdmin):
    list_display = ['sender','receiver','transaction','token_quantity','is_active']
     

admin.site.register(TransactionItem,TransactionItemAdmin)