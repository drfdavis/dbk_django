from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request,'index.html')


def transhistory(request):
    return render(request,'history_table.html')