from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.core.exceptions import ObjectDoesNotExist


from .models import User, Auction_listings, Wishlist, bids, comments


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Auction_listings.objects.all()
    })

def boughtlist(request):
    return render(request, "auctions/itemsBought.html", {
        "listings": Auction_listings.objects.all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

#form to insert a new listing
class newlistform(forms.ModelForm):
    class Meta:
        model=Auction_listings
        fields=["userid","title","description","startingprice"]

#create a new item listing from the form
def newlist(request):
    if request.method == "POST":
        form=newlistform(request.POST)
        if form.is_valid():
            entry=form.save()
            return redirect("listing", listing_id=entry.id)
    else:
        form= newlistform()
    return render(request, "auctions/newlist.html", {
        "form": form
    })



#wishlist implementation? da decidere come fare
@login_required
def wishlistpage(request):
    try:
        mywishlist = Wishlist.objects.get(userid=request.user)
    except ObjectDoesNotExist:
        mywishlist=None
    if mywishlist:
        return render(request, "auctions/wishlist.html", {
            "wishlist": mywishlist.itemid.all()
        })
    else:
        return render(request, "auctions/wishlist.html", {
            "wishlist": mywishlist
        })


#add to wishlist implementation via a button in the item page
@login_required
def add_wishlist(request, listing_id):
    listing= Auction_listings.objects.get(pk=listing_id)
    wishlist, created=Wishlist.objects.get_or_create(userid=request.user)
    wishlist.itemid.add(listing)
    return redirect("listing", listing_id=listing_id)


class bidding_form(forms.Form):
    bidprice= forms.DecimalField(label="bid price", min_value=0.01)

@login_required
def add_bidding(request, listing_id):
    #retrieving the listing with the given id from the db
    listing=Auction_listings.objects.get(id=listing_id)
    #retrieving the highest bid if it exists
    highestBid=listing.bidsreceived.order_by("-bidprice").first()
    #form stuff
    if request.method=="POST":
        #initializing a form variable that has inside the content of the form
        form=bidding_form(request.POST)
        if form.is_valid():
            bidPrice=form.cleaned_data["bidprice"]
            #checking if the bid inserted from the user is higher than the starting price and all the other bids if there are
            if bidPrice > listing.startingprice and (not highestBid or bidPrice > highestBid.bidprice):
                #creating a new instance and saving it to the db with the bid now that i've checked it is the highest
                bid = bids.objects.create(listingid=listing, userid=request.user, bidprice=bidPrice)
                return redirect("listing", listing_id=listing_id)
    else:
        form= bidding_form()
    return render(request, "auctions/bidding.html", {
        "listing":listing,
        "form": form
    })

@login_required
def EndAuction(request, listing_id):
    #retrieving the listing with the given id from the db
    listing=Auction_listings.objects.get(id=listing_id)
    if request.user.is_authenticated and listing.userid == request.user and listing.active:
        highest_bid= listing.bidsreceived.order_by("-bidprice").first()
        #if highest bid exists so checking if i was able to retrieve it from the db
        if highest_bid:
            #set the winner of the bid
            winner= highest_bid.userid
            listing.winner=winner
            listing.finalPrice=highest_bid
            #set the listing as inactive so it doesn't show in the auction page
            listing.active= False
            listing.save()
            #winning allert
            messages.success(request, f"{winner} has won the auction for {listing.title}")

            #redirect to the deactivated listing page 
            return redirect("listing", listing_id=listing.id)
        else:
            messages.error(request, "no bids placed for this item")
    #error management when i finish setting the rest instead of just redirecting to the index... maybe
    return redirect("index")

#form declaration where to add comments?
class commentForm (forms.ModelForm):
    class Meta:
        model = comments
        fields = ["commenttext"]

#render the page showing the listing of the item with the given id
def listing(request, listing_id):
    #retrieving the listing with the given id from the db
    listing=Auction_listings.objects.get(id=listing_id)
    #retrieving the highest bid if it exists
    highestBid=listing.bidsreceived.order_by("-bidprice").first()
    #get comments
    comments= listing.commentsposted.all()
    form=commentForm()
    if request.method== "POST":
        form=commentForm(request.POST)
        if form.is_valid():
            #saving the comment but waiting to upload the save on the db to add the missing fields
            comment = form.save(commit=False)
            #assigning the current user id to the comment made
            comment.userid = request.user
            #assigning the current listing page id to the comment made
            comment.listingid = listing
            #uploading to the db
            comment.save()
            return redirect("listing", listing_id=listing_id)
    #return the rendered page
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "highestBid": highestBid,
        "comments": comments
    })



#manage comments?
def commentrender(request):
    None