#!/usr/bin/env python3

'''Author : Luca Turchet '''

import os, sys
import json
import pathlib
import contextlib


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




class Encoder:

    def __init__(self, file_location):
        self.ttl_file_name = file_location
        self.var_elk_configs = dict()

    def __enter__(self):
        self.ttl_file = open(self.ttl_file_name, 'w')
        return self

    def __exit__(self, *args):
        self.ttl_file.close()
        
    def write_on_ttl_file(self, content):
        self.ttl_file.write(content)

    def load_json_config(self, json_file):
        with open(json_file) as f:
            return json.load(f)
     
    def parse_SUSHI(self):
        with open(CONFIG_SUSHI) as f:
            data = json.load(f)

        for t in data['tracks']:
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
      
            dict_SUSHI  =   dict(
                                t_name = t_name, 
                                t_mode = t_mode, 
                                i_engine_bus = i_engine_bus, 
                                i_track_bus = i_track_bus, 
                                o_engine_bus = o_engine_bus,
                                o_track_bus = o_track_bus,
                                p_name = p_name,
                                p_type = p_type
                                )
            self.var_elk_configs.update(dict_SUSHI)


                                
    
    def parse_SENSEI(self):
        with open(CONFIG_SENSEI) as f:
            data = json.load(f)

            for s in data['sensors']:
                s_id = s['id']
                s_name = s['name']
                s_sensor_type = s['sensor_type']

            dict_SENSEI =   dict(
                                s_id = s_id,
                                s_name = s_name,
                                s_sensor_type = s_sensor_type
                                )
            self.var_elk_configs.update(dict_SENSEI)

    
    def parse_MAPPINGS(self):
        with open(CONFIG_MAPPINGS) as f:
            data = json.load(f) 

            for m in data['mappings']:
                m_mapping_id = m['mapping_id']
                m_sensor_id = m['sensor_id']
                m_name_effect = m['name_effect']
                m_effect_parameter = m['effect_parameter']
         
            dict_MAPPINGS = dict(
                                 m_mapping_id = m_mapping_id,
                                 m_sensor_id = m_sensor_id,
                                 m_name_effect = m_name_effect,
                                 m_effect_parameter = m_effect_parameter
                                )
            self.var_elk_configs.update(dict_MAPPINGS)




    def encode(self):
        e.parse_SUSHI()
        e.parse_SENSEI()
        e.parse_MAPPINGS()
        with e:
            e.write_on_ttl_file(TTL_PREFIXES)




                        
if __name__ == '__main__': 
    
    ttl_file_name = os.path.join(CURRENT_DIR,"preset.ttl")
    e = Encoder(ttl_file_name)
    e.encode()


    for k, v in e.var_elk_configs.items():
        print(k, v)



    # Here call function to write on ttl 
    # write_on_ttl_file(ttl_file, result of function that takes the parsed variables)


