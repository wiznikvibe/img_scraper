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
        # Creating new folder inside the directory
        save_dirs = "images/"
        if not os.path.exists(save_dirs):
            os.makedirs(save_dirs)
        
        query = request.form['query'].replace(" ", "")
        response = requests.get(f"https://www.google.com/search?q={query}&tbm=isch&ved=2ahUKEwiNkKj3y7WAAxVE_DgGHcCQA2AQ2-cCegQIABAA&oq=ronoroa+&gs_lcp=CgNpbWcQARgAMgcIABCKBRBDMgUIABCABDIFCAAQgAQyBQgAEIAEMgcIABCKBRBDMgUIABCABDIFCAAQgAQyBAgAEB4yBggAEAUQHjIJCAAQGBCABBAKOgQIIxAnOg0IABCKBRCxAxCDARBDOggIABCABBCxAzoKCAAQigUQsQMQQ1D1CFiHFGC-HWgAcAB4AIABowGIAcIIkgEDMC45mAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=7ebFZM3lEMT44-EPwKGOgAY&bih=718&biw=1536")
        
        # Storing the response content 
        content = BeautifulSoup(response.content, "html.parser")

        image_tags = content.findAll("img")



        return render_template('result.html', files=image_tags)



if __name__ == "__main__":
    app.run(debug=True)