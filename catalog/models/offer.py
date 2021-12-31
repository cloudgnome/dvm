from django.db import models
from catalog.models import Category,AbstractGallery
from user.models import User
from django.utils.translation import ugettext_lazy as _

class Offer(models.Model):
    name = models.CharField(max_length=255)
    sold = models.BooleanField(default=0)
    price = models.PositiveIntegerField()
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    location_text = models.CharField(max_length=255)
    place_id = models.CharField(max_length=255,null=True)
    location_lat = models.FloatField(null=True)
    location_lng = models.FloatField(null=True)
    condition_choices = (
        (1,_('New')),
        (2,_('Used')),
    )
    condition = models.PositiveIntegerField(choices=condition_choices,default=1)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    @property
    def gallery_list(self):
        return [{'id':image.id,'image':image.url} for image in self.gallery.all()]

    class Meta:
        ordering = ['-id']

class Offer_Gallery(AbstractGallery):
    related = models.ForeignKey(Offer,on_delete=models.CASCADE,related_name='gallery')
    size = 500

    class Meta:
        verbose_name = _('Offer gallery')
        verbose_name_plural = _('Offer gallery')
        ordering = ['-id']