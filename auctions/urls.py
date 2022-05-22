from django.urls import path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:pk>", views.auction, name="auction"),
    path("auction/create", views.create_auction, name="create_auction"),
    path("add/watchlist/<int:pk>", views.add_watchlist, name="add_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bit/<int:pk>", views.add_bit, name="add_bit"),
    path("auction/close/<int:pk>", views.auction_close, name= "auction_close"),
    path("create_comment/<int:pk>", views.create_comment, name="create_comment"),
    path("category", views.category, name="category"),
    path("categoty/<int:pk>", views.category_auction, name="category_auction")
] 

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
