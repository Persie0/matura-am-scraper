import json
import genanki


#open beispiele.json
with open('beispiele.json') as json_file:
    data = json.load(json_file)

thema="Binomialverteilung"

my_deck = genanki.Deck(
    deck_id=12345, # a unique id for the deck
    name=thema) # the name of the deck


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
        model_id=12345,
        fields=[
            {'name': 'Image1'},
            {'name': 'Image2'},
            
            {'name': 'AnswerImage'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Image}}<br>{{Image}}',
                'afmt': '{{Image}}<br>{{Answer}}',
            },
        ]
    ),
    fields=[ah_path, ab_path, auf_dir+"/"+"loesung.jpeg", bsp["loesung"]])
    my_deck.add_note(my_card)
    if c==4:
        break

genanki.Package(my_deck).write_to_file(thema+'.apkg')



