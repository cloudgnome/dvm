var urlpatterns = {
    "^/user/profile$":{view:'ProfileView',menu:'/user/profile'},
    "^/chat/messages$":{view:'ChatView',menu:'/chat/messages'},
    "^/add/offer$":{view:'AddOfferView',menu:'/add/offer'},
    "^/auctions$":{view:'AuctionsView',menu:'/auctions'},
    "^/$":{view:'OffersView',menu:'/'},
    "^/offer/[0-9]+$":{view:'OfferView',menu:'/'},
    "^/auction/[0-9]+$":{view:'AuctionView',menu:'/auctions'},
    "^/edit/Offer/[0-9]+$":{view:'EditOffer',menu:'/edit/Offer'},
    "^/edit/Auction/[0-9]+$":{view:'AuctionOffer',menu:'/edit/Auction'},
    "^/category/Offer/[0-9]+$":{view:'Offers',menu:'/'},
    "^/category/Auction/[0-9]+$":{view:'Auctions',menu:'/auctions'},
};