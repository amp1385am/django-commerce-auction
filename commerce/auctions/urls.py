from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("bid/<int:listing_id>/", views.place_bid, name="place_bid"),
    path("close/<int:listing_id>/", views.close_auction, name="close_auction"),
    path("create/", views.create_listing, name="create_listing"),
    path("comment/<int:listing_id>/", views.add_comment, name="add_comment"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>/", views.toggle_watchlist, name="toggle_watchlist"),
]
