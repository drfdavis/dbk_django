from django.shortcuts import render
from transactions.models import TransactionItem
# Create your views here.


def dashboard(request):
    return render(request,'index.html')


def transhistory(request):
    transactionItems = TransactionItem.objects.all()
    context = {
        "all_transactions":transactionItems
    }
    return render(request,'history_table.html', context)