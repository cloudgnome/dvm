from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _
from mptt import register

class Category(MPTTModel):
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name=_("Parent"),related_name="child",on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    type_choices = (
            (1,_('Price')),
            (2,_('Job')),
            (3,_('Business')),
            (4,_('Giveaway for Free')),
            (5,_('Swap')),
        )
    type = models.PositiveIntegerField(choices=type_choices,default=1)
    active = models.BooleanField(default=1)
    class_icon = models.CharField(max_length=20,null=True)
    offers_count = models.PositiveIntegerField(default=0)
    auctions_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

register(Category)