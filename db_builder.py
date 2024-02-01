from apps.card_search.models import *
import json
from decimal import Decimal
from datetime import datetime



startTime = datetime.now()
for x in range(1,20):
	filename = "mtg-json"+str(x)+".json"
	with open(filename, "r") as j:
		print
		c = json.load(j)
		j.close()
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
	print("FILE"+str(x)+"COMPLETE")
print(datetime.now()-startTime)