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
    "Who is Renaud ?",
    "What album did Pink Floyd produce ?"
]
sparql_base_req = {}

sparql_base_req['who'] = "select distinct ?name where {?x dbpedia-owl:%s ?name FILTER (regex(?name, '.*%s.*','i'))}"
sparql_base_req['abstract'] = "select distinct ?data where {<%s> dbpedia-owl:abstract ?data filter (lang(?data) = '' || langMatches(lang(?data), 'en'))}"

#dg = nltk.parse.parse_one(tokens)

import_request = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbpedia: <http://dbpedia.org/resource/>
    PREFIX dataset: <http://dbpedia.org/ontology/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
    PREFIX dbpprop: <http://dbpedia.org/property/>"""

def build_client_res(question):
    tokens = nltk.word_tokenize(question)
    tagged = nltk.pos_tag(tokens)

    if get_WP(tagged).lower() == "who":
        query = sparql_base_req['who'] % ('associatedBand', get_object(tagged))

        results = send_sparql_query(query)

        print results

        if len(results) == 0:
            query = sparql_base_req['who'] % ('musicalArtist', get_object(tagged))
            results = send_sparql_query(query)

        if len(results) == 0:
            query = sparql_base_req['who'] % ('person', get_object(tagged))
            results = send_sparql_query(query)


        if len(results) > 0:
            name = results[0]['name']['value'].split('/')[-1]
            query = sparql_base_req['abstract'] % results[0]['name']['value']
            results = send_sparql_query(query)
            abstract = results[0]['data']['value'].split('.')[0] + ". "
            #abstract = re.sub(r'[.*]', '', abstract)
            info = '<a href="https://en.wikipedia.org/wiki/%s" target="_blank">More informations.</a>' % name
            return abstract + info
        return "Sorry, I don't know '" + get_object(tagged).replace(".*", " ") + "'."



def get_tagged_word(tag, tagged_word):
    subjects = []
    for item in tagged_word:
        if re.search(tag + '$', item[1]):
            subjects.append(item[0])
            #return item[0]

    return ".*".join(subjects)

def get_WP(tagged_word):
    return get_tagged_word("WP", tagged_word)

def get_subject(tagged_word):
    return get_tagged_word("NN", tagged_word)

def get_verb(tagged_word):
    return get_tagged_word("VB", tagged_word)

def get_object(tagged_word):
    return get_tagged_word("NNP", tagged_word)

def send_sparql_query(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(import_request + query)
    sparql.setReturnFormat(JSON)
    res = sparql.query().convert()
    return res['results']['bindings']


if __name__ == '__main__':
    print build_client_res(sentences[2])







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


