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
sparql_base_req = {
    'who': {
        'member': "select distinct ?name where {?x dbpedia-owl:%s ?name FILTER (regex(?name, '.*%s.*','i'))}",
        'default':  "select distinct ?name where {?x dbpedia-owl:%s ?name FILTER (regex(?name, '.*%s.*','i'))}"
    },
    'where': {
        'born':  "select distinct ?born where {?x dbpedia:placeOfBirth ?born . ?x dbpedia-owl:%s ?name FILTER (regex(?name, '.*%s.*','i'))}",
        'live': "select distinct ?name where {?x dbpedia-owl:%s ?name FILTER (regex(?name, '.*%s.*','i'))}"
    },
    'what': {
        'album': "select distinct ?album, ?albumName where { ?album a dbpedia-owl:Album . ?album rdfs:label ?albumName . ?album dbpedia-owl:artist dbpedia:%s. filter (lang(?albumName) = '' || langMatches(lang(?albumName), 'en'))}"
    }
}

sparql_base_req['abstract'] = "select distinct ?data where {<%s> dbpedia-owl:abstract ?data filter (lang(?data) = '' || langMatches(lang(?data), 'en'))}"

import_request = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbpedia: <http://dbpedia.org/resource/>
    PREFIX dataset: <http://dbpedia.org/ontology/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
    PREFIX dbpprop: <http://dbpedia.org/property/>"""

SUBJECT_CONTEXT = {}
def build_client_res(uuid, question):
    tokens = nltk.word_tokenize(question)
    tagged = nltk.pos_tag(tokens)
    print tagged
    print uuid

    if get_WP(tagged).lower() == "who":
        if get_subject(tagged) in sparql_base_req['who']:

            query = sparql_base_req['who']['member'] % ('associatedBand', get_object(uuid, tagged))
            return "Sorry, I don't know '" + get_object(uuid, tagged).replace(".*", " ") + "'."

        else:

            query = sparql_base_req['who']['default'] % ('associatedBand', get_object(uuid, tagged))
            results = send_sparql_query(query)

            print results

            if len(results) == 0:
                query = sparql_base_req['who']['default'] % ('musicalArtist', get_object(uuid, tagged))
                results = send_sparql_query(query)

            if len(results) == 0:
                query = sparql_base_req['who']['default'] % ('person', get_object(uuid, tagged))
                results = send_sparql_query(query)


            if len(results) > 0:
                name = results[0]['name']['value'].split('/')[-1]
                query = sparql_base_req['abstract'] % results[0]['name']['value']
                results = send_sparql_query(query)
                abstract = results[0]['data']['value'].split('.')[0] + ". "
                #abstract = re.sub(r'[.*]', '', abstract)
                info = '<a href="https://en.wikipedia.org/wiki/%s" target="_blank">More informations.</a>' % name
                return abstract + info
            return "Sorry, I don't know '" + get_object(uuid, tagged).replace(".*", " ") + "'."

    if get_WP(tagged).lower() == "what":

        # On trouve le groupe
        subject = get_subject(tagged)
        print subject
        object = get_object(uuid, tagged)
        print subject, object
        query = sparql_base_req['who']['default'] % ('associatedBand', object)
        results = send_sparql_query(query)

        if len(results) == 0:
            query = sparql_base_req['who']['default'] % ('musicalArtist', object)
            results = send_sparql_query(query)

        if len(results) == 0:
            query = sparql_base_req['who']['default'] % ('person', object)
            results = send_sparql_query(query)

        print results[0]['name']['value']
        name_object = results[0]['name']['value'].split('/')[-1]
        print name_object, 'lel', subject, object
        if sparql_base_req['what'][subject] != None:
            print 'before'
            query = sparql_base_req['what'][subject] % name_object
            print 'after'
            results = send_sparql_query(query)
            print 'lel', query
            if len(results) > 0:
                result_html = []
                for result in results:
                    print result['albumName']['value']
                    if not result['albumName']['value'] in result_html:
                        result_html.append(result['albumName']['value'])
                return "<br/>".join(result_html)
            return "Sorry, I don't know '" + name_object.replace(".*", " ") + "'."
        return "Sorry, I don't know '" + name_object.replace(".*", " ") + "'."


    # if get_WP(tagged).lower() == "where":
    #     query = sparql_base_req['where'] % ('associatedBand', get_object(uuid, tagged))

    #     results = send_sparql_query(query)

    #     print results

    #     if len(results) == 0:
    #         query = sparql_base_req['who'] % ('musicalArtist', get_object(uuid, tagged))
    #         results = send_sparql_query(query)

    #     if len(results) == 0:
    #         query = sparql_base_req['who'] % ('person', get_object(uuid, tagged))
    #         results = send_sparql_query(query)


    #     if len(results) > 0:
    #         name = results[0]['name']['value'].split('/')[-1]
    #         query = sparql_base_req['abstract'] % results[0]['name']['value']
    #         results = send_sparql_query(query)
    #         abstract = results[0]['data']['value'].split('.')[0] + ". "
    #         #abstract = re.sub(r'[.*]', '', abstract)
    #         info = '<a href="https://en.wikipedia.org/wiki/%s" target="_blank">More informations.</a>' % name
    #         return abstract + info
    #     return "Sorry, I don't know '" + get_object(uuid, tagged).replace(".*", " ") + "'."


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
    return get_tagged_word("(NN|NNS)", tagged_word)

def get_verb(tagged_word):
    return get_tagged_word("VB", tagged_word)

def get_object(uuid, tagged_word):
    res = get_tagged_word("NNP", tagged_word)
    if res == "":
        if uuid in SUBJECT_CONTEXT:
            res = SUBJECT_CONTEXT[uuid]
    else:
        SUBJECT_CONTEXT[uuid] = res

    return res

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
