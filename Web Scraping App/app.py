import flask
from flask import Flask , render_template, request
import bs4
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def getvalue():
    url = request.form['link']
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    products = []
    ratings = []
    prices = []

    for data in soup.find_all('div',attrs={'class':'_3pLy-c'}):
        name = data.find('div',attrs={'class':'_4rR01T'}).text
        products.append(name)
        cost = data.find('div',attrs={'class':'_30jeq3 _1_WHN1'}).text
        prices.append(cost)
        rating = data.find('div',attrs={'class':'_3LWZlK'})
        try:
            rating = rating.text
        except:
            rating = 'None'
        ratings.append(rating)

    headers = ('Name','Price In Rupees','Rating')
    tabledata = (products,prices,ratings)
    finaltable = dict(zip(headers,tabledata))

    Table = pd.DataFrame(finaltable)
    result = Table.to_html()

    return result








if __name__ == '__main__':
    app.run(debug=True)
