# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 09:29:48 2016

@author: guish
"""

from SPARQLWrapper import SPARQLWrapper, JSON
import nltk

sentences = [
    "Who is Daft Punk ?",
    "Where did john lennon live ?"
]
tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)

#dg = nltk.parse.parse_one(tokens)

def get_tagged_word(tag, tagged_word):
    for item in tagged_word:
        if item[1] == tag:
            return item[0]

    return None

print tagged

print get_tagged_word("WP", tagged)







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