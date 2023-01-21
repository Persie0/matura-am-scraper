import requests
import json
from bs4 import BeautifulSoup
import time

URL = "https://prod.aufgabenpool.at/srdp/phpcode/search.php"


all=[]
#loop through a to z
for i in range(97, 123):
#post request with query=buchstabe as payload
    r = requests.post(url = URL, data = {'query': chr(i)})
    #extracting response text
    soup = BeautifulSoup(r.content, "html.parser")
    #get all <li> tags
    li = soup.find_all('li')

    
    #get "id" attribute of the <div> in <li> tag
    li_id = [i.find('div')['id'] for i in li]

    #get inner text of <li> tags
    li_text = [i.text for i in li]

    #remove text between and "<" until ">" 
    li_text = [i.split("<")[0] for i in li_text]

    #remove "(number)" at the end
    li_text = [i.split("(")[0] for i in li_text]

    #trim whitespaces
    li_text = [i.strip() for i in li_text]

    #combine id and text to json
    li_text = [{"id": li_id[i], "thema": li_text[i]} for i in range(len(li_id))]

    all += li_text
    print(len(all))
    time.sleep(0.2)

#remove duplicates
all = list({v['id']:v for v in all}.values())

#remove {"id": "Ooops ...", "thema": "Ihre Suche hat leider keine Treffer erzielt."}
all = [i for i in all if i['id'] != "Ooops ..."]

#save as json
with open('themen.json', 'w') as outfile:
    json.dump(all, outfile)
