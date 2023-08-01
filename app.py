import pymongo
import logging 
from flask import Flask, render_template, request, redirect, url_for 
import requests
import os
from bs4 import BeautifulSoup



app = Flask(__name__)
logging.basicConfig(filename="./logs/scraper_logs.log",level=logging.INFO, format='%(levelname)s %(asctime)s %(name)s: %(message)s')

@app.route("/", methods=['GET','POST'])
def search():
    
    if request.method == 'POST':
        try:
            # Creating new folder inside the directory
            save_directory = "images/"
            if not os.path.exists(save_directory):
                os.makedirs(save_dirs)
            

            
            query = request.form['query'].replace(" ", "")
            header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
            response = requests.get(f"https://www.google.com/search?sxsrf=AB5stBj-yjpQW68M7EDDc06zYGXn3hCBGw:1690896467683&q={query}&tbm=isch&source=lnms&sa=X&ved=2ahUKEwj7mruayLuAAxXPxDgGHYYUAj8Q0pQJegQIDRAB&biw=767&bih=708&dpr=1.25", headers=header)
            
            # Storing the response content 
            content = BeautifulSoup(response.content, "html.parser")

            image_tags = content.findAll("img")
            del image_tags[0]
            img_data = []
            for index, image_tag in enumerate(image_tags):
                image_url = image_tag['src']
                image_data = requests.get(image_url).content
                
                mydict = {"Index":index, "Image":image_data}

                img_data.append(mydict)
                with open(os.path.join(save_directory,f"{query}_{image_tag.index}.jpg"), 'wb') as f:
                    f.write(image_data)
            client = pymongo.MongoClient("mongodb+srv://wiznikvibe:3RfTsmlZz7ncmxpt@cluster0.1dfdb77.mongodb.net/?retryWrites=true&w=majority")
            db = client['images']
            review_col = db['image_data']
            review_col.insert_many(img_data)

            return "Images Loaded"
        except Exception as e:
            logging.info(e)
            return "Something went wrong"

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)