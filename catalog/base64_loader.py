from django.core.files.base import ContentFile
from base64 import b64decode
from user.models import User

def load_image(code):
    name = User.make_random_password(length=16)
    if 'data:image/jpeg;base64' in code:
        return ContentFile(b64decode(code.replace('data:image/jpeg;base64,','')), name='{}.{}'.format(name,'jpg'))
    elif 'data:image/png;base64' in code:
        return ContentFile(b64decode(code.replace('data:image/png;base64,','')), name='{}.{}'.format(name,'png'))

