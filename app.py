import pymongo
import logging 
from flask import Flask, render_template, request, redirect, url_for 
import requests
import os
from bs4 import BeautifulSoup



app = Flask(__name__)
logging.basicConfig(filename="./logs/scraper_logs.log",level=logging.INFO, format='%(levelname)s %(asctime)s %(name)s: %(message)s')

@app.route("/")
def home():
    # logging.info("Home Page Called")
    app.logger.info("App Running")
    return render_template("home.html")

@app.route("/search", methods=['GET','POST'])
def search():
    if request.method == 'GET':
        app.logger.info("Search Initiated")
        return render_template('search.html', title='Search')
    else:
        query = request.form['query'].replace(" ", "")
        return render_template('result.html', query=query)



if __name__ == "__main__":
    app.run(debug=True)