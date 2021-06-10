from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("Watchlist", views.watchlist, name="WatchList"),
    path("NewListing", views.create_listing, name="NewListing"),
    path("MyListing", views.my_listing, name="MyListing"),
    path("Categories", views.categories, name="Categories"),
    path("AddtoWatchlist/<int:Listing_id>", views.add_to_watchlist, name="AddtoWatchlist"),
    path("Listing/<int:Listing_id>", views.ViewLisitng, name="ViewLisitng"),
    path("AddComment/<int:Listing_id>", views.AddComment, name="AddComment"),
    path("CloseBid/<int:Listing_id>", views.CloseBid, name="CloseBid"),
    path("ViewCategory/<int:Category_id>", views.ViewCategory, name="ViewCategory"),
]
