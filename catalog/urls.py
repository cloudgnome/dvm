from django.urls import re_path
from catalog.views import *
from user.decorators import login_required

urlpatterns = [
    re_path(r'^category/(?P<model>[A-Za-z]+)/(?P<category_id>[0-9]+)$',category),
    re_path(r'^add/offer$',login_required(AddOfferView.as_view())),
    re_path(r'^add/auction$',login_required(AddAuctionView.as_view())),
    re_path(r'^auctions$',auctions),
    re_path(r'^match/(?P<model>[a-z]+)$',match),
    re_path(r'^offer/(?P<id>[0-9]+)$',offer),
    re_path(r'^auction/(?P<id>[0-9]+)$',auction),
    re_path(r'^add/image/(?P<model>[A-Za-z]+)/(?P<id>[0-9]+)',login_required(add_image)),
    re_path(r'^remove/image/(?P<model>[A-Za-z]+)/(?P<id>[0-9]+)',login_required(remove_image)),
    re_path(r'^edit/(?P<model>[A-Za-z]+)/(?P<id>[0-9]+)',login_required(EditView.as_view())),
    re_path(r'^', offers),
]