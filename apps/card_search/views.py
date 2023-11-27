from django.shortcuts import render, HttpResponse, redirect
from .forms import CardSearch
from .models import *
from django.db.models.query import QuerySet
from .query_functions import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from apps.decks.models import Deck

def index(request):

	context = {
		'search_form':CardSearch(),
		'logged_in':request.user.is_authenticated,
	}
	return render(request, "card_search/index.html",context)

def search(request):

	errors = {}

	if ((request.POST.get('colors',"")!= "" or 
			request.POST.getlist('colors') != []) and 
			request.POST['exactly_or_not']=='default'):
		errors['color_error'] = "Please select how to search colors!!!!!!"

	if ((request.POST.get('mpt',"none")=="none" and 
			request.POST.get('mpt_condition', "none")!="none") or
			((request.POST.get('mpt',"none")!="none" and 
			request.POST.get('mpt_condition', "none")=="none"))):
		errors['format_error'] = "Please select all conditions for format query"

	if ((request.POST.get('lrb',"none")=="none" and 
			request.POST.get('game_types', "none")!="none") or
			((request.POST.get('lrb',"none")!="none" and 
			request.POST.get('game_types', "none")=="none"))):
			errors['mpt_error'] = "Please select all conditions for stats query"
	if errors:
		for key, value in errors.items():
				messages.error(request, value)
		return redirect('index')
	else:
		all_cards = Card.objects.all()

		name_cards = name_query(request.POST['card_name'])

		color_cards = Card.objects.none()

		color_cards = color_query(request.POST.getlist('colors'),
			request.POST['exactly_or_not'])

		color_identity_cards = color_identity_query(request.POST.getlist('colors_identity'))

		rarity_cards = rarity_query(request.POST.getlist('rarity'))


		mpt_cards = mpt_query(request.POST['mpt'],
								request.POST['mpt_condition'],
								request.POST['mpt_parameter'])

		lrb_cards = lrb_query(request.POST['lrb'],request.POST['game_types'])
		all_text_cards = all_text_query(request.POST['any_text'])
		type_cards = type_query(request.POST['type_line'])

		all_queries = [name_cards, color_cards, color_identity_cards,
							rarity_cards, mpt_cards, lrb_cards, 
							all_text_cards, type_cards]

		matching_queries = []

		for query in all_queries:
			if query != Card.objects.none():
				matching_queries.append(query)

		matching_cards = matching_queries[0].intersection(*matching_queries)
		matching_cards_ids = []
		for x in matching_cards:
			matching_cards_ids.append(x.id)
		request.session['card_ids'] = matching_cards_ids
		return redirect('cards',page=1)

def card_pages(request,page):
	last_page = len(request.session['card_ids'])//60
	if page == 1:
		cards = request.session['card_ids'][:60]
	elif page != last_page:
		cards = request.session['card_ids'][60*page:(60*page)+60]
	elif page >=last_page:
		page = last_page
		cards = request.session['card_ids'][(60*(last_page-1))+60:]
	to_union = []
	for x in cards:
		to_union.append(Card.objects.filter(id=x))
	page_cards = Card.objects.none().union(*to_union)
	page_one = False
	next_page = page+1
	if page+1>=last_page:
		next_page = last_page
	if page == 1:
		page_one = True

	context = {
		'cards':page_cards,
		'page':page,
		'page_one':page_one,
		'prev_page':page-1,
		'next_page':page+1,
		'last_page':last_page==page,
		'logged_in':request.user.is_authenticated,
	}
	return render(request, 'card_search/cards.html', context)

def single_card(request,card_id):

	request.session['card_ids'] = None
	card = Card.objects.filter(id=card_id).first()
	printings = Card.objects.filter(name=card.name)
	if len(printings) > 11:
		printings = printings[:11]
	context = {
		'card':card,
		'printings':printings,
		'logged_in':request.user.is_authenticated,
		'decks':Deck.objects.filter(user=User.objects.get(id=request.user.id)),
	}
	return render(request,'card_search/single_card.html', context)

def all_prints(request,card_id):

	name_cards = name_query(Card.objects.get(id=card_id).name)
	matching_cards_ids = []
	for x in name_cards:
		matching_cards_ids.append(x.id)
	request.session['card_ids'] = matching_cards_ids
	return redirect('cards', page=1)

	