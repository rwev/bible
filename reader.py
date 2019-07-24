from glob import glob
from os.path import splitext, basename
import xml.etree.ElementTree as ET

root = ET.parse('translations/NIV.xml')

def get_translations():
    return [splitext(basename(f))[0] for f in glob('translations/*.xml')]

def get_books():
    return [bel.attrib['n'] for bel in root.findall('b')]

def get_chapters(book_str):
    return [chel.attrib['n'] for chel in root.find('b[@n=\'{0}\']'.format(book_str)).findall('c')]

def get_verses_elements(book_str, chapter_str):
    return root.find('b[@n=\'{0}\']'.format(book_str)).find('c[@n=\'{0}\']'.format(chapter_str)).findall('v')

def get_verses(book_str, chapter_str):
    return [vel.attrib['n'] for vel in
            get_verses_elements(book_str, chapter_str)]
 
def get_chapter_text(book_str, chapter_str):
    vels = get_verses_elements(book_str, chapter_str)
    return ' '.join(map(lambda v: '({0}) {1}'.format(v.attrib['n'], v.text), vels))



