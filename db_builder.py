from apps.card_search.models import *
import json
from decimal import Decimal
from datetime import datetime



startTime = datetime.now()


with open("mtg-clean3.json", "r") as j:
	c = json.load(j)

colors_list = ["W","B","U","G","R"]
for color in colors_list:
	Color.objects.create(color=color)
	ColorIdentity.objects.create(color_identity=color)

rarity_list = ['rare', 'uncommon', 'common', 'mythic', 'bonus', 'special']

for rarity in rarity_list:
	Rarity.objects.create(rarity=rarity)

layout_list = ['normal', 'augment', 'flip', 'adventure', 'host', 'meld', 
				'token', 'modal_dfc', 'planar', 'prototype', 'mutate', 
				'transform', 'scheme', 'vanguard', 'art_series', 
				'reversible_card', 'emblem', 'double_faced_token', 
				'split', 'class', 'leveler', 'saga']

for layout in layout_list:
	Layout.objects.create(layout=layout)

digital_list = [True, False]

for digital in digital_list:
	Digital.objects.create(digital=digital)

reserved_list = [True, False]

for reserved in reserved_list:
	Reserved.objects.create(reserved=reserved)

power_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 18, 20, 99]

power_bad_list = ["",'+4','-1','*','∞','1.5','+2','1+*','2+*','.5','*²',
					'3.5','+0','?','+3','+1','2.5',"1.5"]
for power in power_list:
	Power.objects.create(power=power)

toughness_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 20, 99]

toughness_bad_list = ['+4', '-1', '*','+1','1.5','7-*','+2','1+*','+3',
				'.5','2.5','2+*','14', '?','*²','*+1','-0','3.5','+0','1.5',""]

for toughness in toughness_list:
	Toughness.objects.create(toughness=toughness)

cmc_list = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 
			11.0, 12.0, 13.0, 0.5, 15.0, 16.0, 14.0, 1000000.0]

for cmc in cmc_list:
	Cmc.objects.create(cmc=Decimal(cmc))

gametype_list = ['standard', 'future', 'historic', 'gladiator', 'pioneer',
				'explorer', 'modern', 'legacy', 'pauper', 'vintage', 
				'penny', 'commander', 'oathbreaker', 'brawl',
				'historicbrawl', 'alchemy', 'paupercommander', 'duel', 
				'oldschool', 'premodern', 'predh']
legality_list = ['not_legal', 'banned', 'restricted', 'legal']
for gametype in gametype_list:
	g = GameType.objects.create(game_type=gametype)
	for legality in legality_list:
		Legality.objects.create(legality=legality, game_type=g)
ManaCost.objects.create(mana_cost="")

for card in c:
	cs = None
	mc = None
	ft = ""
	p = None
	t = None
	ot = ""
	img_s = None
	img_n = None
	img_l = None
	cmc = Cmc.objects.get(cmc=Decimal(0.0))
	tl = ""
	if len(CardSet.objects.filter(set_code=card['set'])) == 0:
		cs = CardSet.objects.create(name=card['set_name'], set_code=card['set'])
	else:
		cs = CardSet.objects.get(name=card['set_name'], set_code=card['set'])

	if 'mana_cost' in card:
		if len(ManaCost.objects.filter(mana_cost=card['mana_cost'])) == 0:
			mc = ManaCost.objects.create(mana_cost=card['mana_cost'])
		else:
			mc = ManaCost.objects.get(mana_cost=card['mana_cost'])
	else:
		mc = ManaCost.objects.get(mana_cost="")
	if 'flavor_text' in card:
		ft = card['flavor_text']
	if 'power' in card:
		if card['power'] not in power_bad_list:
			p = Power.objects.get(power=int(card['power']))
	if 'toughness' in card:
		if card['toughness'] not in toughness_bad_list:
			t = Toughness.objects.get(toughness=int(card['toughness']))
	if 'oracle_text' in card:
		ot = card['oracle_text']
	if 'image_uris' in card:
		if 'small' in card['image_uris']:
			img_s = card['image_uris']['small']
		if 'normal' in card['image_uris']:
			img_n = card['image_uris']['normal']
		if 'large' in card['image_uris']:
			img_l = card['image_uris']['large']
	if 'cmc' in card:
		cmc = Cmc.objects.get(cmc=Decimal(card['cmc']))
	if 'type_line' in card:
		tl = card['type_line'] 
	new_card = Card.objects.create(name = card['name'],
						power = p,
						toughness = t,
						cmc = cmc,
						rarity = Rarity.objects.get(rarity=card['rarity']),
						scryfall_id = card['id'],
						digital = Digital.objects.get(digital=card['digital']),
						reserved = Reserved.objects.get(reserved=card['reserved']),
						flavor_text = ft,
						collector_number = card['collector_number'],
						card_set = cs,
						oracle_text = ot,
						image_small = img_s,
						image_normal = img_n,
						image_large = img_l,
						layout = Layout.objects.get(layout=card['layout']),
						type_line = tl,
						mana_cost = mc)
	for gametype,legality in card['legalities'].items():
		g = Legality.objects.filter(legality=legality, 
			game_type=GameType.objects.filter(game_type=gametype).first()).first()
		g.cards.add(new_card)
	if 'keywords' in card:
		for keyword in card['keywords']:
			if len(Keyword.objects.filter(keyword=keyword)) == 0:
				k = Keyword.objects.create(keyword=keyword)
				k.cards.add(new_card)
	if 'colors' in card:
		for color in card['colors']:
			cc = Color.objects.get(color=color)
			cc.cards.add(new_card)
	if 'color_identity' in card:
		for color_iden in card['color_identity']:
			cc = ColorIdentity.objects.get(color_identity=color_iden)
			cc.cards.add(new_card)
print(datetime.now()-startTime)