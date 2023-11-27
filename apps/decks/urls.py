from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.decks, name='decks'),
    path('add_deck/', views.add_deck, name="add_deck"),
    path('add_card/', views.add_card, name="add_card"),
    path('deck_detail/<int:deck_id>/', views.deck_detail, name="deck_detail"),
    path('card_quantity/', views.card_quantity, name="remove_card"),
    path('delete_card/', views.delete_card, name="delete_card"),
]
