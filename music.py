# coding: utf-8

import re

def BuildRequest(query, sujet):
    query = ""
    artiste = Artiste()
    band = Band()
    chanteur = Chanteur()
    auteur = Auteur()
    memberof = Memberof()

class Artiste:
    self.regex = re.compile('.*(artist).*')

    def get_filter(query, sujet):
        if(self.regex.match(query)):
            return ('?x <http://dbpedia.org/ontology/musicalArtist> ?artist)', 'FILTER regex(?artist, ".*' + sujet +'.*") ')
        return ""

class Band:
    self.regex = re.compiler('.*(band|group).*')

    def get_filter(query, sujet):
        if(self.regex.match(query)):
            return ('?x <http://dbpedia.org/ontology/associatedBand> ?band)', 'FILTER regex(?band, ".*' + sujet +'.*") ')
        return ""

class Chanteur:
    self.regex = re.compiler('.*(singer).*')

    def get_filter(query, sujet):
        if(self.regex.match(query)):
            return ('?x <http://dbpedia.org/ontology/singer> ?singer', 'FILTER regex(?singer, ".*' + sujet +'.*") ')
        return ""

class Auteur:
    self.regex = re.compiler('.*(author).*')

    def get_filter(query, sujet):
        if(self.regex.match(query)):
            return ('?x <http://dbpedia.org/ontology/author> ?author', 'FILTER regex(?author, ".*' + sujet +'.*") ')
        return ""

class Memberof:
    self.regex = re.compiler('.*(member of)')

    def get_filter(query, sujet):
        if(self.regex.match(query)):
            return ('?x <http://dbpedia.org/ontology/author> ?author', 'FILTER regex(?author, ".*' + sujet +'.*") ')
        return ""