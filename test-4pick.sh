#!/bin/bash

source test-0config.sh

# performed by the organizer (judge)
# sample random records from C and write the sampled record to D and the sampled index (hidden) to X
pytest pick2.py  $C  $D  $X

