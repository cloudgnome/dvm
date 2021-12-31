from django.views.generic import View
from user.forms import SignUpForm,UserSocialForm
from user.models import User
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from json import loads
from requests import get
from system.settings import MEDIA_ROOT
import os
from transliterate import slugify

class SignUpView(View):
    path = '%susers/image/%s/'

    def email(self,json):
        social_type = dict(User.social_type_choices).get(json.get('social_type'))
        email = json.get('email')
        email = email if email else '%s%s@mail.ru' % (social_type,json.get('social_id'))

        return email

    def social_auth(self,request):
        json = loads(request.body.decode('utf-8'))
        user = False
        try:
            user = User.objects.get(social_type=json.get('social_type'),social_id=json.get('social_id'))
        except User.DoesNotExist:
            json['email'] = self.email(json)
            form = UserSocialForm(json)
            if form.is_valid():
                user = form.save()
                # if json.get('image'):
                #     image = self.save_image(json.get('image'),json.get('social_type'))
                #     user.image = image
                #     user.save()

        if user:
            return JsonResponse({'href':request.META.get('HTTP_REFERER','/')})
        else:
            return JsonResponse({'errors':form.errors})

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('/')

        context = {
            'form': SignUpForm(),
            'h1': _('Регистрация')
        }

        return render(request, 'user/auth/signup.html', context)

    def post(self,request,*args,**kwargs):
        try:
            json = loads(request.body.decode('utf-8'))
            if json.get('social'):
                return self.social_auth(request)
        except Exception as e:
            pass

        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            User.verify(user.email)
            request.session['email'] = user.email
            return redirect('/user/activate')
        else:
            context = {}
            context['form'] = form
            context['error'] = _('С полями формы что то не так.')
        return render(request, 'user/auth/signup.html', context)

    def save_image(self,src,type):
        href = src
        if type == 1:
            src = src.replace('https://pp.userapi.com/','').replace('/','').replace('-','')
        elif type == 2:
            src = src.replace('https://platform-lookaside.fbsbx.com/','').replace('/','').replace('-','')

        path = self.path % (MEDIA_ROOT,src[0:2])
        if not os.path.isdir(path):
            os.mkdir(path)
            os.chmod(path,0o777)
        image = slugify(src,language_code='uk') + ".jpg"
        path = path + image

        if not os.path.isfile(path):
            r = get(href)
            image = "users/image/%s/%s" % (src[0:2],image)
            with open(path, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)
        return image