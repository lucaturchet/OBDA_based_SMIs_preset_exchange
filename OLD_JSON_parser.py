#!/usr/bin/env python3

'''Author : Luca Turchet '''

import json
import collections

def flatten(x):
    if isinstance(x, dict) :
        return [x]
    elif isinstance(x, collections.Iterable) :
        return [a for i in x for a in flatten(i)]
    else:
        return [x]



#############################################################################

#Load the JSON file into a dictionary

with open('config_sushi_simple_daw_v1.json', 'r') as f:
    loaded_json_dict = json.load(f)

'''
for x in loaded_json_dict:
    print("%s: %s" % (x, loaded_json_dict[x]))
'''



#Now put the json tags of interest into variables

tracks = loaded_json_dict["tracks"]
#print(tracks)


get_tracks_list = flatten(tracks)


for item in get_tracks_list :
    print(item)



#do something like:
#name_track = tracks["name"]
##print(name_track)


#Now that I can have all json tags into variables I can create the file turtle

#1) create a turtle file

#2) aggoingi i prefissi che servono

#3) for each variable create the triple, knowing the ontology

import rdflib
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD
from rdflib import Graph
g = Graph()
g.bind("foaf", FOAF)

name = Literal('Bob')
bob = rdflib.term.URIRef(u'http://example.org/people/bob')
linda = rdflib.term.URIRef(u'http://example.org/people/linda')


g.add((bob, RDF.type, FOAF.Person))
g.add((bob, FOAF.name, name))
g.add((bob, FOAF.knows, linda))
g.add((linda, RDF.type, FOAF.Person))
g.add((linda, FOAF.name, Literal("Linda")))

print(g.serialize(format="turtle").decode("utf-8"))


#Now that I have created the turtle prefixes and triples I save them in a .ttl file











































