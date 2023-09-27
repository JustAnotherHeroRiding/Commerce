from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('add_listing', views.add_auction_listing, name='add_listing'),
    path('listing/<int:id>/', views.auction_listing_detail, name='listing'),
    path('add_to_watchlist/<int:listing_id>', views.add_to_watchlist ,name='add_to_watchlist'),
    path('watchlist/', views.view_watchlist, name='watchlist'),
    path('close/<int:listing_id>/', views.close_auction, name='close'),
    path('listing/<int:listing_id>/post_comment/', views.post_comment, name='post_comment'),
    path('categories', views.categories, name='categories'),
    path('category/<str:category>/', views.category_listings, name='category_listings'),
]
