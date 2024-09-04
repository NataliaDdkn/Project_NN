from flask import Flask, render_template, request, redirect

app = Flask(__name__)
import requests
import json
my_cards=[]
points=[]


@app.route('/')
def get_deck():
	global deck
	deck = json.loads(
	requests.post('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)['deck_id']
	return render_template('index.html', deck=deck)

@app.route('/draw')
def new_game():
    
	return render_template('draw.html', deck=deck)



@app.route('/draw/<deck>')
def get_cards(deck):
	cards=json.loads(
	requests.post('https://deckofcardsapi.com/api/deck/'+deck+'/draw/?count=1').text)['cards'][0]
	
	card_suit=cards['image']
	card_value=cards['value']
	card_points=0
	points_all=0	
	
	def card_points(card_value):
		if card_value == 'JACK' or card_value == 'KING' or card_value == 'QUEEN' or card_value == 'ACE':
			card_points=10
		else:
			card_points=int(card_value)
		return(card_points)
		
	card_points=card_points(card_value)
	
	my_cards.append(card_suit)
	
	points.append(card_points)
	points_all=sum(points)
		
	cards_left = json.loads(
	requests.post('https://deckofcardsapi.com/api/deck/'+deck+'').text)['remaining']
	return render_template('draw.html', my_cards=my_cards, deck=deck, cards_left=cards_left, points_all=points_all)

if __name__ == '__main__':
    app.run()