from django.shortcuts import render
from user.models import Payment

def payments(request):
    context = {
        'payments':Payment.objects.filter(user=request.user)
    }
    return render(request,'user/profile/payments.html',context)