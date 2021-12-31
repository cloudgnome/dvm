from django.db import models
from random import choice
from string import ascii_lowercase, digits
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from system.settings import BASE_URL,MEDIA_ROOT
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from PIL import Image, ImageEnhance
import os
from random import randint

class PassCode(models.Model):
    code = models.CharField(max_length=64,verbose_name='Код')
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    social_type_choices = (
            (1,'fb'),
            (2,'g')
        )
    social_type = models.PositiveIntegerField(choices=social_type_choices,null=True)
    social_id = models.CharField(max_length=255,null=True)
    is_active = models.BooleanField(default=False)
    balance = models.PositiveIntegerField(default=0)
    image = models.ImageField(max_length=255,upload_to='users/image/',null=True)
    phone = models.CharField(max_length=16,null=True)

    def image_path(name,size):
        path = 'users/image/%s/' % randint(1,10000)
        root = MEDIA_ROOT + path
        if not os.path.isdir(root):
            try:
                os.makedirs(root)
            except FileExistsError:
                pass
        return path + name + '%sx%s.jpg' % (size,size)

    def thumbnail(image):
        name = image.name
        image = Image.open(image)
        path = User.image_path(name,100)
        image.thumbnail([100,100])
        try:
            image = image.convert('RGBA')
            image.save(MEDIA_ROOT + path,'PNG')
        except:
            image = image.convert('RGB')
            image.save(MEDIA_ROOT + path,'JPEG')

        return path

    @property
    def image_url(self):
        try:
            return self.image.url
        except:
            return '/static/image/user_no_image.jpg'

    @property
    def full_name(self):
        return '%s %s' % (self.fname,self.lname)

    def restore_password(self,code):
        context = {'code':code,'BASE_URL':BASE_URL}
        subject, from_email, to = 'Восстановление пароля', "%s DVM-Market <info@%s>" % (BASE_URL,BASE_URL), self.email
        text_content,html_content = render_to_string('auth/recover.txt',context),render_to_string('auth/recover.html',context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def generate_name(length=16, chars=ascii_lowercase+digits, split=4, delimiter='-'):
    
        name = ''.join([choice(chars) for i in range(length)])
        
        if split:
            name = delimiter.join([name[start:start+split] for start in range(0, len(name), split)])
        
        try:
            User.objects.get(name=name)
            return generate_name(length=length, chars=chars, split=split, delimiter=delimiter)
        except User.DoesNotExist:
            return name

    def make_random_password(length=10,
                             allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                           'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                           '23456789'):
        """
        Generate a random password with the given length and given
        allowed_chars. The default value of allowed_chars does not have "I" or
        "O" or letters and digits that look similar -- just to avoid confusion.
        """
        return get_random_string(length, allowed_chars)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def __str__(self):
        return self.full_name

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True if self.is_active else False

    def verify(email):
        try:
            code = MailCode.objects.get(email=email,created_at__gte=timezone.now() - timedelta(minutes=15))
        except:
            MailCode.objects.filter(email=email).delete()
            code = MailCode.objects.create(email=email,code=User.make_random_password(length=50))

        context = {'code':code,'BASE_URL':BASE_URL}
        subject, from_email, to = 'Подтверждение email', "%s DVM-Market <info@%s>" % (BASE_URL,BASE_URL), email
        text_content,html_content = render_to_string('user/auth/verify.txt',context),render_to_string('user/auth/verify.html',context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
        except:
            pass

class MailCode(models.Model):
    code = models.CharField(max_length=50,verbose_name='Код')
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()

    def __str__(self):
        return self.code

class AnonymousUser:
    id = None
    pk = None
    name = ''
    is_staff = False
    is_active = False
    is_superuser = False
    # _groups = EmptyManager(Group)
    # _user_permissions = EmptyManager(Permission)

    def verify(self,email):
        User.verify(email)

    def __str__(self):
        return 'AnonymousUser'

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __hash__(self):
        return 1  # instances always return the same hash value

    def save(self):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def delete(self):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def set_password(self, raw_password):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def check_password(self, raw_password):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    @property
    def groups(self):
        return self._groups

    @property
    def user_permissions(self):
        return self._user_permissions

    def get_group_permissions(self, obj=None):
        return set()

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj=obj)

    def has_perm(self, perm, obj=None):
        return _user_has_perm(self, perm, obj=obj)

    def has_perms(self, perm_list, obj=None):
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, module):
        return _user_has_module_perms(self, module)

    @property
    def is_anonymous(self):
        return True

    @property
    def is_opt(self):
        return False

    @property
    def is_authenticated(self):
        return False

    def get_username(self):
        return self.name