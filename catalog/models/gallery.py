from django.db import models
from PIL import Image
from system.settings import MEDIA_ROOT
import os
from random import randint
from django.utils.translation import gettext_lazy as _

class AbstractGallery(models.Model):
    image = models.ImageField(max_length=255,upload_to='data/company/%Y/%m/%d', blank=True,verbose_name=_('Image'))
    last_modified = models.DateTimeField(auto_now_add=True)

    @property
    def url(self):
        return self.image.url

    def __str__(self):
        return self.image.url

    def image_path(name,size):
        path = 'company/image/%s/' % randint(1,10000)
        root = MEDIA_ROOT + path
        if not os.path.isdir(root):
            try:
                os.makedirs(root)
            except FileExistsError:
                pass
        return path + name + '%sx%s.jpg' % (size,size)

    def thumbnail(image,size):
        name = image.name
        image = Image.open(image)
        path = AbstractGallery.image_path(name,size)
        image.thumbnail([size,size])
        try:
            image = image.convert('RGBA')
            image.save(MEDIA_ROOT + path,'PNG')
        except:
            image = image.convert('RGB')
            image.save(MEDIA_ROOT + path,'JPEG')

        return path

    class Meta:
        abstract = True