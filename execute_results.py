import os
import subprocess
import time
import json
from pathlib import Path

def measure_execution(directory_path, file_path, run_directory, compile_command, execute_command, output_json="results.json"):
    results = {}

    # Ensure the directory exists
    if not os.path.isdir(directory_path):
        print(f"Directory {directory_path} does not exist.")
        return

    # Iterate over each file in the directory
    for version_file in os.listdir(directory_path):
        version_file_path = os.path.join(directory_path, version_file)

        if not os.path.isfile(version_file_path):
            continue

        # Replace the file path content with the current version
        try:
            with open(version_file_path, 'r') as vf, open(file_path, 'w') as target_file:
                target_file.write(vf.read())
        except Exception as e:
            print(f"Failed to replace {file_path} with {version_file_path}: {e}")
            continue

        # Compile if a compile command is provided
        if compile_command:
            try:
                subprocess.run(compile_command, cwd=run_directory, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Compilation failed for {version_file}: {e}")
                continue

        # Execute the command 11 times and measure the average execution time
        total_time = 0
        run_times=11
        for i in range(run_times):
            try:
                start_time = time.time()
                subprocess.run(execute_command, cwd=run_directory, shell=True, check=True)
                end_time = time.time()
                total_time += (end_time - start_time)
            except subprocess.CalledProcessError as e:
                print(f"Execution failed for {version_file} on run {i + 1}: {e}")
                break
        else:
            # Calculate the average execution time
            average_time = total_time / run_times
            results[version_file] = average_time

    # Save the results to a JSON file
    try:
        with open(output_json, 'w') as json_file:
            json.dump(results, json_file, indent=4)
        print(f"Results saved to {output_json}")
    except Exception as e:
        print(f"Failed to save results to {output_json}: {e}")

# Example usage
if __name__ == "__main__":
    measure_execution(
        directory_path="/path/to/version/files",
        file_path="/path/to/target/file",
        run_directory="/path/to/run/directory",
        compile_command="gcc program.c -o program",  # Adjust to your needs
        execute_command="./program",
        output_json="results.json"
    )
