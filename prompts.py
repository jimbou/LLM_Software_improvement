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
Reply in the format:
'''plaintext
The new parameters in the exact same format just with the new values
'''

"""

simple_params_with_doc_template = """
The parameter configuration below may impact runtime performance. Use the accompanying documentation to understand the purpose and constraints of each parameter. 
Optimize the configuration to improve runtime performance while maintaining functionality.

### Parameters:
{parameters}

### Documentation:
{documentation}

Reply in the format:
'''plaintext
The new parameters in the exact same format just with the new values
'''
"""

params_with_hints_template = """
The parameter configuration below may impact runtime performance. Improve the configuration by:
- Identifying parameters most critical to performance.
- Suggesting values or combinations that reduce runtime.
- Maintaining the functionality of the system.

### Parameters:
{parameters}

Reply in the format:
'''plaintext
The new parameters in the exact same format just with the new values
'''
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

Reply in the format:
'''plaintext
The new parameters in the exact same format just with the new values
'''
"""

params_with_cot_template = """
The parameter configuration below may impact runtime performance. Optimize the configuration by following these steps:
1. Analyze the parameters to identify those most likely to influence runtime.
2. Suggest specific adjustments or combinations that could improve performance.
3. Provide the optimized configuration along with an explanation of how the changes impact runtime performance.

### Parameters:
{parameters}

Reply in the format:
'''plaintext
The new parameters in the exact same format just with the new values
'''
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

Reply in the format:
'''plaintext
The new parameters in the exact same format just with the new values
'''
"""