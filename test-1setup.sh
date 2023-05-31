#!/bin/bash

source test-0config.sh

test -d $Csv || mkdir $Csv

# Download NHEANS dataset from CDC website. It takes few seconds. 
pytest activ_diabet10.py $A


