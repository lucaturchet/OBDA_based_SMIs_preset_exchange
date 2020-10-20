#!/usr/bin/env python3

'''Author : Luca Turchet '''

import rdflib


#############################################################################

#1) Load the ttl file


#2) create the Pd file from the triples of the .ttl file
# Note: not all information in the .ttl file are necessary
# Note: the .ttl triples are sequential in the same order of the original JSON, which describes the
# chain of effects from input to output


#DigitalInput 0 and DigitalInput 1 -> adc~ 1 2
#DigitalOutput 0 and DigitalOutput 1 -> dac~ 1 2

#studio:Delay  -> here we search for the implementation of a Delay effect,
                # but ideally we would like first to search whether that exact Pluin exists

#fx:NumericParameter -> fx:name "Feedback"



#I simply have to insert in a file with extension .pd the strings, e.g.:

#N canvas 54 23 550 412 12;
#X obj 7 369 dac~ 1 2;
#X obj 7 13 adc~ 1;
#X obj 158 111 lop~;
#X obj 158 147 snapshot~;
#X obj 158 274 change;
#X obj 158 232 maxlib/scale 0.3 0.6 0 1 0;
#X obj 158 193 clip 0.3 0.6;
#X obj 7 337 _delay_feedback, f 22;
#X obj 158 13 adc~ 3;
#X msg 183 80 50;
#X text 214 82 lowpass cut-off;
#X obj 385 12 loadbang;
#X msg 385 33 1;
#X obj 385 71 metro 100;
#X connect 1 0 7 0;
#X connect 2 0 3 0;
#X connect 3 0 6 0;
#X connect 4 0 7 2;
#X connect 5 0 4 0;
#X connect 6 0 5 0;
#X connect 7 0 0 0;
#X connect 7 0 0 1;
#X connect 8 0 2 0;
#X connect 9 0 2 1;
#X connect 11 0 14 0;
#X connect 12 0 13 0;
#X connect 12 0 9 0;
#X connect 13 0 11 0;
#X connect 14 0 3 0;





