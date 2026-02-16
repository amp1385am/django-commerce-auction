from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Listing, User, Category, Bid, Comment
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required


def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html",{
        "listings":listings
    })
    

def listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    highest_bid = listing.bids.order_by("-amount").first()
    current_price = highest_bid.amount if highest_bid else listing.starting_bid

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_price": current_price,
        "highest_bid": highest_bid
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

@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category_id = request.POST.get("category")

        category = Category.objects.get(id=category_id) if category_id else None

        Listing.objects.create(
            title=title,
            description=description,
            starting_bid=starting_bid,
            image_url=image_url,
            category=category,
            owner=request.user
        )
        return redirect("index")

    return render(request, "auctions/create.html", {
        "categories": Category.objects.all()
    })

@login_required
def place_bid(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, id=listing_id)
        bid_amount = float(request.POST["bid"])
        
        highest_bid = listing.bids.order_by("-amount").first()
        current_price = highest_bid.amount if highest_bid else listing.starting_bid
        
        if bid_amount <= current_price:
            return render(request, "auctions/listing.html", {
                "listing":listing,
                "error": "Your bid must be higher than current price."
            })
        Bid.objects.create(
            user=request.user,
            listing=listing,
            amount=bid_amount
        )
        
        return redirect("listing", listing_id=listing.id)
    
@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    
    if request.user != listing.owner:
        return redirect("listing", listing_id=listing.id)
    
    highest_bid = listing.bids.order_by("-amount").first()
    if highest_bid:
        listing.winner = highest_bid.user
        
    if request.user == listing.owner:
        listing.is_active = False
        listing.save()
    
    return redirect("listing", listing_id=listing.id)

@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == "POST":
        text = request.POST.get("comment")

        Comment.objects.create(
            user=request.user,
            listing=listing,
            text=text
        )

    return redirect("listing", listing_id=listing.id)


@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.user in listing.watchlist.all():
        listing.watchlist.remove(request.user)
    else:
        listing.watchlist.add(request.user)

    return redirect("listing", listing_id=listing.id)

@login_required
def watchlist(request):
    listings = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })
