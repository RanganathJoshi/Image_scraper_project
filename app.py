from flask import Flask,render_template,request
from bs4 import BeautifulSoup
import requests
import os

app=Flask(__name__)

@app.route('/',methods=['GET'])
def homepage():
    if request.method=='GET':
        return render_template('index.html')

@app.route("/review",methods=['POST','GET'])
def index():
    if request.method == 'POST':

                try:

                    #store the input in the 'query' variable
                    query=request.form['content'].replace(" ","")

                    #To store the images
                    save_dir='images/'

                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)

                    # fake user agent to avoid getting blocked by Google
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

                     #Url to the data from
                    url_path=f"https://www.google.com/search?q={query}&sxsrf=AJOqlzUuff1RXi2mm8I_OqOwT9VjfIDL7w:1676996143273&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiq-qK7gaf9AhXUgVYBHYReAfYQ_AUoA3oECAEQBQ&biw=1920&bih=937&dpr=1#imgrc=1th7VhSesfMJ4M"
        
                    #get response from that url 
                    response=requests.get(url_path)

                    #Using Beuatiful soup class to filer only html content
                    soup=BeautifulSoup(response.content,'html.parser')

                    #Extracting only images from that html content
                    img_all=soup.find_all('img')

                    del img_all[0]

                    for index,image in enumerate(img_all):
                        #Extracting image_url
                        img_url=image['src']
                        img_content=requests.get(img_url).content

                        #Storing the extracted image in local disk
                        with open(os.path.join(save_dir,f'{query}_{img_all.index(image)}.jpg'),'wb') as f:
                            f.write(img_content)

                    return "images loaded"
                except Exception as e:
                    return "There is something wrong"


if __name__=="__main__":
    app.run()