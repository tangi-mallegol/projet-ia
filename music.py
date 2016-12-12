# coding: utf-8

import re

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
            return ('?x <http://dbpedia.org/ontology/Band> ?band)', 'FILTER regex(?band, ".*' + sujet +'.*") ')
        return ""

class Chanteur:
    self.regex = re.compiler('.*(singer).*')

    def get_filter(query, sujet):
        if(self.regex.match(query)):
            return ('?x <http://dbpedia.org/ontology/Singer> ?singer', 'FILTER regex(?singer, ".*' + sujet +'.*") ')
        return ""

class Auteur:
    self.regex = re.compiler('.*(author).*')

    def get_filter(query, sujet):
        if(self.regex.match(query)):
            return ('?x <http://dbpedia.org/ontology/Author> ?author', 'FILTER regex(?author, ".*' + sujet +'.*") ')
        return ""