from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlist", views.newlist, name="newlist"),
    path("wish", views.wishlistpage, name="wishlist"),
    path("itemsBought", views.boughtlist, name="myitemsBought"),
    path("add/<int:listing_id>", views.add_wishlist, name="addwishlistpage"),
    path("bidding/<int:listing_id>", views.add_bidding, name="userbid"),
    path("close/<int:listing_id>", views.EndAuction, name="endAuction"),
    path("<int:listing_id>", views.listing, name="listing"),
    
]
