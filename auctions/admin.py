from django.contrib import admin

from .models import User,Auction_listings,comments,bids
# Register your models here.

admin.site.register(User)
admin.site.register(Auction_listings)
admin.site.register(comments)
admin.site.register(bids)