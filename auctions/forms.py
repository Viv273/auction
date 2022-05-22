from django import forms

from .models import Auction, Comment, Bit

class AuctionForm(forms.ModelForm):

    class Meta:
        model = Auction
        fields = ('name_good', 'description', 'price', 'image', 'status', 'categories',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment',)

class BitForm(forms.ModelForm):

    class Meta:
        model = Bit
        fields = ('bit',)