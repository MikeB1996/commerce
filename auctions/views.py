from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import User, Auction_listings


def index(request):
    return render(request, "auctions/index.html", {
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

class newlistform(forms.ModelForm):
    class Meta:
        model=Auction_listings
        fields=["userid","title","description","startingprice"]


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


def listing(request, listing_id):
    listing=Auction_listings.objects.get(id=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing
    })


def wishlist():

    return