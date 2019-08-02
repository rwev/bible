from glob import glob
from os.path import splitext, basename, dirname, join
import xml.etree.ElementTree as ET

TRANSLATIONS_DIR = join(dirname(__file__), "translations")


class Reader:
    def __init__(self):
        self._load_roots()

    def _load_roots(self):
        self._current_root = (None, None)
        self._roots = {}
        for ts in self.get_translations():
            self._roots[ts] = self._get_root(ts)

    def _get_root(self, translation_str):
        return ET.parse("{0}/{1}.xml".format(TRANSLATIONS_DIR, translation_str))

    def set_root(self, translation_str):
        if self._current_root[0] == translation_str:
            return
        self._current_root = (translation_str, self._roots[translation_str])

    def get_translations(self):
        return [
            splitext(basename(f))[0] for f in glob("{0}/*.xml".format(TRANSLATIONS_DIR))
        ]

    def get_books(self):
        return [bel.attrib["n"] for bel in self._current_root[1].findall("b")]

    def get_chapters(self, book_str):
        return [
            chel.attrib["n"]
            for chel in self._current_root[1]
            .find("b[@n='{0}']".format(book_str))
            .findall("c")
        ]

    def get_verses_elements(self, book_str, chapter_str):
        return (
            self._current_root[1]
            .find("b[@n='{0}']".format(book_str))
            .find("c[@n='{0}']".format(chapter_str))
            .findall("v")
        )

    def get_verses(self, book_str, chapter_str):
        return [
            vel.attrib["n"] for vel in self.get_verses_elements(book_str, chapter_str)
        ]

    def get_chapter_text(self, book_str, chapter_str, verse_start=1):
        vels = filter(
            lambda v: int(v.attrib["n"]) >= int(verse_start),
            self.get_verses_elements(book_str, chapter_str),
        )
        return " ".join(map(lambda v: "({0}) {1}".format(v.attrib["n"], v.text), vels))
