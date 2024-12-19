import argparse
import shutil
import json
import os
from pathlib import Path
from model import get_model

import query
from datetime import datetime




def run_simple_source(benchmark,datetime_string, model_name, temperature, run, source_code):
    log_dir = f"{benchmark}/{datetime_string}/{model_name}/{run}"
    
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    model = get_model(model_name, temperature, Path(log_dir))
    query.simple_source(model, source_code)

def run_simple_params(benchmark, datetime_string, model_name, temperature, run, params):
    log_dir = f"{benchmark}/{datetime_string}/{model_name}/{run}"
    
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    model = get_model(model_name, temperature, Path(log_dir))
    query.simple_params(model, params)




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
            for i in range(1, 2):  
                
                log_dir_simple = f"{benchmark}/{datetime_string}/{model}/simple/{i}"
                Path(log_dir_simple).mkdir(parents=True, exist_ok=True)
                model_simple = get_model(model, 0.7, Path(log_dir_simple))
                query.simple_source(model_simple, source)

                log_dir_simple_with_doc = f"{benchmark}/{datetime_string}/{model}/simple_with_doc/{i}"
                Path(log_dir_simple_with_doc).mkdir(parents=True, exist_ok=True)
                model_simple_with_doc = get_model(model, 0.7, Path(log_dir_simple_with_doc))
                query.simple_source_with_doc(model_simple_with_doc, source, documentation)   

                log_dir_with_hints = f"{benchmark}/{datetime_string}/{model}/with_hints/{i}"
                Path(log_dir_with_hints).mkdir(parents=True, exist_ok=True)
                model_with_hints = get_model(model, 0.7, Path(log_dir_with_hints))
                query.source_with_hints(model_with_hints, source)   

                log_dir_with_hints_and_doc = f"{benchmark}/{datetime_string}/{model}/with_hints_and_doc/{i}"
                Path(log_dir_with_hints_and_doc).mkdir(parents=True, exist_ok=True)
                model_with_hints_and_doc = get_model(model, 0.7, Path(log_dir_with_hints_and_doc))
                query.source_with_hints_and_doc(model_with_hints_and_doc, source, documentation)

                log_dir_with_cot = f"{benchmark}/{datetime_string}/{model}/with_cot/{i}"
                Path(log_dir_with_cot).mkdir(parents=True, exist_ok=True)
                model_with_cot = get_model(model, 0.7, Path(log_dir_with_cot)) 
                query.source_with_cot(model_with_cot, source)

                log_dir_with_cot_and_doc = f"{benchmark}/{datetime_string}/{model}/with_cot_and_doc/{i}"
                Path(log_dir_with_cot_and_doc).mkdir(parents=True, exist_ok=True)
                model_with_cot_and_doc = get_model(model, 0.7, Path(log_dir_with_cot_and_doc))
                query.source_with_cot_and_doc(model_with_cot_and_doc, source, documentation) 


    elif "params" in benchmark:
        #run the benchmark with the params
        
        for model in models:
            for i in range(1, 2):   
                log_dir_simple = f"{benchmark}/{datetime_string}/{model}/simple/{i}"
                Path(log_dir_simple).mkdir(parents=True, exist_ok=True)
                model_simple = get_model(model, 0.7, Path(log_dir_simple))
                query.simple_params(model_simple, source)

                log_dir_simple_with_doc = f"{benchmark}/{datetime_string}/{model}/simple_with_doc/{i}"
                Path(log_dir_simple_with_doc).mkdir(parents=True, exist_ok=True)
                model_simple_with_doc = get_model(model, 0.7, Path(log_dir_simple_with_doc))
                query.simple_params_with_doc(model_simple_with_doc, source, documentation)   

                log_dir_with_hints = f"{benchmark}/{datetime_string}/{model}/with_hints/{i}"
                Path(log_dir_with_hints).mkdir(parents=True, exist_ok=True)
                model_with_hints = get_model(model, 0.7, Path(log_dir_with_hints))
                query.params_with_hints(model_with_hints, source)   

                log_dir_with_hints_and_doc = f"{benchmark}/{datetime_string}/{model}/with_hints_and_doc/{i}"
                Path(log_dir_with_hints_and_doc).mkdir(parents=True, exist_ok=True)
                model_with_hints_and_doc = get_model(model, 0.7, Path(log_dir_with_hints_and_doc))
                query.params_with_hints_and_doc(model_with_hints_and_doc, source, documentation)

                log_dir_with_cot = f"{benchmark}/{datetime_string}/{model}/with_cot/{i}"
                Path(log_dir_with_cot).mkdir(parents=True, exist_ok=True)
                model_with_cot = get_model(model, 0.7, Path(log_dir_with_cot)) 
                query.params_with_cot(model_with_cot, source)

                log_dir_with_cot_and_doc = f"{benchmark}/{datetime_string}/{model}/with_cot_and_doc/{i}"
                Path(log_dir_with_cot_and_doc).mkdir(parents=True, exist_ok=True)
                model_with_cot_and_doc = get_model(model, 0.7, Path(log_dir_with_cot_and_doc))
                query.params_with_cot_and_doc(model_with_cot_and_doc, source, documentation) 

    else:
        raise ValueError("Invalid benchmark name")
    

    
 