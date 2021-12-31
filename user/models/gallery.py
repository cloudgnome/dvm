# -*- coding: utf-8 -*-
from django.db import models
from catalog.models import AbstractGallery
from user.models import Business
from django.utils.translation import ugettext_lazy as _

class Business_Gallery(AbstractGallery):
    related = models.ForeignKey(Business,on_delete=models.CASCADE,related_name='gallery')
    size = 100

    class Meta:
        verbose_name = _('Business gallery')
        verbose_name_plural = _('Business gallery')
        ordering = ['-id']