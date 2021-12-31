from django.shortcuts import render,redirect
from user.models import User,PassCode
from django.views.generic import View
from django.contrib.auth import login
from user.forms import ChangePasswordForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.utils import timezone
from datetime import timedelta

class ChangePasswordView(View):
    def get(self, request, *args, **kwargs):
        if 'code' in request.GET:
            try:
                code = PassCode.objects.get(code=request.GET['code'],created_at__gte=timezone.now() - timedelta(minutes=15))
                try:
                    user = User.objects.get(email=code.email)
                except User.DoesNotExist:
                    raise Http404('Пользователь не найден')
                user.backend = 'user.backends.ModelBackend'
                login(request, user)
            except PassCode.DoesNotExist:
                raise Http404('Код не найден')
            if user.is_active:
                context = {}
                context['title'] = 'Смена пароля'
                context['form'] = ChangePasswordForm()
                if 'result' in context:
                    del context['result']
                return render(request,'user/auth/change-password.html',context)
            else:
                return redirect('/')
        else:
            return redirect('/')

    @method_decorator(login_required)
    def post(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            context = {}
            context['title'] = 'Смена пароля'
            context['form'] = ChangePasswordForm(request.POST)
            if context['form'].is_valid():
                user = request.user
                user.set_password(context['form'].cleaned_data['password1'])
                user.save()
                return redirect('/')
            return render(request,'user/auth/change-password.html',context)
        else:
            return redirect('/')