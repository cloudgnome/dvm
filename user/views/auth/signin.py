from django.shortcuts import render,redirect
from user.models import User
from django.views.generic import View
from user.auth import login
from user.forms import SignInForm
from django.utils import timezone
from django.contrib.auth.hashers import check_password

class SignInView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('/')

        return render(request,'user/auth/signin.html',{'form':SignInForm()})

    def post(self,request,*args,**kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            user,error = self.authenticate(request.POST.get('login'), request.POST.get('password'))
            if user and not user.is_active:
                request.session['email'] = user.email
                return redirect('/user/activate?resend=true')
            if user:
                login(request,user)
                return redirect('/')
            form.errors.update({'password':error})

        return render(request,'user/auth/signin.html',{'form':form})

    def authenticate(self, login, password):
        try:
            user = User.objects.get(email=login)
        except User.DoesNotExist:
            return None,'Пользователь не найден'
        if user and check_password(password,user.password):
            user.backend = 'user.backends.ModelBackend'
            # user.activity = int(timezone.now().timestamp())
            # user.save()
            return user,None

        return None,'Пароль не подошел'