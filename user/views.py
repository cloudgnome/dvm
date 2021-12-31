from django.shortcuts import render,redirect
from user.models import User,AnonymousUser,PassCode
from django.views.generic import View
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from user.forms import SignInForm,SignUpForm,ForgetPassForm,ChangePasswordForm
from django.contrib.auth.signals import user_logged_out
from django.http import JsonResponse
from django.utils import timezone
from json import loads,dumps
from base64 import b64decode
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

__all__ = ['ChangePasswordView','forget_pass','signup','SigninView','signout','EditView']

class ChangePasswordView(View):
    def get(self, request, *args, **kwargs):
        if 'password' in request.GET and 'phone' in request.GET:
            try:
                user = User.objects.get(phone=request.GET['phone'])
                try:
                    password = PassCode.objects.get(code=request.GET['password'])
                    user.backend = 'user.backends.ModelBackend'
                    login(request, user)
                    return redirect('/user/change-password')
                except:
                    raise Http404('Не сошлись данные пароля')
            except Exception:
                raise Http404('Не сошлись данные')
        if request.user.is_authenticated:
            context = {}
            context['title'] = 'Смена пароля'
            context['form'] = ChangePasswordForm()
            if 'result' in context:
                del context['result']
            return render(request,'change-password.html',context)
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
                user.password = encrypt(context['form'].cleaned_data['password1'])
                user.save()
                user.backend = 'user.backends.ModelBackend'
                login(request, user)
                return redirect('/activity')
            return render(request,'%s/change-password.html' % request.folder,context)
        else:
            return redirect('/')

def forget_pass(request):
    form = ForgetPassForm()
    if request.POST:
        form = ForgetPassForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(phone=form.cleaned_data['phone'])
            except Exception:
                return render(request, 'forget_password.html',{'form':form,'error':'Пользователь не найден.'})

            passcode = PassCode()
            passcode.code = User.make_random_password()
            passcode.save()
            user.restore_password(passcode.code)
            return render(request, 'forget_password.html')

    return render(request, 'forget_password.html',{'form':form})

class EditView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_anonymous:
            return redirect('/user/signin/')

        try:
            request.user.country = Country.objects.get(id=request.user.country_id).name.replace('ru=','')
        except:
            pass
        try:
            request.user.city = City.objects.get(id=request.user.city_id).name.replace('ru=','')
        except:
            pass

        return render(request,'edit.html',{'view':'EditView'})

    def post(self,request,*args,**kwargs):
        form = EditForm(loads(request.body))
        if form.is_valid():
            extended = loads(request.user.extended)
            extended['profile'].update(form.cleaned_data)
            request.user.birthday = form.cleaned_data['birthday']
            request.user.country_id = form.cleaned_data['country_id']
            request.user.city_id = form.cleaned_data['city_id']
            request.user.extended = dumps(extended)
            request.user.save()
            return JsonResponse({'result':True})

        return JsonResponse({'result':False,'errors':form.errors})

def signup(request):
    if request.POST:
        data = loads(request.body)
        form = SignUpForm(data)
    else:
        form = SignUpForm()

    return render(request,'signup.html',{})

def signout(request):
    user = getattr(request, 'user', None)
    if hasattr(user, 'is_authenticated') and not user.is_authenticated:
        user = None
    user_logged_out.send(sender=user.__class__, request=request, user=user)

    if hasattr(request, 'user'):
        request.user = AnonymousUser()

    request.session.flush()

    if request.is_ajax():
        return JsonResponse({'result':1})
    else:
        return redirect('/')

def encrypt(password):
    import subprocess

    # if you want output
    proc = subprocess.Popen("php /var/www/meetap.ru/test.php " + password, shell=True, stdout=subprocess.PIPE)
    return proc.stdout.read().decode('utf8')

class SigninView(View):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        count = str(User.objects.count()) + '158'
        self.count = ' '.join([count[i:i+3] for i in range(0, len(count), 3)])

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('/activity')

        return render(request,'signin.html',{'count':self.count,'form':SignInForm()})

    def post(self,request,*args,**kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            user = self.authenticate(request.POST.get('login'), request.POST.get('password'))
            if user:
                login(request,user)
                return redirect('/activity')
            else:
                form.errors.update({'password':'<div class="error"><svg><use xlink:href="#errorTriangleIcon"></use></svg>Неправильный логин или пароль.</div>'})

        return render(request,'signin.html',{'form':form,'count':self.count})

    def authenticate(self, login, password):
        password = encrypt(password)
        try:
            user = User.objects.get(phone = login)
        except User.DoesNotExist:
            return None
        if password == user.password:
            user.backend = 'user.backends.ModelBackend'
            user.activity = int(timezone.now().timestamp())
            user.save()
            return user

        return None

        # http://meetap.ru/api/?method=applove.account.login&login=380976415441&password=qwerty&language=ru