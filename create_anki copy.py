import genanki

my_model = genanki.Model(
  1380120064,
  'Example',
  fields=[
    {'name': 'Object'},
    {'name': 'Image'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Object}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Image}}',
    },
  ])

my_note = genanki.Note(
  model=my_model,
  fields=['JPEG File', '<img src="loesung2.jpg">'])

my_deck = genanki.Deck(
  2059400191,
  'Example')

my_deck.add_note(my_note)

my_package = genanki.Package(my_deck)
my_package.media_files = ['loesung2.jpg']

my_package.write_to_file('output.apkg')