from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User,Bid,Listing,Wishlist,Comment,Category
from .forms import AuctionForm

def index(request):
    return render(request, "auctions/index.html",{"Listings": Listing.objects.all()})


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

def categories(request):
    return render(request, "auctions/categories.html",{"Categories": Category.objects.all()})


@login_required(login_url='/login')
def create_listing(request):
    if request.method=='POST':
        user=User.objects.get(username=request.user)
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.Price = 0
            listing.User = user
            if listing.Image_Link==None:
                listing.Image_Link="https://askleo.askleomedia.com/wp-content/uploads/2004/06/no_image-300x245.jpg"
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/new_listing.html", {
                "form": form
            })
    else:
        return render(request, "auctions/new_listing.html",{'form': AuctionForm()})

@login_required(login_url='/login')
def my_listing(request):
    user=User.objects.get(username=request.user)
    return render(request, "auctions/my_listings.html",{"Listings": Listing.objects.filter(User=user)})
 
@login_required(login_url='/login')
def watchlist(request):
    user=User.objects.get(username=request.user)
    wish_list=Wishlist.objects.filter(User=user)
    return render(request, "auctions/watchlist.html",{"Listings": wish_list})

@login_required(login_url='/login')
def add_to_watchlist(request,Listing_id):
    if request:
        user=User.objects.get(username=request.user)
        listing_add=Listing.objects.get(id=Listing_id)
        wishchk=Wishlist.objects.filter(User=user,Listing=listing_add)
        # print(wishchk.exists())
        if wishchk.exists()==False:
            wish=Wishlist(User=user,Listing=listing_add)
            wish.save()
            # print(wish)
        else:
            wishchk.delete()
        return HttpResponseRedirect(reverse("WatchList"))
    return HttpResponseRedirect(reverse("WatchList"))


@login_required(login_url='/login')
def ViewLisitng(request,Listing_id):
    user=User.objects.get(username=request.user)
    if request.method == "POST":
        item = Listing.objects.get(id=Listing_id)
        New_Bid = int(request.POST.get('Newbid'))
        if item.Starting_Bid > New_Bid:
            product = Listing.objects.get(id=Listing_id)
            return render(request, "auctions/viewlisting.html", {
                "product": item,
                "message": "Your Bid should be higher than or Equal the Starting Bid.",
                "msg_type": "danger",
            })
        if item.Price >= New_Bid:
            product = Listing.objects.get(id=Listing_id)
            return render(request, "auctions/viewlisting.html", {
                "product": item,
                "message": "Your Bid should be higher than the Current Bid.",
                "msg_type": "danger",
            })
        item.Price=New_Bid
        Newbid=Bid()
        Newbid.Price=New_Bid
        Newbid.User=user
        Newbid.save()
        item.Item_Bids.add(Newbid)
        item.save()
        return HttpResponseRedirect(reverse("ViewLisitng", args=(Listing_id,)))
    winner=None
    try:
        winner=Listing.objects.get(id=Listing_id).Item_Bids.latest('Price').User
    except:
        if winner==None:
            winner="None"
        return render(request, "auctions/viewlisting.html",{"product": Listing.objects.get(id=Listing_id),"comments":Listing.objects.get(id=Listing_id).Item_Comments.all(),"winner":winner})
    return render(request, "auctions/viewlisting.html",{"product": Listing.objects.get(id=Listing_id),"comments":Listing.objects.get(id=Listing_id).Item_Comments.all(),"winner":winner})
@login_required(login_url='/login')
def AddComment(request,Listing_id):
    user=User.objects.get(username=request.user)
    if request.method == "POST":
        item = Listing.objects.get(id=Listing_id)
        commnt=Comment()
        commnt.Title=request.POST.get('comment_title')
        commnt.Comment=request.POST.get('comment')
        commnt.User=user
        commnt.save()
        item.Item_Comments.add(commnt)
        item.save()
        return HttpResponseRedirect(reverse("ViewLisitng", args=(Listing_id,)))
    return HttpResponseRedirect(reverse("ViewLisitng", args=(Listing_id,)))

@login_required(login_url='/login')
def CloseBid(request,Listing_id):
    user=User.objects.get(username=request.user)
    if request:
        item = Listing.objects.get(id=Listing_id)
        item.Active=False
        item.save()
    return HttpResponseRedirect(reverse("ViewLisitng", args=(Listing_id,)))

def ViewCategory(request,Category_id):
    cat=Category.objects.get(id=Category_id)
    return render(request, "auctions/index.html",{"Listings": Listing.objects.filter(Category=cat)})
