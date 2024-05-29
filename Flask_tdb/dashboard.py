import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from flask import Flask
from pymongo import MongoClient

def create_dashboard(server):
    app = dash.Dash(__name__, server=server, routes_pathname_prefix='/dashboard/')

    # Connexion à la base de données MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['senegactu']
    collection = db['articles']

    # Récupérer les données depuis MongoDB
    articles = pd.DataFrame(list(collection.find()))

    # Préparation des données pour les visualisations
    articles['date'] = pd.to_datetime(articles['date'])
    site_count = articles['site_url'].value_counts()
    author_count = articles['auteurs'].apply(lambda x: pd.Series(x.split(', '))).stack().value_counts()

    app.layout = html.Div([
        html.H1("Tableau de Bord des Articles de Presse"),

        # Diagramme circulaire des sites
        dcc.Graph(
            id='pie-chart-sites',
            figure=px.pie(site_count, names=site_count.index, values=site_count.values, title='Répartition des Articles par Site')
        ),

        # Diagramme à barres des auteurs
        dcc.Graph(
            id='bar-chart-authors',
            figure=px.bar(author_count, x=author_count.index, y=author_count.values, title='Nombre d\'Articles par Auteur')
        ),

        # Liste des articles
        html.H2("Liste des Articles"),
        dcc.Dropdown(
            id='article-dropdown',
            options=[{'label': title, 'value': title} for title in articles['titre']],
            placeholder="Sélectionnez un article"
        ),
        html.Div(id='article-content')
    ])

    @app.callback(
        Output('article-content', 'children'),
        [Input('article-dropdown', 'value')]
    )
    def display_article_content(selected_article):
        if selected_article:
            article = articles[articles['titre'] == selected_article].iloc[0]
            return html.Div([
                html.H3(article['titre']),
                html.P(f"Auteur(s) : {article['auteurs']}"),
                html.P(f"Date : {article['date']}"),
                html.P(article['contenu'])
            ])
        return html.Div("Sélectionnez un article pour afficher son contenu.")

    return app.server
