import requests
import json
from bs4 import BeautifulSoup
import time

URL = "https://aufgabenpool.at/srdp/phpcode/lp_results.php"

#read themen.json
with open('themen.json') as json_file:
    data = json.load(json_file)

res=[]
for el in data:
    payload = {'id': el['id'], 'coll': ''}

    #post request
    r = requests.post(url = URL, data = payload)

    #extracting response text
    soup = BeautifulSoup(r.content, "html.parser")

    #extract all <li> tags
    li = soup.find_all('li')

    #pdf is <a> tag
    #images can be found with src attribute from <img> tag

    all_imgs = []
    for i in li:
        temp= {'loesung': "https://aufgabenpool.at/srdp/"+i.find('a')['href']}
        #get string between last / and .pdf
        temp['name'] = i.find('a')['href'].split("/")[-1].split(".pdf")[0]
        #find all <img> tags
        imgs = i.find_all('img')
        for i in range(len(imgs)):
            if i == 0:
                temp['aufgabe_head'] = "https://aufgabenpool.at/srdp/"+imgs[i]['src']
                temp['teil'] = imgs[i]['src'].split("teil")[1].split("/")[0].upper()
                temp['id'] = imgs[i]['src'].split("/")[1].split("/")[0].upper()
                temp["thema"]=el['thema']
            elif i == 1:
                temp['aufgabe_body'] = "https://aufgabenpool.at/srdp/"+imgs[i]['src']
                break
        res.append(temp)
    print(len(res))
    time.sleep(10)

#save as json
with open('beispiele.json', 'w') as outfile:
    json.dump(res, outfile)

