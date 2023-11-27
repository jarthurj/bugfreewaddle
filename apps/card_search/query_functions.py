from .models import *


def name_query(card_name):
	if card_name == "":
		return Card.objects.all()
	name_cards = Card.objects.filter(name__icontains=card_name).all()
	return name_cards

def color_query(colors_list,exact_or_not):
	if colors_list == []:
		return Card.objects.all()
	if exact_or_not == 'contains':
		cards_list = []
		all_cards = Card.objects.all()
		for color in colors_list:
			cards_list.append(Color.objects.filter(color=color).first().cards.all())
		return all_cards.intersection(*cards_list)
	elif exact_or_not=='exact':
		difference_colors = []
		for c in ['R','W','B','U','G']:
			if c not in colors_list:
				difference_colors.append(c)
		cards_list = []
		all_cards = Card.objects.all()
		for color in colors_list:
			cards_list.append(Color.objects.filter(color=color).first().cards.all())
		cards_list_intersection = all_cards.intersection(*cards_list)

		difference_cards_list = []
		for color in difference_colors:
			difference_cards_list.append(Color.objects.filter(color=color).first().cards.all())

		difference_cards = Card.objects.none().union(*difference_cards_list)
		return_cards = cards_list_intersection.difference(cards_list_intersection.intersection(difference_cards))
		return return_cards
	elif exact_or_not=='at_most':
		cards_list = []
		all_cards = Card.objects.all()
		for color in colors_list:
			cards_list.append(Color.objects.filter(color=color).first().cards.all())
		all_cards_with_searched_colors = Card.objects.none().union(*cards_list)
		difference_colors = []
		for c in ['R','W','B','U','G']:
			if c not in colors_list:
				difference_colors.append(c)
		difference_cards_list = []
		for color in difference_colors:
			difference_cards_list.append(Color.objects.filter(color=color).first().cards.all())

		difference_cards = Card.objects.none().union(*difference_cards_list)
		return_cards = all_cards_with_searched_colors.difference(all_cards_with_searched_colors.intersection(difference_cards))
		return return_cards


def color_identity_query(colors_identity_list):
	if colors_identity_list ==[]:
		return Card.objects.all()
	cards_identity_list = []
	all_cards = Card.objects.all()
	for color in colors_identity_list:
		cards_identity_list.append(Color.objects.filter(color=color).first().cards.all())
	all_cards_with_searched_colors = Card.objects.none().union(*cards_identity_list)
	difference_colors = []
	for c in ['R','W','B','U','G']:
		if c not in colors_identity_list:
			difference_colors.append(c)
	difference_cards_list = []
	for color in difference_colors:
		difference_cards_list.append(Color.objects.filter(color=color).first().cards.all())

	difference_cards = Card.objects.none().union(*difference_cards_list)
	return_cards = all_cards_with_searched_colors.difference(all_cards_with_searched_colors.intersection(difference_cards))
	return return_cards

def rarity_query(rarity_list):
	if rarity_list == []:
		return Card.objects.all()
	empty_rarity_cards = Card.objects.none()
	for rarity in rarity_list:
		empty_rarity_cards = empty_rarity_cards.union(Rarity.objects.filter(rarity=rarity).first().cards)
	return empty_rarity_cards.all()

def mpt_query(mpt,mpt_cond,mpt_param):
	if mpt=='mana':
		if mpt_cond == 'equal':
			return Card.objects.filter(cmc=Cmc.objects.get(cmc=int(mpt_param)))
		elif mpt_cond == 'gt':
			return Card.objects.filter(cmc__gt=Cmc.objects.get(cmc=int(mpt_param)))
		elif mpt_cond == 'lt':
			return Card.objects.filter(cmc__lt=Cmc.objects.get(cmc=int(mpt_param)))
		elif mpt_cond == 'lte':
			return Card.objects.filter(cmc__lte=Cmc.objects.get(cmc=int(mpt_param)))
		elif mpt_cond == 'gte':
			return Card.objects.filter(cmc__gte=Cmc.objects.get(cmc=int(mpt_param)))
		elif mpt_cond == 'nte':
			gt = Card.objects.filter(cmc__gt=Cmc.objects.get(cmc=int(mpt_param)))
			lt = Card.objects.filter(cmc__lt=Cmc.objects.get(cmc=int(mpt_param)))
			return gt.union(lt)
	elif mpt=='power':
		if mpt_cond == 'equal':
			return Card.objects.filter(power=Power.objects.get(power=int(mpt_param))).all()
		elif mpt_cond == 'gt':
			return Card.objects.filter(power__gt=Power.objects.get(power=int(mpt_param)))
		elif mpt_cond == 'lt':
			return Card.objects.filter(power__lt=Power.objects.get(power=int(mpt_param)))
		elif mpt_cond == 'lte':
			return Card.objects.filter(power__lte=Power.objects.get(power=int(mpt_param)))
		elif mpt_cond == 'gte':
			return Card.objects.filter(power__gte=Power.objects.get(power=int(mpt_param)))
		elif mpt_cond == 'nte':
			gt = Card.objects.filter(power__gt=Power.objects.get(power=int(mpt_param)))
			lt = Card.objects.filter(power__lt=Power.objects.get(power=int(mpt_param)))
			return gt.union(lt)
	elif mpt=='toughness':
		if mpt_cond == 'equal':
			return Card.objects.filter(toughness=Toughness.objects.get(toughness=int(mpt_param)))
		elif mpt_cond == 'gt':
			return Card.objects.filter(toughness__gt=Toughness.objects.get(toughness=int(mpt_param)))
		elif mpt_cond == 'lt':
			return Card.objects.filter(toughness__lt=Toughness.objects.get(toughness=int(mpt_param)))
		elif mpt_cond == 'lte':
			return Card.objects.filter(toughness__lte=Toughness.objects.get(toughness=int(mpt_param)))
		elif mpt_cond == 'gte':
			return Card.objects.filter(toughness__gte=Toughness.objects.get(toughness=int(mpt_param)))
		elif mpt_cond == 'nte':
			gt = Card.objects.filter(toughness__gt=Toughness.objects.get(toughness=int(mpt_param)))
			lt = Card.objects.filter(toughness__lt=Toughness.objects.get(toughness=int(mpt_param)))
			return gt.union(lt)
	elif mpt=='none':
		return Card.objects.all()


def lrb_query(lrb, game_type):
	if lrb != 'none':
		legals =  Legality.objects.get(legality=lrb,
					game_type=GameType.objects.get(game_type=game_type))
		return legals.cards.all()
	else:
		return Card.objects.all()

def all_text_query(text):
	if text == "":
		return Card.objects.all()
	names = Card.objects.filter(name__icontains=text)
	types = Card.objects.filter(type_line__icontains=text)
	oracle = Card.objects.filter(oracle_text__icontains=text)
	flavor = Card.objects.filter(flavor_text__icontains=text)
	empty = Card.objects.none()
	return empty.union(names, types, oracle, flavor)

def type_query(typer):
	if typer == "":
		return Card.objects.all()
	type_cards = Card.objects.filter(type_line__icontains=typer)
	return type_cards


