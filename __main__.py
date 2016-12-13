# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 09:29:48 2016

@author: guish
"""

from SPARQLWrapper import SPARQLWrapper, JSON
import nltk
import re
import music

sentences = [
    "Who is Daft Punk ?",
    "Where John Lennon lived ?",
    "What album did Pink Floyd produce ?"
]


#dg = nltk.parse.parse_one(tokens)

import_request = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbpedia: <http://dbpedia.org/resource/>
    PREFIX dataset: <http://dbpedia.org/ontology/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
    PREFIX dbpprop: <http://dbpedia.org/property/>"""

def get_tagged_word(tag, tagged_word):
    subjects = []
    for item in tagged_word:
        if re.search(tag + "*", item[1]) <> None:
            subjects.append(item[0])
            #return item[0]

    return " ".join(subjects)

def get_WP(tagged_word):
    return get_tagged_word("WP", tagged_word)

def get_subject(tagged_word):
    return get_tagged_word("NN", tagged_word)

def get_verb(tagged_word):
    return get_tagged_word("VBZ", tagged_word)

def get_object(tagged_word):
    return get_tagged_word("NNP", tagged_word)


if __name__ == '__main__':
    tokens = nltk.word_tokenize(sentences[2])
    tagged = nltk.pos_tag(tokens)
    print tagged
    print get_WP(tagged)
    print get_subject(tagged)
    print get_verb(tagged)
    print get_object(tagged)
    
    







"""
for element in tagged:
    
    if element[1] == "NNP":
        
        subject = element[0]
        print subject


sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX : <http://dbpedia.org/resource/>
    PREFIX dbpedia2: <http://dbpedia.org/property/>
    PREFIX dbpedia: <http://dbpedia.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    

    SELECT *
    WHERE { <http://dbpedia.org/resource/"+ subject+ "> ?r ?p }
")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    
    print result
    
    #if result["r"]["value"] == "http://dbpedia.org/ontology/wikiPageRedirects":
        
        #print(result["p"]["value"])

"""