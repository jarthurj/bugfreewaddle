from django.db import models
from apps.card_search.models import Card
from django.contrib.auth.models import User

class Deck(models.Model):
	card = models.ManyToManyField(Card, related_name='cards',through="CardDeck")
	name = models.CharField(max_length=100)
	desc = models.CharField(max_length=100)
	user = models.ManyToManyField(User, related_name='users')

class CardDeck(models.Model):
	card = models.ForeignKey(Card, on_delete=models.CASCADE)
	deck = models.ForeignKey(Deck, on_delete=models.CASCADE)

