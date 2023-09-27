from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages



from .models import User,AuctionListing,Bid,Comment,Watchlist

# npx tailwindcss -i static/auctions/input.css -o static/dist/output.css --watch 
# Run from the auctions folder
def index(request):
    listings = AuctionListing.objects.filter(is_active=True)
    return render(request, "auctions/index.html",{
        "listings": listings
    })


def categories(request):
    listings = AuctionListing.objects.filter(is_active=True)
    categories = set([listing.category for listing in listings])
    context = {
        'categories': categories,
    }
    return render(request, 'auctions/categories.html', context)


def category_listings(request, category):
    listings = AuctionListing.objects.filter(category=category, is_active=True)
    return render(request, 'auctions/category_listings.html', {
        'listings': listings,
        'category': category})


@login_required
def add_auction_listing(request):
    if request.method == 'POST':
        # process form data
        user = request.user
        title = request.POST['title']
        description = request.POST['description']
        starting_price = request.POST['starting_price']
        end_time = request.POST['end_time']
        category = request.POST.get('category', '')
        img_url = request.POST.get('img_url', '')

        # create new auction listing object
        listing = AuctionListing.objects.create(
            user=user,
            title=title,
            description=description,
            starting_price=starting_price,
            end_time=end_time,
            category=category,
            image_url=img_url
        )
        # redirect to the listing detail page
        #This does not exist yet
        return HttpResponseRedirect(reverse("listing", kwargs={'id': listing.id}))

    else:
        # display the add listing form
        return render(request, 'auctions/add_listing.html')

@login_required
def add_to_watchlist(request, listing_id):
    if request.user.is_authenticated:
        listing = AuctionListing.objects.get(id=listing_id)
        watchlist, created = Watchlist.objects.get_or_create(
            user=request.user,
            auction_listing=listing
        )
        if created:
            watchlist.save()
            messages.success(request, f'{listing.title} was added to your watchlist.')
            return redirect('index')
        else:
            watchlist.delete()
            messages.success(request, f'{listing.title} was removed from your watchlist.')
            return redirect('index')
    else:
        # You could add a message here to indicate that the user needs to be logged in to add items to their watchlist
        return redirect('index')

@login_required
def view_watchlist(request):
    user = request.user
    watchlist = Watchlist.objects.filter(user=user)
    auction_listings = [w.auction_listing for w in watchlist]

    context = {
        'listings': auction_listings,
    }
    return render(request, 'auctions/watchlist.html', context)
    
def auction_listing_detail(request, id):
    listing = get_object_or_404(AuctionListing, id=id)
    comments = Comment.objects.filter(auction_listing=listing)
    price = str(listing.starting_price)
    price_whole, price_fraction = price.split(".")
    try:
        highest_bid = Bid.objects.filter(auction_listing=listing).latest('price').price
    except Bid.DoesNotExist:
        highest_bid = None


    if request.method == 'POST':
        bid_amount = request.POST.get('bid_amount').strip()
        if bid_amount == '':
            error_message = "Bid amount cannot be empty"
            context = {
                    'listing': listing,
                    'price_whole': price_whole,
                    'price_fraction': price_fraction,
                    'error_message': error_message,
                    "highest_bid": highest_bid,
                    "comments":comments
                    }
            return render(request, 'auctions/listing.html', context)
        else:
            bid_amount = float(bid_amount)
            if bid_amount < listing.starting_price:
                context = {
                    'listing': listing,
                    'price_whole': price_whole,
                    'price_fraction': price_fraction,
                    'error_message': 'Bid must be greater than starting price',
                    "highest_bid": highest_bid,
                    "comments":comments
                    }
                return render(request, 'auctions/listing.html', context)
            elif Bid.objects.filter(auction_listing=listing).exists():
                highest_bid = Bid.objects.filter(auction_listing=listing).order_by('-price').first().price
                if bid_amount <= highest_bid:
                    context = {
                        'listing': listing,
                        'price_whole': price_whole,
                        'price_fraction': price_fraction,
                        'error_message': 'Bid must be greater than highest bid',
                        "highest_bid": highest_bid,
                        "comments":comments
                        }
                        
                    return render(request, 'auctions/listing.html', context)
            bid = Bid(user=request.user, auction_listing=listing, price=bid_amount)
            bid.save()
            return redirect('listing', id=id)
    context = {
        'listing': listing,
        'price_whole': price_whole,
        'price_fraction': price_fraction,
        "highest_bid": highest_bid,
        "comments":comments
    }
    return render(request, 'auctions/listing.html', context)

@login_required
def post_comment(request, listing_id):
    if request.method == 'POST':
        # Get the listing object
        listing = get_object_or_404(AuctionListing, id=listing_id)

        # Get the comment text from the request
        comment_text = request.POST.get('comment')

        # Create a new Comment object
        comment = Comment(auction_listing=listing, user=request.user, text=comment_text)
        comment.save()

        return redirect(reverse('listing', args=(listing_id,)))
    else:
        return redirect(reverse('listing', args=(listing_id,)))

@login_required
def close_auction(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    if request.user != listing.user:
        # return an error message if the user is not the creator of the listing
        return render(request, 'auctions/listing.html', {'error_message': 'You are not the creator of this listing'})
    else:
        # if the user is the creator of the listing, set the listing as inactive and set the highest bidder as the winner
        listing.is_active = False
        highest_bid = Bid.objects.filter(auction_listing=listing).order_by('-price').first()
        listing.winner = highest_bid.user
        listing.save()
        return redirect('index')


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

@login_required
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
