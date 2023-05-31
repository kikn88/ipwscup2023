#!/bin/bash

source test-0config.sh

# reidetify D with B and output the estimated indexs to E
pytest rlink2.py $B  $D  $E

# evaulate the correctly reidentified rate 
pytest lmark2.py  $E  $X
