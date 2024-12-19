import argparse
import shutil
import json
import os
from pathlib import Path
from model import get_model

import entailment
from datetime import datetime




def run_simple_source(benchmark,datetime_string, model_name, temperature, run, source_code):
    log_dir = f"{benchmark}/{datetime_string}/{model_name}/{run}"
    
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    model = get_model(model_name, temperature, Path(log_dir))
    entailment.simple_source(model, source_code)

def run_simple_params(benchmark, datetime_string, model_name, temperature, run, params):
    log_dir = f"{benchmark}/{datetime_string}/{model_name}/{run}"
    
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    model = get_model(model_name, temperature, Path(log_dir))
    entailment.simple_params(model, params)




if __name__ == '__main__':
    #get as argument the benchmark to run
    models =[ "gpt-4o-mini-2024-07-18", "meta-llama/Meta-Llama-3.1-70B-Instruct",  "qwen2.5-7b-instruct",  "gpt-3.5-turbo-0125" ]
    

        # Get current datetime
    current_datetime = datetime.now()

    # Convert to string
    datetime_string = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    argparser = argparse.ArgumentParser()
    argparser.add_argument("--benchmark", type=str, required=True)
    args = argparser.parse_args()
    benchmark = args.benchmark

    #from a folder with the benchmark name get the source.md file and the documentations.md file
    #parse the source.md file and get the source code
    #parse the documentations.md file and get the expected output
    
    with open(f"{benchmark}/source.md", "r") as f:
        source = f.read()
    with open(f"{benchmark}/documentation.md", "r") as f:
        documentation = f.read()
    
    #if benchmark contains the word source in it then we are in source mode and if it contains the word params we are in params mode
    if "source" in benchmark:
        #run the benchmark with the source code
        
        for model in models:
            for i in range(1, 6):   
                run_simple_source(benchmark, datetime_string, model, 0.7, i, source)


    elif "params" in benchmark:
        #run the benchmark with the params
        
        for model in models:
            for i in range(1, 2):   
                run_simple_params(benchmark, datetime_string, model, 0.7, i, source)
        pass
    else:
        raise ValueError("Invalid benchmark name")
    

    
 