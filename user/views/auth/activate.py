from django.shortcuts import render,redirect
from user.models import User,MailCode
from django.utils import timezone
from datetime import timedelta
from user.auth import login

def activate(request):
    if request.GET.get('code'):
        if request.user.is_active:
            return redirect('/')
        try:
            code = MailCode.objects.get(code=request.GET.get('code'),created_at__gte=timezone.now() - timedelta(minutes=15))
            try:
                user = User.objects.get(email=code.email)
            except User.DoesNotExist:
                code.delete()
                return redirect('/')

            user.is_active = True
            user.save()
            login(request,user)
            return render(request,'user/auth/activate.html',{'activated':True})
        except MailCode.DoesNotExist:
            pass

    if not request.session.get('email'):
        return redirect('/')

    if request.user.is_active:
        return redirect('/profile')

    if request.GET.get('resend') and request.session.get('email'):
        try:
            user = User.objects.get(email=request.session.get('email'))
        except User.DoesNotExist:
            del request.session['email']
            return redirect('/')
        request.user.verify(request.session.get('email'))

    return render(request,'user/auth/activate.html')