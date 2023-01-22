import json
import genanki

#open themen.json
with open('themen.json') as json_file:
    themen = json.load(json_file)


#open beispiele.json
with open('beispiele.json') as json_file:
    data = json.load(json_file)

for the in themen:
    thema=the["thema"]

    my_deck = genanki.Deck(
        deck_id=12345, # a unique id for the deck
        name=thema+"_RDP_scraped") # the name of the deck

    img=[]
    #filter by thema
    data = [i for i in data if i['thema'] == thema]
    c=0
    for bsp in data:
        c+=1
        aufgabe_name= bsp["name"]+"_"+bsp["id"]
        auf_dir=thema+"/"+aufgabe_name
        ah=bsp['aufgabe_head']
        ah_name= aufgabe_name+"_ah"
        ah_path= auf_dir+"/"+ah_name+".png"
        ab=bsp['aufgabe_body']
        ab_name= aufgabe_name+"_ab"
        ab_path= auf_dir+"/"+ab_name+".png"
        my_card = genanki.Note(
        model=genanki.Model(
            1380120064,
    'Example',
            fields=[
                {'name': 'Image1'},
                {'name': 'Image2'},
                
                {'name': 'AnswerImage'},
                {'name': 'Answer'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Image1}}<br>{{Image2}}',
                    'afmt': '{{AnswerImage}}<br>{{Answer}}',
                },
            ]
        ),
        fields=['<img src="{}">'.format(ah_name+".png"), '<img src="{}">'.format(ab_name+".png"), '<img src="{}">'.format("loesung.jpeg"), '<a href="{}">Link</a>'.format(bsp["loesung"])])

        img.append(ah_path)
        img.append(ab_path)
        img.append(auf_dir+"/"+"loesung.jpeg")
        my_deck.add_note(my_card)
        if c==3:
            break

    my_package = genanki.Package(my_deck)
    my_package.media_files = img



    my_package.write_to_file(thema+'.apkg')



