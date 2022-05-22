from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.files import ImageField


class User(AbstractUser):
    pass

class Category(models.Model):
   name = models.CharField(max_length = 200)

   def __str__(self):
     return f'{self.name}'

AUCTION_STATUSES = [
    ('AC', 'Active'),
    ('CL', 'Closed'),
]

class Auction(models.Model):
   name_good = models.CharField(max_length = 64)
   description=models.TextField(max_length = 500)
   price=models.FloatField()
   image=models.ImageField(upload_to='auctions/static/auctions/image/', blank=True)
   status=models.CharField(max_length=2, choices=AUCTION_STATUSES, default='AC')
   categories = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='categories')
   user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_auction')

   def __str__(self):
     return f'{self.id} name:{self.name_good}, description:{self.description}, price:{self.price}, category: {self.categories}'

class Comment(models.Model):
    comment=models.TextField(max_length=500)
    user=models.ForeignKey(User, on_delete=models.PROTECT, related_name='author')
    auction=models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments_auction')
    date=models.DateField(auto_now_add=True)

    def __str__(self):
     return f'{self.comment}'

class Bit(models.Model):
    bit=models.FloatField()
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='bits_author')
    auction=models.ForeignKey(Auction, on_delete=models.PROTECT, related_name='bits_auction')
    

    def __str__(self):
     return f'{self.bit}'

class Watchlist(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlists_author')
    item=models.ManyToManyField(Auction, blank=True, related_name='auctions_watchlist')
    

    def __str__(self):
     return f"{self.user}'s WatchList"


    