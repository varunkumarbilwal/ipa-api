import requests
from bs4 import BeautifulSoup
import json
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'


url = 'https://ipa-apps.me'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, features='html5lib')

articles = soup.find_all({'div': 'item-content'})

imgsrcs = []
titles = []
hrefs = []

for i in articles:

    itemMedia = i.find('div', class_ = 'item-media')
    if(itemMedia != None):
        imgTag = itemMedia.find('img', class_ = 'app-icon')
        if(imgTag != None):
            imgSrc = imgTag['src']
            if imgSrc not in imgsrcs:
                imgsrcs.append(imgSrc)
    
    itemInner = i.find('div', class_ = 'item-inner')
    if(itemInner != None):
        itemTitle = itemInner.find('div', class_ = 'item-title')
        title = itemTitle.text
        if title not in titles:
            titles.append(title)

    itemTitleRow = i.find('div', class_ = 'item-title-row')
    if(itemTitleRow != None):
        itemAfter = itemTitleRow.find('div', class_ ='item-after')
        if(itemAfter != None):
            alink = itemAfter.find('a', class_ = 'button')
            if(alink != None):
                ahref = alink['href']
                if ahref not in hrefs:
                    hrefs.append(ahref)

certname = soup.find('span', class_ = 'success1')
certtext = certname.text
cert = certtext.split('"')
fcert = cert[1]

keys = ['imgsrc', 'title', 'href']
items = [dict(zip(keys, [u, t, d])) for u, t, d in zip(imgsrcs, titles, hrefs)]

d = {
      'CertName': fcert,
      'items': items
    }
d = json.dumps(d, indent=4)

@app.route('/get')
def about():
    return d


