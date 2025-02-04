import os
import subprocess
import time
import json
from pathlib import Path
import statistics



def run_command(command, directory =None):
    """ Helper function to run a shell command and return its output. """
    
    return subprocess.run(command, shell=True, text=True, capture_output=True, cwd=directory)
# 
    
def create_directory_with_suffix(base_path):
    """ Create a directory with an incrementing number suffix if it already exists. """
    counter = 1
    new_path = base_path
    while os.path.exists(new_path):
        new_path = f"{base_path}{counter}"
        counter += 1
    os.makedirs(new_path)
    return new_path

def load_parameters(param_file):
    """ Load parameters from a .params file and return them as a dictionary. """
    params = {}
    with open(param_file, 'r') as file:
        for line in file:
            if ":="  in line:
                key, value = line.split(' := ')
            elif "="  in line:
                key, value = line.split('=')
            else:
                continue
            params[key.strip()] = value.strip().strip("'")
    return params

def build_command(params, cmd):
    """ Build the command based on the loaded parameters. """
    cmd = [cmd]
    # Define mappings from parameter names to command line flags
    flag_mappings = {
        'luby': '-luby',
        'rnd-init': '-no-rnd-init',
        'gc-frac': '-gc-frac',
        'rinc': '-rinc',
        'var-decay': '-var-decay',
        'cla-decay': '-cla-decay',
        'rnd-freq': '-rnd-freq',
        'rnd-seed': '-rnd-seed',
        'phase-saving': '-phase-saving',
        'ccmin-mode': '-ccmin-mode',
        'rfirst': '-rfirst',
        'pre': '-pre',
        'verb': '-verb',
        'rcheck': '-no-rcheck',
        'asymm': '-no-asymm',
        'elim': '-elim',
        'simp-gc-frac': '-simp-gc-frac',
        'sub-lim': '-sub-lim',
        'cl-lim': '-cl-lim',
        'grow': '-grow',
        'RESTARTS': 'RESTARTS',
        'LUBYFACTOR': 'LUBYFACTOR',
        'FIXEDPERIOD': 'FIXEDPERIOD',
        'PHASE': 'PHASE',
        'CLADECAY': 'CLADECAY',
        'INITCONFLICTBOUND': 'INITCONFLICTBOUND',
        'VARDECAY': 'VARDECAY',
        'CONFLICTBOUNDINCFACTOR': 'CONFLICTBOUNDINCFACTOR',
        'SIMP': 'SIMP',
        'CLEANING': 'CLEANING',
        'lbd-cut': '-lbd-cut',
        'lbd-cut-max': '-lbd-cut-max',
        'cp-increase ': '-cp-increase',
        'P': '-P',
        'I': '-I',
        'K': '-K',
        'M': '-M',
        'V': '-V',
        'N': '-N',
        'U': '-U',
        'B': '-B',
        'num-decimal-places': '-num-decimal-places',
        'level': 'level',
        'wbits': 'wbits',
        'memLevel': 'memLevel',
        'strategy': 'strategy',
        'search_steps':'-search_steps',
        'restarts':'-restarts',
        'repeats':'-repeats',
        'noise':'-noise',
        'static_noise':'-static_noise',
        'lowmemory':'-lowmemory',
        'method':'--method',
        'jac':'--jac',
        'tol':'--tol',
        'disp':'--disp',
        'maxiter':'--maxiter'

    }

    for key, value in params.items():
        if key in flag_mappings:
            if key in [ 'P', 'I', 'K', 'M', 'V', 'N', 'U', 'B','num-decimal-places','static_noise','lowmemory', 'search_steps', 'restarts', 'repeats', 'noise']:

                if value.lower() == 'true':
                    cmd.append(flag_mappings[key])
                elif value.lower() == 'false':
                    pass
                elif value.lower() == 'none':
                    pass
                else:
                    cmd.append(flag_mappings[key] + ' ' + value)
            elif key in ['method', 'jac', 'tol', 'disp', 'maxiter']:
                if value.lower() == 'none' or value.lower() == None or value.lower() == 'false':
                    pass
                else:
                    cmd.append(flag_mappings[key] + '=' + value)
            else:
                if value.lower() == 'true':
                    cmd.append(flag_mappings[key])
                elif value.lower() == 'false':
                    if "no-" not in flag_mappings[key]:
                        cmd.append('-no-' + flag_mappings[key][1:])
                else:
                    cmd.append(flag_mappings[key] + '=' + value)
    return cmd



def measure_execution(name,directory_path, file_path, run_directory, compile_command, execute_command, test_command, output_json="results.json"):
    #if output json does not exist create it
    if not os.path.exists(output_json):
        with open(output_json, 'w') as f:
            f.write("{}")
    try:
        # Read the JSON content from the file
        with open(output_json, 'r') as vf:
            content = json.load(vf)
    except Exception as e:
        print(f"Failed to read {output_json}: {e}")
        return
    erroneous_files = []
    execute_command_temp=execute_command

    # Ensure the directory exists
    if not os.path.isdir(directory_path):
        print(f"Directory {directory_path} does not exist.")
        return
    if name not in content:
        content[name] = {}
    temp_obj = {}
    for root, _, files in os.walk(directory_path):
        for version_file in files:
            version_file_path = os.path.join(root, version_file)

            # Ensure it's a file
            if not os.path.isfile(version_file_path):
                continue
            print('version file path:', version_file_path)
            
            # Replace the file path content with the current version
            try:
                with open(version_file_path, 'r') as vf, open(file_path, 'w') as target_file:
                    target_file.write(vf.read())
                print(f"Replaced content of {file_path} with {version_file_path}")
            except Exception as e:
                print(f"Failed to replace {file_path} with {version_file_path}: {e}")
                continue
            #get the name of the version file without extensions
            version_file_name = os.path.splitext(version_file)[0]
            # Compile if a compile command is provided
            if compile_command != "":
                try:
                    subprocess.run(compile_command, cwd=run_directory, shell=True, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Compilation failed for {version_file}: {e}")
                    continue
            test_success = True
            if test_command!="":
                if version_file.endswith('.params'):
                    params = load_parameters(version_file_path)
                    print(f"the params are {params}")
                    test_command = build_command(params, test_command)
                    test_command= " ".join(test_command)
                print(f"Executing command: {test_command}")

                # Execute the test command
                try:
                    run_command(test_command, run_directory)
                    test_success = True
                except:
                    test_success = False
                
            if not test_success:
                content[name][version_file] = "Failed compilation"
            else:

                # Execute the command 11 times and measure the average execution time
                total_time = []
                total_failures=[]
                run_times=0
                #if the name of the fiile is a .params file
                if version_file.endswith('.params'):
                    execute_command = execute_command_temp
                    params = load_parameters(version_file_path)
                    print(f"params: {params}")
                    execute_command = build_command(params, execute_command)
                    execute_command= " ".join(execute_command)
                print(f"Executing command: {execute_command}")
                #add to  an object with the file name , the run directory and the command
                temp_obj[version_file_name] = {'run_directory': run_directory, 'command': execute_command}
                for i in range(run_times):
                    try:
                        start_time = time.time()
                        subprocess.run(execute_command, cwd=run_directory, shell=True, check=True, timeout = 40)
                        end_time = time.time()
                        #check that the duration is more than 1 sec
                        if end_time - start_time > 1:
                            print(f"Execution time for {version_file} on run {i + 1} is more than 1 second.")
                            
                            total_time.append(end_time - start_time)
                        else:
                            erroneous_files.append(version_file)
                            
                            
                            
                            total_failures.append("Failed start")
                            
                    except subprocess.TimeoutExpired:
                        print(f"Command timed out after 40 seconds: {execute_command}")
                        erroneous_files.append(version_file)
                        total_failures.append("Failed timeout")
                        
                    except subprocess.CalledProcessError as e:
                        print(f"Execution failed for {version_file} on run {i + 1}: {e}")
                        # content[name][version_file] = "Failed execution"
                        total_failures.append("Failed execution")
                        erroneous_files.append(version_file)
                        
                        
                total_list=total_time+total_failures
                    # Calculate the median execution time
                if len(total_time) == 0:
                    content[name][version_file] = "All Failed"
                    content[name][f'{version_file}_all'] = total_list
                else:
                    median_time = statistics.median(total_time)
                    
                    content[name][version_file] = median_time
                    content[name][f'{version_file}_all'] = total_list

                # Save the content to a JSON file
                try:
                    with open(output_json, 'w') as json_file:
                        json.dump(content, json_file, indent=4)
                    print(f"Results saved to {output_json}")
                except Exception as e:
                    print(f"Failed to save results to {output_json}: {e}")
                # time.sleep(20)
    #save the temp object to a json file but append dont ovewrite
    with open("commands_12.json", 'a') as json_file:
        json.dump(temp_obj, json_file, indent=4)
        print(f"Results saved to commands.json")
    #save the erroneous files to a text file
    try:
        with open('erroneous_files.txt', 'w') as ef:
            for file in erroneous_files:
                ef.write(f"{file}\n")
        print("Erroneous files saved to erroneous_files.txt")
    except Exception as e:
        print(f"Failed to save erroneous files to erroneous_files.txt: {e}")

# Example usage
if __name__ == "__main__":
    # measure_execution(
    #     name="lpg_params",
    #     directory_path="/home/jim/LLm_Software_improvement/Results/lpg_params_07_parsed",
    #     file_path="/home/jim/LLm_Software_improvement/lpg_necessary/lpg.params",
    #     run_directory="/home/jim/LLm_Software_improvement/lpg_necessary/",
    #     compile_command="",  # Adjust to your needs
    #     execute_command="bash run_fixed.sh",
    #     test_command="",
    #     output_json="results.json"
    # )
    # measure_execution(
    #         name="minisat_hack_params_07",
    #         directory_path="/home/jim/LLm_Software_improvement/Results/minisat_hack_params_07_parsed",
    #         file_path="/home/jim/LLm_Software_improvement/minisat_hack_necessary/minisat_advanced.params",
    #         run_directory="/home/jim/LLm_Software_improvement/minisat_hack_necessary",
    #         compile_command="",  # Adjust to your needs
    #         execute_command="bash run_fixed.sh",
    #         test_command="",
    #         output_json="results.json"
    #     )
    # measure_execution(
    #     name="lpg_params_07",
    #     directory_path="/home/jim/LLm_Software_improvement/Results/lpg_params_07_parsed",
    #     file_path="/path/to/target/file",
    #     run_directory="/path/to/run/directory",
    #     compile_command="gcc program.c -o program",  # Adjust to your needs
    #     execute_command="./program",
    #     test_command="python test.py",
    #     output_json="results.json"
    # )
    # measure_execution(
    #         name="lpg_params_07",
    #         directory_path="/home/jim/LLm_Software_improvement/Results/lpg_params_07_parsed",
    #         file_path="/home/jim/LLm_Software_improvement/lpg_necessary/lpg.params",
    #         run_directory="/home/jim/LLm_Software_improvement/lpg_necessary/",
    #         compile_command="",  # Adjust to your needs
    #         execute_command="bash run_fixed.sh",
    #         test_command="",
    #         output_json="results1.json"
    #     )
    

    measure_execution(
            name="lpg_params_12",
            directory_path="/home/jim/LLm_Software_improvement/Results/lpg_params_12_parsed",
            file_path="/home/jim/LLm_Software_improvement/lpg_necessary/lpg.params",
            run_directory="/home/jim/LLm_Software_improvement/lpg_necessary/",
            compile_command="",  # Adjust to your needs
            execute_command="bash run_fixed.sh",
            test_command="",
            output_json="results1.json"
        )
    
    # measure_execution(
    #         name="minisat_hack_params_07",
    #         directory_path="/home/jim/LLm_Software_improvement/Results/minisat_hack_params_07_parsed",
    #         file_path="/home/jim/LLm_Software_improvement/minisat_hack_necessary/minisat_advanced.params",
    #         run_directory="/home/jim/LLm_Software_improvement/minisat_hack_necessary",
    #         compile_command="",  # Adjust to your needs
    #         execute_command="bash run_fixed.sh",
    #         test_command="",
    #         output_json="results1.json"
    #     )
    measure_execution(
            name="minisat_hack_params_12",
            directory_path="/home/jim/LLm_Software_improvement/Results/minisat_hack_params_12_parsed",
            file_path="/home/jim/LLm_Software_improvement/minisat_hack_necessary/minisat_advanced.params",
            run_directory="/home/jim/LLm_Software_improvement/minisat_hack_necessary",
            compile_command="",  # Adjust to your needs
            execute_command="bash run_fixed.sh",
            test_command="",
            output_json="results1.json"
        )
    # measure_execution(
    #         name="minisat_params_07",
    #         directory_path="/home/jim/LLm_Software_improvement/Results/minisat_params_07_parsed",
    #         file_path="/home/jim/LLm_Software_improvement/minisat_necessary/minisat_simplified.params",
    #         run_directory="/home/jim/LLm_Software_improvement/minisat_necessary/",
    #         compile_command="",  # Adjust to your needs
    #         execute_command="bash run_fixed.sh",
    #         test_command="",
    #         output_json="results1.json"
    #     )
    measure_execution(
            name="minisat_params_12",
            directory_path="/home/jim/LLm_Software_improvement/Results/minisat_params_12_parsed",
            file_path="/home/jim/LLm_Software_improvement/minisat_necessary/minisat_simplified.params",
            run_directory="/home/jim/LLm_Software_improvement/minisat_necessary/",
            compile_command="",  # Adjust to your needs
            execute_command="bash run_fixed.sh",
            test_command="",
            output_json="results1.json"
        )
    # measure_execution(
    #         name="sat4j_params_07",
    #         directory_path="/home/jim/LLm_Software_improvement/Results/sat4j_params_07_parsed",
    #         file_path="/home/jim/magpie_llm/examples/sat4j/necessary/test.params",
    #         run_directory="/home/jim/magpie_llm/examples/sat4j/necessary/",
    #         compile_command="",  # Adjust to your needs
    #         execute_command="bash run_fixed.sh",
    #         test_command="",
    #         output_json="results1.json"
    #     )
    measure_execution(
            name="sat4j_params_12",
            directory_path="/home/jim/LLm_Software_improvement/Results/sat4j_params_12_parsed",
            file_path="/home/jim/magpie_llm/examples/sat4j/necessary/test.params",
            run_directory="/home/jim/magpie_llm/examples/sat4j/necessary/",
            compile_command="",  # Adjust to your needs
            execute_command="bash run_fixed.sh",
            test_command="",
            output_json="results1.json"
        )
    # measure_execution(
    #         name="scipy_params_07",
    #         directory_path="/home/jim/LLm_Software_improvement/Results/scipy_params_07_parsed",
    #         file_path="/home/jim/magpie_llm/examples/scipy/necessary/scipy.params",
    #         run_directory="/home/jim/magpie_llm/examples/scipy/necessary/",
    #         compile_command="",  # Adjust to your needs
    #         execute_command="bash run_fixed.sh",
    #         test_command="",
    #         output_json="results1.json"
    #     )
    measure_execution(
            name="scipy_params_12",
            directory_path="/home/jim/LLm_Software_improvement/Results/scipy_params_12_parsed",
            file_path="/home/jim/magpie_llm/examples/scipy/necessary/scipy.params",
            run_directory="/home/jim/magpie_llm/examples/scipy/necessary/",
            compile_command="",  # Adjust to your needs
            execute_command="bash run_fixed.sh",
            test_command="",
            output_json="results1.json"
        )
    # measure_execution(
    #         name="weka_params_07",
    #         directory_path="/home/jim/LLm_Software_improvement/Results/weka_params_07_parsed",
    #         file_path="/home/jim/magpie_llm/examples/weka/necessary/weka.params",
    #         run_directory="/home/jim/magpie_llm/examples/weka/necessary/",
    #         compile_command="",  # Adjust to your needs
    #         execute_command="bash run_fixed.sh",
    #         test_command="",
    #         output_json="results1.json"
    #     )
    measure_execution(
            name="weka_params_12",
            directory_path="/home/jim/LLm_Software_improvement/Results/weka_params_12_parsed",
            file_path="/home/jim/magpie_llm/examples/weka/necessary/weka.params",
            run_directory="/home/jim/magpie_llm/examples/weka/necessary/",
            compile_command="",  # Adjust to your needs
            execute_command="bash run_fixed.sh",
            test_command="",
            output_json="results1.json"
        )

        
    # measure_execution(
    #         name="zlib_params_07",
    #         directory_path="/home/jim/LLm_Software_improvement/Results/zlib_params_07_parsed",
    #         file_path="/home/jim/magpie_llm/examples/zlib/necessary/zlib.params",
    #         run_directory="/home/jim/magpie_llm/examples/zlib/necessary/",
    #         compile_command="",  # Adjust to your needs
    #         execute_command="bash run_fixed.sh",
    #         test_command="",
    #         output_json="results1.json"
    #     )
    measure_execution(
            name="zlib_params_12",
            directory_path="/home/jim/LLm_Software_improvement/Results/zlib_params_12_parsed",
            file_path="/home/jim/magpie_llm/examples/zlib/necessary/zlib.params",
            run_directory="/home/jim/magpie_llm/examples/zlib/necessary/",
            compile_command="",  # Adjust to your needs
            execute_command="bash run_fixed.sh",
            test_command="",
            output_json="results1.json"
        )