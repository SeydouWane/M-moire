from flask import Flask, render_template
from dashboard import create_dashboard
from pymongo import MongoClient
import json

app = Flask(__name__)

# Connexion à MongoDB (assurez-vous que MongoDB est en cours d'exécution)
client = MongoClient('mongodb://localhost:27017/')
db = client['senegactu']
collection = db['articles']

# Charger les données JSON dans MongoDB
with open('articles.json', 'r', encoding='utf-8') as file:
    articles_data = json.load(file)
    if collection.count_documents({}) == 0:
        collection.insert_many(articles_data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return create_dashboard(app)

if __name__ == '__main__':
    app.run(debug=True)
