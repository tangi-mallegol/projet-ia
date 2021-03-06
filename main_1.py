# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 09:29:48 2016

@author: guish
"""

from SPARQLWrapper import SPARQLWrapper, JSON
import nltk

sentence = """Where is Paris ?"""
tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)

for element in tagged:
    
    if element[1] == "NNP":
        
        subject = element[0]
        print subject


sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
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
    WHERE { <http://dbpedia.org/resource/"""+ subject+ """> ?r ?p }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    
    print result
    
    #if result["r"]["value"] == "http://dbpedia.org/ontology/wikiPageRedirects":
        
        #print(result["p"]["value"])

# PREFIX dataset: <http://dbpedia.org/ontology/>

# PREFIX foaf: <http://xmlns.com/foaf/0.1/>

# SELECT ?name ?influencedBy
# WHERE
# {
#   {
#   ?uri a dataset:Philosopher  .
#   ?uri dataset:influencedBy ?influencedBy   .
#   ?uri dataset:birthPlace ?birthPlace   .
#   ?uri foaf:name ?name   .
#   filter regex(?birthPlace, 'France', 'i')   .
#   filter regex(?influencedBy, 'Test Name 1', 'i')   .
#   }
#   UNION
#   {
#   ?uri a dataset:Philosopher  .
#   ?uri dataset:influencedBy ?influencedBy   .
#   ?uri dataset:birthPlace ?birthPlace   .
#   ?uri foaf:name ?name   .
#   filter regex(?birthPlace, 'France', 'i')   .
#   filter regex(?influencedBy, 'Test Name 2', 'i')   .
#   }
# }
# LIMIT  40