from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Comment(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    Title = models.CharField(max_length=25, default="")
    Comment = models.CharField(max_length=255)
    Time = models.DateTimeField(auto_now_add=True, blank=True)

class Category(models.Model):
    Name = models.CharField(max_length=32)
    def __str__(self):
        return self.Name

class Bid(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    Price = models.DecimalField(max_digits=12, decimal_places=2)
    Time = models.DateTimeField(auto_now_add=True, blank=True)

class Listing(models.Model):
    Title=models.CharField(max_length=128)
    Description=models.CharField(max_length=255)
    Category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='Category',null=True, blank=True)
    Starting_Bid=models.DecimalField(max_digits=12, decimal_places=2)
    Price=models.DecimalField(max_digits=12, decimal_places=2)
    Time_Added = models.DateTimeField(auto_now_add=True, blank=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Lister")
    Item_Bids = models.ManyToManyField(Bid, blank=True, related_name="Item_Bids")
    Item_Comments = models.ManyToManyField(Comment, blank=True, related_name="Item_Comments")
    Image_Link = models.CharField(max_length=200, default=None, blank=True, null=True)
    Active=models.BooleanField(default=True)
    def __str__(self):
        return self.Title
    
class Wishlist(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_wishlist")
    Listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing")
    def __str__(self):
        return self.Listing.Title
    
    