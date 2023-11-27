from django import forms
# from .form_helpers import *
# DECKS = user_decks()

# QUANTITY = (
# 	(1,1),
# 	(2,2),
# 	(3,3),
# 	(4,4),
# 	(5,5),
# 	(6,6),
# 	(7,7),
# 	(8,8),
# 	(9,9),)
class DeckForm(forms.Form):
	deck_name = forms.CharField(max_length=100)
	deck_description = forms.CharField(max_length=100)

# class AddCardForm(forms.Form):
# 	deck_name = forms.ChoiceField(choices=DECKS)
# 	quantity = forms.ChoiceField(choices=QUANTITY)

