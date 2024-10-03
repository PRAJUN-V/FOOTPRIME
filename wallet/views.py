from django.shortcuts import render
from .models import Wallet
from django.contrib.auth.decorators import login_required

@login_required(login_url='home:signin')
def wallet(request):
    user_wallet, created = Wallet.objects.get_or_create(user=request.user, defaults={'balance': 0.00})
    return render(request,'wallet/wallet.html',{'balance': user_wallet.balance})
