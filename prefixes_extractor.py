# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbpedia: <http://dbpedia.org/resource/>
PREFIX dataset: <http://dbpedia.org/ontology/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
PREFIX dbpprop: <http://dbpedia.org/property/>

select distinct ?prettyName ?property where {
  { select distinct ?property where {
      [ a dbpedia-owl:Person ; ?property [] ]
    } }
  values (?prefixURI ?prefixName) {
    (dbpedia-owl: "dbpedia-owl")
    (dbpprop:     "dbpprop")
    (foaf:        "foaf")
    (dataset: "dataset")
  }
  filter strstarts(str(?property),str(?prefixURI))
  bind(concat(?prefixName,":",strafter(str(?property),str(?prefixURI))) as ?prettyName)
}
limit 1000
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

params_query = dict()
for result in results['results']["bindings"]:
    params_query[result['prettyName']['value'].split(':')[1]] = { "query" : result['prettyName']['value'], "name" : result['prettyName']['value'].split(':')[1] }

print params_query    
