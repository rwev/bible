import xml.etree.ElementTree as ET


root = ET.parse('translations/NIV.xml')

def get_books():
    return [bel.attrib['n'] for bel in root.findall('b')]

def get_chapters(book_str):
    return [chel.attrib['n'] for chel in root.find('b[@n=\'{0}\']'.format(book_str)).findall('c')]


