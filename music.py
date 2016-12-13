# coding: utf-8
requete_exemple = """PREFIX dbpedia: <http://dbpedia.org/resource/>
PREFIX dataset: <http://dbpedia.org/ontology/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dbpprop: <http://dbpedia.org/property/>
PREFIX mo:  <http://purl.org/ontology/mo/>

select ?name, ?member
where {
?x <http://dbpedia.org/ontology/associatedBand> ?name 
Optional {
?x <http://dbpedia.org/ontology/formerBandMember> ?member
}
FILTER(regex(?name, ".*Beatles.*"))

}"""

import re

def BuildRequest(query, sujet):
    query = ""
    artiste = Artiste()
    band = Band()
    chanteur = Chanteur()
    auteur = Auteur()
    memberof = Memberof()
    

class Artiste:
    def __init__():
        self.regex = re.compile('.*(artist).*')

    def get_filter(query, sujet):
        if(self.regex.match(query)):
            return ('?x <http://dbpedia.org/ontology/musicalArtist> ?artist)', 'FILTER regex(?artist, ".*' + sujet +'.*") ')
        return ""

class Band:
    def __init__():
        self.regex = re.compiler('.*(band|group).*')

    def get_filter(query, sujet):
        if(self.regex.match(query)):
            return ('?x <http://dbpedia.org/ontology/associatedBand> ?band)', 'FILTER regex(?band, ".*' + sujet +'.*") ')
        return ""

class Chanteur:
    def __init__():
        self.regex = re.compiler('.*(singer).*')

    def get_filter(query, sujet):
        if(self.regex.match(query)):
            return ('?x <http://dbpedia.org/ontology/singer> ?singer', 'FILTER regex(?singer, ".*' + sujet +'.*") ')
        return ""

class Auteur:
    def __init__():
        self.regex = re.compiler('.*(author).*')

    def get_filter(query, sujet):
        if(self.regex.match(query)):
            return ('?x <http://dbpedia.org/ontology/author> ?author', 'FILTER regex(?author, ".*' + sujet +'.*") ')
        return ""

class Memberof:
    def __init__():
        self.regex = re.compiler('.*(member of).*')

    def get_filter(query, sujet):
        if(self.regex.match(query)):
            return ('?x <http://dbpedia.org/ontology/formerBandMember> ?formerBandMember', 'FILTER regex(?formerBandMember, ".*' + sujet +'.*") ')
        return ""