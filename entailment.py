import re

# This is the final step after the final post condition has been generated. This is the prompt template that will be filled in with the problem description, the program,
# and the final output hints (postcondition). It instructs the model to determine whether the program
# satisfies the description and output specification, and asks it to return either "True" or "False".

simple_source_template = """
Given the program below, optimize its runtime performance while maintaining functionality. 
Focus on:
- Reducing computational complexity (e.g., replacing O(n^2) operations with O(n log n) if possible).
- Improving data structures for efficiency.
- Eliminating redundant operations.

### Program:
{src_code}
Give us the optimized program for the best runtime performance.

"""

simple_params_template = """
Given the parameter configuration below, optimize it for runtime efficiency. 
Focus on:
- Identifying the parameters most likely to impact performance.
- Suggesting values or combinations that minimize runtime without compromising functionality.

### Parameters:
{parameters}
Give us the optimized parameters for the best runtime performance.


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

def simple_params(model, parameters):
    prompt = simple_params_template.format(parameters=parameters)
    
    response = model.query(prompt)
    return response

# TBD: WHAT OTHER APPROACH CAN BE USED OTHER THAN NAIVE?