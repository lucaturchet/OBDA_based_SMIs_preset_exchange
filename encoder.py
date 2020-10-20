#!/usr/bin/env python3

'''Author : Luca Turchet '''

import os, sys
import json
import pathlib


CURRENT_DIR     = pathlib.Path(__file__).parent.absolute()
CONFIG_SUSHI    = os.path.join(CURRENT_DIR,"config_files_elk/config_sushi_simple_daw_v1.json")
CONFIG_SENSEI   = os.path.join(CURRENT_DIR,"config_files_elk/config_sensei_simple_daw_v1.json")
CONFIG_MAPPINGS = os.path.join(CURRENT_DIR,"config_files_elk/mappings.json")

TTL_PREFIXES = """ 
@prefix smi:				<http://purl.org/ontology/iomust/smi> .
@prefix mo:					<http://purl.org/ontology/mo> .
@prefix sosa:				<http://www.w3.org/ns/sosa> .
@prefix mx:					<http://purl.org/ontology/studio/mixer/> .
@prefix con: 				<http://purl.org/ontology/studio/connectivity/> .
@prefix device:				<http://purl.org/ontology/studio/device> .
@prefix fx:					<https://w3id.org/aufx/ontology/1.0> .
@prefix studio:				<http://purl.org/ontology/studio/main> .
@prefix foaf: 				<http://xmlns.com/foaf/0.1/name> .
@prefix rdf:				<http://www.w3.org/1999/02/22-rdf-syntax-ns> .
"""


t_name = ''
t_mode = ''
i_engine_bus = ''
i_track_bus = ''
o_engine_bus = ''
o_track_bus = ''
p_name = ''
p_type = ''







def print_on_ttl_file(ttl_file, content):
    ttl_file.write(content)



def load_json_config(json_file):
    with open(json_file) as f:
        return json.load(f)


def parse_SUSHI(data):
    for t in data['tracks']:

        global t_name 
        global t_mode 
        global i_engine_bus
        global i_track_bus
        global o_engine_bus
        global o_track_bus
        global p_name
        global p_type

        t_name = t['name']
        t_mode = t['mode']
    for i in data['tracks'][0]['inputs']:
        i_engine_bus = i['engine_bus'] 
        i_track_bus = i['track_bus'] 
    for o in data['tracks'][0]['outputs']:
        o_engine_bus = o['engine_bus'] 
        o_track_bus = o['track_bus']
    for p in data['tracks'][0]['plugins']:
        p_name = p['name']
        p_type = p['type']      

                    




if __name__ == '__main__': 
    
    ttl_file = open(os.path.join(CURRENT_DIR,"preset.ttl"), "w")
    print_on_ttl_file(ttl_file, TTL_PREFIXES)

    data_SUSHI = load_json_config(CONFIG_SUSHI)
    parse_SUSHI(data_SUSHI)
    print(t_name)
    print(t_mode)
    print(i_engine_bus)
    print(i_track_bus)
    print(o_engine_bus)
    print(o_track_bus)
    print(p_name)
    print(p_type)
    # Here call function to write on ttl 
    # print_on_ttl_file(ttl_file, result of function that takes the parsed variables)

    ttl_file.close()


