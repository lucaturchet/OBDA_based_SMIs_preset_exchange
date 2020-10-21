#!/usr/bin/env python3

'''Author : Luca Turchet '''

import os, sys
import json
import pathlib
import rdflib

CURRENT_DIR = pathlib.Path(__file__).parent.absolute()



class Decoder:

    def __init__(self, preset_file_location, pd_file_location):

        self.g = rdflib.Graph()
        self.g.parse(preset_file_location, format='turtle')
        for subj, pred, obj in self.g:
            if not (subj, pred, obj) in self.g:
                raise Exception("Iterator / Container Protocols are Broken!!")
        # For debug purposes    
        #print("rdflib Graph loaded successfully with {} triples".format(len(self.g)))
        #print(self.g.serialize(format="turtle").decode("utf-8"))
        #for triples in self.g:
        #    print(triples)
        # for s, p, o in self.g:
        #    print (s, p, o)    

        self.StereoChannel = rdflib.URIRef("http://purl.org/ontology/studio/mixer/StereoChannel")
        self.PressureSensor = rdflib.URIRef("http://purl.org/ontology/iomust/smi/PressureSensor")
        self.mapping_function = rdflib.URIRef("http://purl.org/ontology/iomust/smi/mapping_function")
        self.Delay = rdflib.URIRef("http://purl.org/ontology/studio/main/Delay")
        self.plugin_name = rdflib.URIRef("http://purl.org/ontology/iomust/smi/plugin_name")
        self.mdaDelay = rdflib.Literal('mdaDelay')
        self.rdftype = rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns/type")
        self.MappingTransform = rdflib.URIRef("http://purl.org/ontology/iomust/smi/MappingTransform")
        self.maps = rdflib.URIRef("http://purl.org/ontology/iomust/smi/maps")
        self.effect_name = rdflib.URIRef("https://w3id.org/aufx/ontology/1.0/name")
        self.Feedback = rdflib.Literal('Feedback')

        self.pd_file_name = pd_file_location


    def __enter__(self):
        self.pd_file = open(self.pd_file_name, 'w')
        return self

    def __exit__(self, *args):
        self.pd_file.close()
        
    def write_on_pd_file(self, content):
        self.pd_file.write(content)

    
    def decode(self):  

        mappingOfPressureSensor = ""
        mappedParameterOfPressureSensor = ""
    
        with d:
            d.write_on_pd_file("#N canvas 659 23 550 412 12;\r\n")

            if (None, None, self.StereoChannel) in self.g:
                d.write_on_pd_file(
f"#X obj 7 13 adc~ 1 2;\r\n"
f"#X obj 7 369 dac~ 1 2;\r\n"                    
                )
                id_adc12 = 0
                id_dac12 = 1

            if (self.PressureSensor, self.mapping_function, None) in self.g:
                d.write_on_pd_file("#X obj 158 13 adc~ 3;\r\n")
                id_adc3 = 2

                for s, p, o in self.g.triples((self.PressureSensor, self.mapping_function, None)):
                    #I keep track of the mapping between the sensor of and the sound parameter
                    mappingOfPressureSensor = o  

                    for s, p, o in self.g.triples((mappingOfPressureSensor, self.maps, None)):
                        mappedParameterOfPressureSensor = o
                        if (mappedParameterOfPressureSensor, self.effect_name, self.Feedback) in self.g:
                            #The system knows what are the inlets of an object associated to a certain parameter
                            feedback_parameter_inlet = 2 


            # Here I search for all effects (for the sake of the example I only check for the delay effect). 
            # If a certain effect category is found then I search for a specific implementation of that effect.
            # Note: this code assumes that the instrument already has a number of effects implementation 
            # including the one of this example (i.e., mdaDelay).
            if (None, None, self.Delay) in self.g:
                if (None, self.plugin_name, self.mdaDelay) in self.g:
                    d.write_on_pd_file("#X obj 7 337 _delay_feedback, f 22;\r\n") #Here I assume that the existing pd subpatch "_delay_feedback" corresponds to mdaDelay implementation
                    id_mdadelay = 3

            #The following lines are just a standard way to process the incoming sensor values. They could set automatically by the internal system of the instrument or they could be set by the user
            d.write_on_pd_file(
f"#X obj 158 111 lop~;\r\n"
f"#X obj 158 147 snapshot~;\r\n"
f"#X obj 158 274 change;\r\n"
f"#X obj 158 232 maxlib/scale 0.3 0.6 0 1 0;\r\n"
f"#X obj 158 193 clip 0.3 0.6;\r\n"
f"#X msg 183 80 50;\r\n"
f"#X obj 385 12 loadbang;\r\n"
f"#X msg 385 38 1;\r\n"
f"#X obj 385 71 metro 100;\r\n"
            )   
            id_lop = 4
            id_snapshot = 5
            id_change = 6
            id_maxlibscale = 7
            id_clip = 8
            id_msf50 = 9
            id_loadbang = 10
            id_msg1 = 11
            id_metro = 12



            # At this point all the objects have been created as a result of the translation process of the ontology concepts into pure data.
            # In the following lines we simply connect the objects together. From Pd cdocumentation:
            # "Almost all objects can be interconnected with wires in PureData. Each wire is stored in the file using the following syntax:
            # #X connect [source]? [outlet_number]? [sink]? [inlet_number]?;\r\n ""

            d.write_on_pd_file(
f"#X connect {id_adc12} 0 {id_mdadelay} 0;\r\n"
f"#X connect {id_adc12} 1 {id_mdadelay} 0;\r\n"
f"#X connect {id_adc3} 0 {id_lop} 0;\r\n"
f"#X connect {id_mdadelay} 0 {id_dac12} 0;\r\n"
f"#X connect {id_mdadelay} 0 {id_dac12} 1;\r\n"
f"#X connect {id_lop} 0 {id_snapshot} 0;\r\n"
f"#X connect {id_snapshot} 0 {id_clip} 0;\r\n"
f"#X connect {id_change} 0 {id_mdadelay} {feedback_parameter_inlet};\r\n"
f"#X connect {id_maxlibscale} 0 {id_change} 0;\r\n"
f"#X connect {id_clip} 0 {id_maxlibscale} 0;\r\n"
f"#X connect {id_msf50} 0 {id_lop} 1;\r\n"
f"#X connect {id_loadbang} 0 {id_msg1} 0;\r\n"
f"#X connect {id_loadbang} 0 {id_msf50} 0;\r\n"
f"#X connect {id_msg1} 0 {id_metro} 0;\r\n"
f"#X connect {id_metro} 0 {id_snapshot} 0;\r\n"
)





if __name__ == '__main__': 
    
    ttl_file_name = os.path.join(CURRENT_DIR,"output_preset_ttl_file/preset.ttl")
    pd_file_name = os.path.join(CURRENT_DIR,"output_pd_sound_engine_file/sound_engine.pd")
    d = Decoder(ttl_file_name, pd_file_name)
    d.decode()