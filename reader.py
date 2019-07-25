from glob import glob
from os.path import splitext, basename
import xml.etree.ElementTree as ET

class Reader():
    def __init__(self):
        self.root_tuple = (None, None)
        
    def set_root(self, translation_str):
        if (self.root_tuple[0] == translation_str):
            return
        self.root_tuple = (translation_str,                ET.parse('translations/{0}.xml'.format(translation_str)))

    def get_translations(self):
        return [splitext(basename(f))[0] for f in glob('translations/*.xml')]

    def get_books(self):
        return [bel.attrib['n'] for bel in self.root_tuple[1].findall('b')]

    def get_chapters(self, book_str):
        return [chel.attrib['n'] for chel in self.root_tuple[1].find('b[@n=\'{0}\']'.format(book_str)).findall('c')]

    def get_verses_elements(self, book_str, chapter_str):
        return self.root_tuple[1].find('b[@n=\'{0}\']'.format(book_str)).find('c[@n=\'{0}\']'.format(chapter_str)).findall('v')

    def get_verses(self, book_str, chapter_str):
        return [vel.attrib['n'] for vel in    self.get_verses_elements(book_str, chapter_str)]
 
    def get_chapter_text(self, book_str, chapter_str):
        vels = self.get_verses_elements(book_str, chapter_str)
        return ' '.join(map(lambda v: '({0}) {1}'.format(v.attrib['n'], v.text), vels))
