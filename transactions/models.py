from django.db import models
from django.db.models.signals import pre_save
from fbc.utils import unique_slug_generator,unique_id_generator
from accounts.models import DBKAccount
from profiles.models import Profile

# Create your models here.
class Transaction(models.Model):
    transaction_id = models.CharField(max_length=120, blank=True)
    slug = models.SlugField(blank=True, null=True,unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug

def transaction_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
       
pre_save.connect(transaction_pre_save_receiver, sender=Transaction)


class TransactionItem(models.Model):
    sender = models.ForeignKey(DBKAccount, on_delete=models.CASCADE,null=True)
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(blank=True, null=True,unique=True)
    token_quantity = models.DecimalField(max_digits=1000000, null=True, decimal_places=2)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return self.slug

def transactionitem_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(transactionitem_pre_save_receiver, sender=TransactionItem)
