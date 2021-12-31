from django.conf.urls import url
from catalog.views import *
from user.decorators import login_required

urlpatterns = [
    url(r'^category/(?P<model>[A-Za-z]+)/(?P<category_id>[0-9]+)$',category),
    url(r'^add/offer$',login_required(AddOfferView.as_view())),
    url(r'^add/auction$',login_required(AddAuctionView.as_view())),
    url(r'^auctions$',auctions),
    url(r'^match/(?P<model>[a-z]+)$',match),
    url(r'^offer/(?P<id>[0-9]+)$',offer),
    url(r'^auction/(?P<id>[0-9]+)$',auction),
    url(r'^add/image/(?P<model>[A-Za-z]+)/(?P<id>[0-9]+)',login_required(add_image)),
    url(r'^remove/image/(?P<model>[A-Za-z]+)/(?P<id>[0-9]+)',login_required(remove_image)),
    url(r'^edit/(?P<model>[A-Za-z]+)/(?P<id>[0-9]+)',login_required(EditView.as_view())),
    url(r'^', offers),
]