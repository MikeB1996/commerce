from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Auction_listings(models.Model):
    #id of the user inserting the listing should be automatically retrieved from the user account (table)
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField( max_length = 50 )
    description = models.TextField( max_length = 200 )
    #price in cents? i'll see in the future and change it in a more readable way
    startingprice = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    winner= models.ForeignKey(User, on_delete=models.SET_NULL, related_name="Auctions_won", blank=True, null=True)
    finalPrice=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    #image? to add
    
    def __str__(self):
        return f"{self.userid} listed {self.title} description: {self.description} price: {self.startingprice/100}"



class bids(models.Model):
    #id of the user making the bid it should be automatically retrieved from the user account (table)
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidsmade")
    #id of the listing the bid is for many to 1 relationship? the listing can have many bids
    listingid = models.ForeignKey(Auction_listings, on_delete=models.CASCADE, related_name="bidsreceived")
    bidprice = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.userid} bids for: {self.listingid} an offer of: {self.bidprice/100}"


class comments(models.Model):
    #id of the user making the comment it should be automatically retrieved from the user account (table)
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentsmade")
    commenttext = models.TextField( max_length = 200 )
    listingid = models.ForeignKey(Auction_listings, on_delete=models.CASCADE, related_name="commentsposted")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.userid} comments: {self.commenttext} to: {self.listingid} at: {self.created_at}"


#da vedere bene se la relazione funziona
class Wishlist(models.Model):
    userid= models.ForeignKey(User, on_delete=models.CASCADE, related_name="wisher")
    itemid= models.ManyToManyField(Auction_listings)

    def __str__(self):
        return f"{self.userid.username}'s wishlist"