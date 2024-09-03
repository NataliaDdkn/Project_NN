from flask import Flask, render_template, request, redirect

app = Flask(__name__)
import requests
import json
@app.route('/')

def get_deck():
	deck = json.loads(
	requests.post('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)['deck_id']
	return render_template('index.html', deck=deck)
@app.route('/draw/<deck>')
def get_cards(deck):
	cards = json.loads(
	requests.post('https://deckofcardsapi.com/api/deck/'+deck+'/draw/?count=1').text)['cards'][0]['image']
	return render_template('index.html', cards=cards, deck=deck)

if __name__ == '__main__':
    app.run()