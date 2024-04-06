from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction_listings(models.Model):
    #id of the user inserting the listing should be automatically retrieved from the user account (table)
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.TextField( max_length = 50 )
    description = models.TextField( max_length = 200 )
    #price in cents? i'll see in the future and change it in a more readable way
    startingprice = models.IntegerField()
    #image? to add
    
    def __str__(self):
        return f"{self.userid} listed {self.title} description: {self.description} price: {self.startingprice/100}"



class bids(models.Model):
    #id of the user making the bid it should be automatically retrieved from the user account (table)
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidsmade")
    #id of the listing the bid is for many to 1 relationship? the listing can have many bids
    listingid = models.ForeignKey(Auction_listings, on_delete=models.CASCADE, related_name="bidsreceived")
    bidprice = models.IntegerField()

    def __str__(self):
        return f"{self.userid} bids for: {self.listingid} an offer of: {self.bidprice/100}"


class comments(models.Model):
    #id of the user making the comment it should be automatically retrieved from the user account (table)
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentsmade")
    commenttext = models.TextField( max_length = 200 )
    listingid = models.ForeignKey(Auction_listings, on_delete=models.CASCADE, related_name="commentsposted")

    def __str__(self):
        return f"{self.userid} comments: {self.commenttext} to: {self.listingid}"


#da vedere bene se la relazione funziona
class wishlist(models.Model):
    userid= models.ForeignKey(User, on_delete=models.CASCADE, related_name="wisher")
    listingid= models.ForeignKey(Auction_listings, on_delete=models.CASCADE, related_name="wished")
