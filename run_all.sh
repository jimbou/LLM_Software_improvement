#!/bin/bash

# Run all the scripts in the correct order
# python3 test.py --benchmark lpg_params
# python3 test.py --benchmark minisat_hack_params
# python3 test.py --benchmark minisat_hack_source
python3 test.py --benchmark minisat_params
# python3 test.py --benchmark minisat_source
python3 test.py --benchmark sat4j_params
# python3 test.py --benchmark sat4j_source
python3 test.py --benchmark scipy_params
python3 test.py --benchmark weka_params
# python3 test.py --benchmark weka_source
python3 test.py --benchmark zlib_params