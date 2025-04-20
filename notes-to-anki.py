# Importing BeautifulSoup class from the bs4 module 
import genanki
from markdown import markdown
import os

my_model = genanki.Model(
  1607392319,
  'Simple Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
])

my_deck = genanki.Deck(2059400110, 'Czech - generated')

def file_to_note(file_path: str):
    file = open(file_path, "r")
    back_html = markdown(file.read())
    file_path_without_ext, _ = os.path.splitext(file_path) # _ means, don't save the extension
    file_name = file_path_without_ext.split('/')[-1] # the last one is the file name
    my_note = genanki.Note(
      model=my_model,
      fields=[file_name, back_html])
    my_deck.add_note(my_note)

def get_all_mds(path='.'):
    files = []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            files += get_all_mds(full_path)
        _, extension = os.path.splitext(full_path)
        if (extension == ".md"):
            files.append(full_path);

    return files

notes = get_all_mds("/home/bakterio/Dokumenty/obsidian-vault/GJB/Čeština/")

for note in notes:
    print(note)
    file_to_note(note)

genanki.Package(my_deck).write_to_file('output.apkg')
