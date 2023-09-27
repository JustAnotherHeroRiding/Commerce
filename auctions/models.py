from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    #watchlist = models.ManyToManyField(AuctionListing, through='Watchlist')

    #def has_listing_in_watchlist(self, listing):
    #    return self.watchlist.filter(auction_listing=listing).exists()

#one for auction listings, one for bids, and one for comments made on auction listings.
class AuctionListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_price = models.FloatField()
    end_time = models.DateTimeField()
    category = models.CharField(max_length=50, blank=True)
    image_url = models.URLField(blank=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='winning_listings')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    price = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} bid {self.price} on {self.auction_listing}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} commented on {self.auction_listing}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} has added {self.auction_listing} to their watchlist"

