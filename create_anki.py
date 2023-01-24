import json
import genanki
import os

if not os.path.exists("/content/drive/MyDrive/AM_RDP_Decks"):
    os.makedirs("/content/drive/MyDrive/AM_RDP_Decks")

with open("/content/drive/MyDrive/"+'themen.json') as json_file:
    themen = json.load(json_file)
i=0
mainimgs=[]
alldecks=[]
for the in themen:
  i+=1
    #open beispiele.json
  with open('/content/drive/MyDrive/beispiele.json') as json_file:
      data = json.load(json_file)

  thema=the["thema"]

  my_deck = genanki.Deck(
      deck_id=12345, # a unique id for the deck
      name=thema+"_RDP_scraped") # the name of the deck

  maindeck = genanki.Deck(
  deck_id=i, # a unique id for the deck
  name="RDP_Scraped::"+thema.replace("/","und")+'.apkg') # the name of the deck
  

  img=[]
  #filter by thema
  data = [i for i in data if i['thema'] == thema]
  c=0
  
  
  for bsp in data:
      
          #get "aufgabe_body"
      ab=bsp['aufgabe_body']
       #extract bsp letter + ")"
      aufgabe = ab.split("/")[-1].split(".")[0]
      c+=1
      aufgabe_name= bsp["name"]+"_"+bsp["id"]+aufgabe
      auf_dir="/content/drive/MyDrive/Themen/"+thema+"/"+aufgabe_name
      ah=bsp['aufgabe_head']
      ah_name= bsp["id"]+aufgabe+"_ah"
      ah_path= auf_dir+"/"+ah_name+".png"
      ab=bsp['aufgabe_body']
      ab_name= bsp["id"]+aufgabe+"_ab"
      ab_path= auf_dir+"/"+ab_name+".png"
      my_card = genanki.Note(
      model=genanki.Model(
          1380120064,
    'Persie0 Style',
          fields=[
              {'name': 'Image1'},
              {'name': 'Image2'},
              
              {'name': 'AnswerImage'},
              {'name': 'Answer'},
          ],
          templates=[
              {
                  'name': 'Card 1',
                  'qfmt': '<br>{{Image1}}<br>{{Image2}}',
                  'afmt': '{{FrontSide}}<br><hr id=answer>{{AnswerImage}}<br>{{Answer}}',
              },
          ]
      ),
      fields=['<div style="text-align: center;"><img src="{}"></div>'.format(ah_name+".png"), '<div style="text-align: center;"><img src="{}"></div>'.format(ab_name+".png"), '<div style="text-align: center;"><img src="{}"></div>'.format(bsp["id"]+aufgabe+"_loesung.jpeg"), '<div style="text-align: center;"><a href="{}">Link</a></div>'.format(bsp["loesung"])])

      mainimgs.append(ah_path)
      mainimgs.append(ab_path)
      mainimgs.append(auf_dir+"/"+bsp["id"]+aufgabe+"_loesung.jpeg")
      maindeck.add_note(my_card)

      img.append(ah_path)
      img.append(ab_path)
      img.append(auf_dir+"/"+bsp["id"]+aufgabe+"_loesung.jpeg")
      my_deck.add_note(my_card)



  my_package = genanki.Package(my_deck)
  my_package.media_files = img

  alldecks.append(maindeck)
  
  

  if len(img)!=0:
    print(thema+" fertig")
    continue
    my_package.write_to_file("/content/drive/MyDrive/AM_RDP_Decks/"+thema.replace("/","und")+'.apkg')
  
package = genanki.Package(alldecks)
package.media_files = mainimgs
package.write_to_file("/content/drive/MyDrive/RDP_scraped.apkg")

