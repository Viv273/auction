from ast import If
from tkinter.messagebox import NO
from django.contrib.auth import authenticate, login, logout
from django.core.checks import messages
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required 


from .models import Auction, User, Watchlist, Bit, Comment, Category
from .forms import AuctionForm, BitForm, CommentForm


def index(request):
    auctions=Auction.objects.filter(status='AC').all()
    return render(request, "auctions/index.html", {
        "auctions": auctions
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

def auction(request, pk):
    auction=Auction.objects.get(pk=pk)

    try:
        bit_object=Bit.objects.filter(auction=auction).values_list('bit', flat=True).order_by('-bit')
        bitmax=float(bit_object[0])
    except:
        bitmax=None

    message_winner=None
    if auction.status=='AC':
        form=BitForm()
    else:
        form=False
        winner_bit=get_object_or_404(Bit, auction=auction, bit=bitmax)
        winner_user=winner_bit.user
        if request.user.is_authenticated:
            if winner_user==request.user:
                message_winner='Сongratulations! You are the winner of the auction!'

    form_auction=AuctionForm()
    if request.user.is_authenticated:
        if Watchlist.objects.filter( user = request.user, item= auction).exists():
            message='Remove from watchlist'
        else:
            message='Add to watchlist'
        
        if auction.user==request.user:
            message_close='You can close the auction.'
        else:
            message_close=None
    else:
        message=None
        message_close=None
        

    form_comment=CommentForm()
    
    try:
        auctioncomments=Comment.objects.filter(auction=auction).all()
    except:
        auctioncomments=None

#print(f'comment {comment.comment}')
    return render(request, 'auctions/auction.html', {
        "auction":auction, "message":message, "form": form, "form_auction": form_auction,
        "message_close": message_close, "bitmax": bitmax, "message_winner": message_winner, "form_comment":form_comment, "auctioncomments":auctioncomments
    })

@login_required(login_url='login')
def create_auction(request):
    if request.method == 'POST':
            form = AuctionForm(request.POST, request.FILES)
            if form.is_valid():
                auction=form.save(commit=False)
                auction.user = request.user
                auction.save()
                form.save_m2m()
                return redirect('auction', pk=auction.pk)
    else:
        form = AuctionForm()
    return render(request, 'auctions/create_auction.html', {
        'form': form
    })

@login_required(login_url='login')
def add_watchlist(request, pk):
    watchlist_to_save=get_object_or_404(Auction,pk=pk)
    if Watchlist.objects.filter( user = request.user, item= watchlist_to_save).exists():
        #user_list, created=Watchlist.objects.filter(user = request.user)
        #user_list.watchlist.delate(watchlist_to_save)

        # watchlist_auction=Watchlist.objects.filter(user = request.user).only('item').all()
        # watchlist_auction=watchlist_auction.filter(item= watchlist_to_save)
        # watchlist_auction.delete()
        user = request.user
        watchlist=Watchlist.objects.get(user = user)
        watchlist.item.remove(watchlist_to_save)
        try:
            watchlist=Watchlist.objects.get(user = user)
            watchlists=watchlist.item.all()
        except Watchlist.DoesNotExist:
            watchlists= None
        # return HttpResponseRedirect(reverse('index'))
        
        return render(request, "auctions/watchlist.html", {
            'watchlists': watchlists
        })
    user_list, created=Watchlist.objects.get_or_create(user = request.user)
    user_list.item.add(watchlist_to_save)
    #watchlist_filter=Watchlist.objects.filter(user = request.user)
    user = request.user
    #auctions=user.watchlists_author.all()
    #auctions = Watchlist.objects.filter(user = request.user).only('watchlist').all()
    try:
        watchlist=Watchlist.objects.get(user = user)
        watchlists=watchlist.item.all()
    except Watchlist.DoesNotExist:
        watchlists= None
    messages.add_message(request, messages.SUCCESS, "Successfully added to your watchlist")
    return render(request, "auctions/watchlist.html", {
        'watchlists': watchlists
    })

    #user = request.user
    #watchlist=Watchlist.objects.first()
    #user_id=int(request.user)
    #user=Watchlist.objects.get(pk=user_id)
    #watchlist.user.add(user)
    #watchlist.watchlist.add(auction)
    #auct=Watchlist.objects.filter(user=user)
    #return render(request, 'auctions/watchlist.html', {
    #    'auctions':auct
    #})

@login_required(login_url='login')
def watchlist(request):
    user = request.user
    #auctions = user.watchlists_author.only('watchlist').all()
    #watchl=Watchlist.objects.all().filter(user = user)
    #watchlists=watchl.only('watchlist')
    # watchlist=Watchlist.objects.get(user = user)
    try:
        watchlist=Watchlist.objects.get(user = user)
        watchlists=watchlist.item.all()
    except Watchlist.DoesNotExist:
        watchlists= None
    # auctions=Auction.objects.values()
    #delwatchlist=Watchlist.objects.filter(user = user).values()
    # delwatchlist=Watchlist.objects.values()
    # item=Watchlist.objects.prefetch_related('item__auction') (Cannot find 'auction' on Auction object, 'item__auction' is an invalid parameter to prefetch_related())
    # print(f"delwatclist={delwatchlist}")
    # print(f"auctions={auctions}")
    #print(f"item={item}")
    
    return render(request, "auctions/watchlist.html", {
        'watchlists': watchlists
    })

@login_required(login_url='login')
def add_bit(request, pk):
    auction=Auction.objects.get(pk=pk)
    if Watchlist.objects.filter( user = request.user, item= auction).exists():
        message='Remove from watchlist'
    else:
        message='Add to watchlist'
    if request.method == 'POST':
        form=BitForm(request.POST)
        if form.is_valid:
            bit=float(request.POST['bit'])
            price=auction.price
            if bit>price:
                try:
                    bit_object=Bit.objects.filter(auction=auction).values_list('bit', flat=True).order_by('-bit')
                    print(f'bit_object {bit_object}')
                    bits=bit_object[0]
                    print(f'bits {bits}')
                    bmax=float(bits)
                    print(f'bmax {bmax}')
                except:
                    bmax=0
                    print(f'bitlists {bmax}')
                if bit>bmax:
                    bit=form.save(commit=False)
                    bit.user=request.user
                    bit.auction=auction
                    bit.save()
                    return render(request, 'auctions/auction.html', {
                        'pk': pk, 'auction': auction, 'message': message,  'bitmax': bit
                    })
                   
                else:
                    message_bit='You can not set price, which is not bigger than last bit: '
                    print(f'дана ставка за низька, вкажіть ставку вищу ніж:{bmax}')
                    return render(request, 'auctions/auction.html', {
                        'form': form, 'pk': pk, 'auction': auction, 'message': message, 'message_bit': message_bit, 'bmax': bmax
                    })
            else:
                message_bit='You can not set price, which is not bigger than price'
                print('ставка має бути вище ціни')
                return render(request, 'auctions/auction.html', {
                        'form': form, 'pk': pk, 'auction': auction, 'message': message, 'message_bit': message_bit
                    })
        else:
            return render(request, 'auctions/auction.html', {
                'form': form, 'pk': pk, 'auction': auction, 'message': message
            })

    else:
        form=BitForm()
    return render(request, 'auctions/auction.html', {
        'form': form, 'pk': pk, 'auction': auction, 'message': message
    })
            
@login_required(login_url='login')
def auction_close(request, pk):
    auction=Auction.objects.get(pk=pk)  
    if request.method == 'POST':
        form_auction=AuctionForm(request.POST)
        if form_auction.is_valid:
            auction.status=request.POST['status']
            auction.save()
            return HttpResponseRedirect(reverse("auction", args=(pk,)))

@login_required(login_url='login')
def create_comment(request, pk):
    auction=Auction.objects.get(pk=pk)
    if request.method == 'POST':
        form_comment=CommentForm(request.POST)
        if form_comment.is_valid:
            comment=form_comment.save(commit=False)
            comment.user=request.user
            comment.auction=auction
            comment.save() 
            return HttpResponseRedirect(reverse("auction", args=(pk,)))
        
def category(request):
    categorys=Category.objects.all()
    return render (request, "auctions/category.html", {"categorys":categorys
    })

def category_auction(request, pk):
    category=Category.objects.get(pk=pk)
    auctions=category.categories.all()
    return render(request, "auctions/index.html", {
        "auctions": auctions
    })

