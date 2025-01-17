import os
import re

def parse_and_restructure(input_dir):
    # Define the target output directory
    output_dir = f"Results/zlib_params_12_parsed"
    print("hello")
    for subdir in os.listdir(input_dir):
        subdir_path = os.path.join(input_dir, subdir)
        if os.path.isdir(subdir_path):
            print(f"Processing {subdir}")
            for numbered_dir in os.listdir(subdir_path):
                numbered_dir_path = os.path.join(subdir_path, numbered_dir)
                if os.path.isdir(numbered_dir_path):
                    print(f"Processing {numbered_dir}") 
                    response_file = os.path.join(numbered_dir_path, "0000.response.md")
                    if os.path.exists(response_file):
                        print(f"Processing {response_file}")
                        with open(response_file, "r") as file:
                            content = file.read()

                        # Extract the code block between ```plaintext``` or ```python```
                        match = re.search(r"```(?:plaintext|python)\n(.*?)\n```", content, re.DOTALL)
                        if match:
                            code_block = match.group(1)

                            # Remove comments from the code block
                            cleaned_code = re.sub(r"#.*", "", code_block).strip()
                            #remove every line of the cleaned code that starts with @
                            cleaned_code = re.sub(r"@.*", "", cleaned_code).strip()
                            #remove empty lines
                            cleaned_code = re.sub(r"\n\s*\n*", "\n", cleaned_code)
                            # Create the corresponding directory structure in the output directory
                            output_subdir_path = os.path.join(output_dir, subdir, numbered_dir)
                            os.makedirs(output_subdir_path, exist_ok=True)
                            print(f"Writing to {output_subdir_path}")
                            # Write the cleaned code block to a new file with the specified naming convention
                            output_file_name = f"zlib_params__{subdir}_{numbered_dir}.params"
                            output_file = os.path.join(output_subdir_path, output_file_name)
                            with open(output_file, "w") as output:
                                output.write(cleaned_code + "\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_directory>")
    else:
        input_directory = sys.argv[1]
        parse_and_restructure(input_directory)
