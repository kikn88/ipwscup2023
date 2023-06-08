#!/bin/bash

source test-0config.sh

# anonymization: rr for categorical attributes, and dp for numerical attributes
pytest rr.py $B  0.9 $Csv/c-tmp.csv  0_2_3_4_6_7_10
pytest lap.py $Csv/c-tmp.csv 1_5 1.0_2.0 $C

# format check
pytest checkC.py $B $C

# quantify the utility loss
pytest umark2.py $B $C


