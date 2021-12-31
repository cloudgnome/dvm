from django.db import models
from catalog.models import Category,AbstractGallery
from user.models import User
from django.utils.translation import ugettext_lazy as _

class Auction(models.Model):
    name = models.CharField(max_length=255)
    sold = models.BooleanField(default=0)
    start_price = models.PositiveIntegerField()
    buyout = models.PositiveIntegerField(null=True)
    bid_step = models.PositiveIntegerField(null=True)
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
    status_choices = (
        (1,_('Active')),
        (2,_('Ended')),
    )
    status = models.PositiveIntegerField(choices=status_choices,default=1)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    @property
    def gallery_list(self):
        return [{'id':image.id,'image':image.url} for image in self.gallery.all()]

    @property
    def max_bid(self):
        return self.bids.first() or self.start_price

    class Meta:
        ordering = ['-id']

class Auction_Bid(models.Model):
    auction = models.ForeignKey(Auction,related_name="bids",on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name="bids",on_delete=models.CASCADE)
    bid = models.PositiveIntegerField()

    def __str__(self):
        return self.bid

    class Meta:
        unique_together = ['auction','user']

class Auction_Gallery(AbstractGallery):
    related = models.ForeignKey(Auction,on_delete=models.CASCADE,related_name='gallery')
    size = 500

    class Meta:
        verbose_name = _('Auction gallery')
        verbose_name_plural = _('Auction gallery')
        ordering = ['-id']