from django.shortcuts import render
from user.models import User,PassCode
from user.forms import RecoverForm
from django.utils import timezone
from datetime import timedelta

def recover(request):
    form = RecoverForm()
    if request.POST:
        form = RecoverForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data['email'],is_active=True)
            except Exception:
                return render(request,'auth/recoverForm.html',{'form':form,'error':'Пользователь не найден.'})

            try:
                passcode = PassCode.objects.get(email=user.email,created_at__gte=timezone.now() - timedelta(minutes=15))
            except PassCode.DoesNotExist:
                PassCode.objects.filter(email=user.email).delete()
                passcode = PassCode.objects.create(code=User.make_random_password(length=64),email=user.email)

            user.restore_password(passcode)
            return render(request, 'auth/recoverForm.html')

    return render(request,'auth/recoverForm.html',{'form':form})