from django.shortcuts import render
from profiles.models import Profile
from .models import Transaction, TransactionItem
from django.conf import settings 

user = settings.AUTH_USER_MODEL

def _tranaction_id(request):
    transaction = request.session.session_key
    if not transaction:
        transaction = request.session.create()
    return transaction


# Create your views here.
def sendToken(request):
    sender = request.user
    if request.method == 'POST':
        receiver = request.POST['receiver']
        tokens_qty = request.POST['token_amount']

        receiver_profile = Profile.objects.get(user__username=receiver)#.user#.username
        
       
        # print('Sender token:',sender.profile.tokens)
        # print('receiver token:',receiver_profile.tokens)

        try:
            transaction = Transaction.objects.get(transaction_id=_tranaction_id(request))
        except Transaction.DoesNotExist:
            transaction = Transaction.objects.create(transaction_id=_tranaction_id(request))
        transaction.save()

        transaction_item = TransactionItem.objects.create(sender=sender,receiver=receiver_profile,transaction=transaction,token_quantity=tokens_qty)
        transaction_item.save()

    
    return render(request,'transactions/sendtokenform.html')   