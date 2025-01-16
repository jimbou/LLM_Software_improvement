import os

def create_results_directory():
    # Define the base structure
    base_dir = "results"
    subdirs_temp = ["temp07", "temp12"]
    high_level_dirs = [
        ("minisat_params", ".params"),
        ("sat4j_params", ".params"),
        ("weka_params", ".params"),
        ("lpg_params", ".params"),
        ("minisat_source", ".cc"),
        ("sat4j_source", ".java"),
        ("weka_source", ".java"),
        ("minisat_hack_params", ".params"),
        ("scipy_params", ".params"),
        ("zlib_params", ".params"),
        ("minisat_hack_source", ".cc")
    ]
    final_subdirs = [
        "simple", "with_cot", "with_hints", 
        "simple_with_doc", "with_cot_and_doc", "with_hints_and_doc"
    ]

    # Create base directory
    os.makedirs(base_dir, exist_ok=True)

    for temp_dir in subdirs_temp:
        temp_path = os.path.join(base_dir, temp_dir)
        os.makedirs(temp_path, exist_ok=True)

        for dir_name, file_extension in high_level_dirs:
            high_level_path = os.path.join(temp_path, dir_name)
            os.makedirs(high_level_path, exist_ok=True)

            for final_subdir in final_subdirs:
                final_subdir_path = os.path.join(high_level_path, final_subdir)
                os.makedirs(final_subdir_path, exist_ok=True)

                # Create 5 files in each final subdir
                for i in range(1, 6):
                    file_name = f"{dir_name}_{temp_dir}_{final_subdir}_{i}{file_extension}"
                    file_path = os.path.join(final_subdir_path, file_name)
                    with open(file_path, "w") as f:
                        f.write(f"Content of {file_name}\n")

if __name__ == "__main__":
    create_results_directory()
