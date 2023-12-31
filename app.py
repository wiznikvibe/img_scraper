import pymongo
import logging 
from flask import Flask, render_template, request, redirect, url_for 
import requests
import os
from bs4 import BeautifulSoup
from configparser import ConfigParser



app = Flask(__name__)
logging.basicConfig(filename="./logs/scraper_logs.log",level=logging.INFO, format='%(levelname)s %(asctime)s %(name)s: %(message)s')
config = ConfigParser()
config.read('config.ini')
key = config['USER']['KEY']


@app.route("/", methods=['GET','POST'])
def search():
    
    if request.method == 'POST':
        try:
            query = request.form['content']
            save_directory = "images/"
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
                
            response = requests.get(f"https://www.google.com/search?q={query}&tbm=isch&ved=2ahUKEwiNkKj3y7WAAxVE_DgGHcCQA2AQ2-cCegQIABAA&oq=ronoroa+&gs_lcp=CgNpbWcQARgAMgcIABCKBRBDMgUIABCABDIFCAAQgAQyBQgAEIAEMgcIABCKBRBDMgUIABCABDIFCAAQgAQyBAgAEB4yBggAEAUQHjIJCAAQGBCABBAKOgQIIxAnOg0IABCKBRCxAxCDARBDOggIABCABBCxAzoKCAAQigUQsQMQQ1D1CFiHFGC-HWgAcAB4AIABowGIAcIIkgEDMC45mAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=7ebFZM3lEMT44-EPwKGOgAY&bih=718&biw=1536")
            response.raise_for_status
            

                # Storing the response content 
            content = BeautifulSoup(response.content, "html.parser")
            image_tags = content.findAll('img')
            del image_tags[0]
            img_data = []
            for index, image_tag in enumerate(image_tags):
                image_url = image_tag['src']
                image_data = requests.get(image_url).content
                mydict = {"index":index,'image':image_data}
                img_data.append(mydict)
                with open(os.path.join(save_directory,f'{query}-{image_tags.index(image_tag)}.jpeg'), 'wb') as f:
                    f.write(image_data)
            client = pymongo.MongoClient(f"mongodb+srv://wiznikvibe:{key}@cluster0.1dfdb77.mongodb.net/?retryWrites=true&w=majority")
            db = client['image_directory']
            image_dir = db['image_scrape_data']
            image_dir.insert_many(img_data)
            logging.info("Image data populated into the MongoDb Cluster")
                    
            return "<h1>Images Loaded</h1>"
        except Exception as e:
            logging.info(e)
         
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000)