import re

# This is the final step after the final post condition has been generated. This is the prompt template that will be filled in with the problem description, the program,
# and the final output hints (postcondition). It instructs the model to determine whether the program
# satisfies the description and output specification, and asks it to return either "True" or "False".

simple_source_template = """
Given the program below, optimize its runtime performance while maintaining functionality. 

### Program:
{src_code}
Give us the optimized program for the best runtime performance.

"""
simple_source_with_doc_template = """
Given the program below and its documentation, optimize its runtime performance while maintaining functionality.

### Program:
{src_code}

### Documentation:
{documentation}

Give us the optimized program for the best runtime performance.
"""
source_with_hints_template = """
The program below may have runtime bottlenecks. Improve its performance by:
- Replacing inefficient algorithms with more optimized ones.
- Simplifying logic while maintaining correctness.
- Eliminating unnecessary computations.
- Enhancing the use of data structures for better efficiency.

### Program:
{src_code}

Give us the optimized program for the best runtime performance.
"""
source_with_hints_and_doc_template = """
The program below may have runtime bottlenecks. Use the accompanying documentation to better understand its functionality and constraints. 
Optimize its performance by:
- Replacing inefficient algorithms with more optimized ones.
- Simplifying logic while maintaining correctness.
- Eliminating unnecessary computations.
- Enhancing the use of data structures for better efficiency.

### Program:
{src_code}

### Documentation:
{documentation}

Give us the optimized program for the best runtime performance.
"""

source_with_cot_template = """
The program below may be inefficient. Optimize its runtime performance by following these steps:
1. Analyze the program to identify parts that could be computationally expensive or inefficient.
2. Suggest specific changes to improve the code's efficiency.
3. Provide the updated version of the program along with an explanation of how the changes reduce runtime.

### Program:
{src_code}

### Optimized Program:
"""

source_with_cot_and_doc_template = """
The program below may be inefficient. Use the accompanying documentation to understand its functionality and constraints.
Optimize its runtime performance by following these steps:
1. Analyze the program to identify parts that could be computationally expensive or inefficient.
2. Suggest specific changes to improve the code's efficiency.
3. Provide the updated version of the program along with an explanation of how the changes reduce runtime.

### Program:
{src_code}

### Documentation:
{documentation}

### Optimized Program:
"""


simple_params_template = """
Given the parameter configuration below, optimize it for runtime efficiency. 

### Parameters:
{parameters}
Give us the optimized parameters for the best runtime performance.

"""

simple_params_with_doc_template = """
The parameter configuration below may impact runtime performance. Use the accompanying documentation to understand the purpose and constraints of each parameter. 
Optimize the configuration to improve runtime performance while maintaining functionality.

### Parameters:
{parameters}

### Documentation:
{documentation}

### Optimized Parameters:
"""

params_with_hints_template = """
The parameter configuration below may impact runtime performance. Improve the configuration by:
- Identifying parameters most critical to performance.
- Suggesting values or combinations that reduce runtime.
- Maintaining the functionality of the system.

### Parameters:
{parameters}

### Optimized Parameters:
"""

params_with_hints_and_doc_template = """
The parameter configuration below may impact runtime performance. Use the accompanying documentation to understand the functionality and constraints of the parameters. 
Improve the configuration by:
- Identifying parameters most critical to performance.
- Suggesting values or combinations that reduce runtime.
- Maintaining the functionality of the system.

### Parameters:
{parameters}

### Documentation:
{documentation}

### Optimized Parameters:
"""

params_with_cot_template = """
The parameter configuration below may impact runtime performance. Optimize the configuration by following these steps:
1. Analyze the parameters to identify those most likely to influence runtime.
2. Suggest specific adjustments or combinations that could improve performance.
3. Provide the optimized configuration along with an explanation of how the changes impact runtime performance.

### Parameters:
{parameters}

### Optimized Parameters:
"""

params_with_cot_and_doc_template = """
The parameter configuration below may impact runtime performance. Use the accompanying documentation to understand the purpose and constraints of each parameter.
Optimize the configuration by following these steps:
1. Analyze the parameters to identify those most likely to influence runtime.
2. Suggest specific adjustments or combinations that could improve performance.
3. Provide the optimized configuration along with an explanation of how the changes impact runtime performance.

### Parameters:
{parameters}

### Documentation:
{documentation}

### Optimized Parameters:
"""



# Parses the model response to see if it responded True or False

def extract_correctness_from_response(response_content: str) -> str:
    pattern = r"Correctness:\s*\*\*(.*?)\*\*|Correctness:\s*(True|False)"
    match = re.findall(pattern, response_content)
    if match:
        if match[-1][0]:
            return match[-1][0].strip()
        elif match[-1][1]:
            return match[-1][1].strip()
    return response_content

# This function handles the core logic for checking program correctness using a naive entailment approach.
def simple_source(model, src_code):
    prompt = simple_source_template.format(src_code=src_code
                                                        )
    
    response = model.query(prompt)
    return response

def simple_source_with_doc(model, src_code, documentation):
    prompt = simple_source_with_doc_template.format(src_code=src_code,
                                                        documentation=documentation)
    
    response = model.query(prompt)
    return response

def source_with_hints(model, src_code):
    prompt = source_with_hints_template.format(src_code=src_code)
    
    response = model.query(prompt)
    return response

def source_with_hints_and_doc(model, src_code, documentation):
    prompt = source_with_hints_and_doc_template.format(src_code=src_code,
                                                        documentation=documentation)
    
    response = model.query(prompt)
    return response

def source_with_cot(model, src_code):
    prompt = source_with_cot_template.format(src_code=src_code)
    
    response = model.query(prompt)
    return response

def source_with_cot_and_doc(model, src_code, documentation):
    prompt = source_with_cot_and_doc_template.format(src_code=src_code,
                                                        documentation=documentation)
    
    response = model.query(prompt)
    return response

def simple_params(model, parameters):
    prompt = simple_params_template.format(parameters=parameters)
    
    response = model.query(prompt)
    return response

def simple_params_with_doc(model, parameters, documentation):
    prompt = simple_params_with_doc_template.format(parameters=parameters,
                                                        documentation=documentation)
    
    response = model.query(prompt)
    return response

def params_with_hints(model, parameters):
    prompt = params_with_hints_template.format(parameters=parameters)
    
    response = model.query(prompt)
    return response

def params_with_hints_and_doc(model, parameters, documentation):
    prompt = params_with_hints_and_doc_template.format(parameters=parameters,
                                                        documentation=documentation)
    
    response = model.query(prompt)
    return response

def params_with_cot(model, parameters):
    prompt = params_with_cot_template.format(parameters=parameters)
    
    response = model.query(prompt)
    return response

def params_with_cot_and_doc(model, parameters, documentation):
    prompt = params_with_cot_and_doc_template.format(parameters=parameters,
                                                        documentation=documentation)
    
    response = model.query(prompt)
    return response

# TBD: WHAT OTHER APPROACH CAN BE USED OTHER THAN NAIVE?