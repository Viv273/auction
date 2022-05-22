from django.contrib import admin
from .models import User, Category, Auction, Comment, Bit, Watchlist
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Auction)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Bit)