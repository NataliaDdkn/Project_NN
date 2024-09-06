from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from models import CARDS, db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# связываем приложение и экземпляр SQLAlchemy
db.init_app(app)
#создаем все, что есть в db.Models
with app.app_context():
    db.create_all()
import requests
import json
app.config['SECRET_KEY']= 'ochen_$ecRetNyI_Kod'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_THRESHOLD'] = 500
Session(app)

def ...():

 new_card = get_card(...)['cards'][0]
 # создаем экземпляр модели
 new_card_to_db = CARDS (
     deck_id = session.get('deck_id'),
       username = session.get('username'),
       datetime = datetime.now(),
       card = new_card['code'])

 # добавляем экземпляр в сессию базы данных
 db.session.add(new_card_to_db)
 # подтверждаем изменения сессии и сохраняем данные
  db.session.commit()

return ...

@app.route('/')
def get_deck():
	session["my_cards"]=[]
	session["points"]=[]
	session["deck"]=json.loads(
	requests.post('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)['deck_id']
	return render_template('index.html', deck=session["deck"])

@app.route('/draw')
def new_game():
    
	return render_template('draw.html', deck=session["deck"])



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
	
	session["my_cards"].append(card_suit)
	
	session["points"].append(card_points)
	points_all=sum(session["points"])
	
	cards_left = json.loads(
	requests.post('https://deckofcardsapi.com/api/deck/'+deck+'').text)['remaining']
	return render_template('draw.html', my_cards=session["my_cards"], deck=deck, cards_left=cards_left, points_all=points_all)

if __name__ == '__main__':
    app.run()