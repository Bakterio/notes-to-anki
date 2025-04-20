# Importing BeautifulSoup class from the bs4 module 
from bs4 import BeautifulSoup 
from lxml.html.clean import Cleaner
from lxml import html
import genanki

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

cleaner = Cleaner(
    style=True,            # remove all <style> blocks & style attributes
    scripts=True,          # remove any <script> blocks
    comments=True,         # remove HTML comments
    links=False,           # if True removes href/@src attributes entirely
    javascript=True,       # remove onclick, etc
    page_structure=False,  # leave <html>/<head>/<body> alone
)


  
filename = "Farma zvířat"
# Opening the html file 
HTMLFile = open(filename + ".html", "r") 
  
# Reading the file 
index = HTMLFile.read() 
  
# Creating a BeautifulSoup object and specifying the parser 
Parse = BeautifulSoup(index, 'lxml') 
  
def search_sub_headings(level, heading: str):
    global Parse
    all_headers = Parse.find_all(class_=[f"el-{level}", "heading-wrapper"])
    for header in all_headers:
        first_child = header.contents[0]
        if (first_child.text.lower() == heading.lower()):
            return header.contents[-1]

subs = search_sub_headings("h3", "Postavy")

for heading in subs:
    print("Processing")
    front = heading.find(class_="heading").text
    paragraph = heading.find(class_="heading-children")
    back = paragraph.text
    clean_back = cleaner.clean_html(html.fromstring(back))
    clean_back = html.tostring(clean_back, encoding='unicode', method='text')
    my_note = genanki.Note(
      model=my_model,
      fields=[front, clean_back])
    my_deck.add_note(my_note)
    print("\n")

genanki.Package(my_deck).write_to_file('output.apkg')
