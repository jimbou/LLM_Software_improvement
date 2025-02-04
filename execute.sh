#!/bin/bash

INPUT_FILE="$1"
OUTPUT_FILE="$2"

# Ensure jq is installed
if ! command -v jq &> /dev/null; then
    echo "[ERROR] jq is required but not installed. Install it and rerun the script."
    exit 1
fi

echo "[INFO] Processing input file: $INPUT_FILE"
echo "[INFO] Results will be saved in: $OUTPUT_FILE"

# Create a temporary file to store results
TEMP_FILE=$(mktemp)

# Initialize empty JSON object
echo "{}" > "$TEMP_FILE"

# Read each entry from the JSON file
jq -c 'to_entries[]' "$INPUT_FILE" | while read -r entry; do
    key=$(echo "$entry" | jq -r '.key')
    dir=$(echo "$entry" | jq -r '.value.run_directory')
    cmd=$(echo "$entry" | jq -r '.value.command')

    echo "[INFO] Processing: $key"
    echo "[DEBUG] Run directory: $dir"
    echo "[DEBUG] Command: $cmd"

    # Move to the specified directory
    cd "$dir" || {
        echo "[ERROR] Directory not found: $dir"
        jq --arg key "$key" --arg fail "does not run" '. + {($key): {time: $fail}}' "$TEMP_FILE" > "$TEMP_FILE.tmp" && mv "$TEMP_FILE.tmp" "$TEMP_FILE"
        continue
    }

    echo "[INFO] Executing command: $cmd"
    



    # Start execution with timeout monitoring
    start_time=$(date +%s%N)
    eval "$cmd" >/dev/null 2>&1 &
    pid=$!

    max_duration=30  # Maximum allowed execution time in seconds
    elapsed=0

    while kill -0 $pid 2>/dev/null; do
        sleep 1
        elapsed=$((elapsed + 1))

        if [ "$elapsed" -ge "$max_duration" ]; then
            echo "[WARN] Command exceeded time limit ($max_duration sec). Killing process."
            kill -9 $pid 2>/dev/null
            jq --arg key "$key" --arg fail "timeout" '. + {($key): {time: $fail}}' "$TEMP_FILE" > "$TEMP_FILE.tmp" && mv "$TEMP_FILE.tmp" "$TEMP_FILE"
            continue 2  # Skip to the next JSON entry
        fi
    done

    end_time=$(date +%s%N)
    duration=$(( (end_time - start_time) / 1000000 )) # Convert to milliseconds

    if [ "$duration" -lt 1000 ]; then
        echo "[WARN] Command failed to execute properly (exited too soon)"
        jq --arg key "$key" --arg fail "does not run" '. + {($key): {time: $fail}}' "$TEMP_FILE" > "$TEMP_FILE.tmp" && mv "$TEMP_FILE.tmp" "$TEMP_FILE"
        continue
    fi

    echo "[INFO] Command executed successfully. Running 11 times for median calculation."

    # If the command runs correctly, execute it 11 times and measure median time


    # If the command runs correctly, execute it 11 times and measure median time
    times=()
    for i in {1..11}; do
        echo "[DEBUG] Running iteration $i..."
        start_time=$(date +%s%N)
        eval "$cmd" >/dev/null 2>&1
        end_time=$(date +%s%N)
        duration=$(( (end_time - start_time) / 1000000 )) # Convert to milliseconds
        echo "[DEBUG] Iteration $i execution time: $duration ms"
        times+=("$duration")
    done

    # Sort times and find the median
    sorted_times=($(printf "%s\n" "${times[@]}" | sort -n))
    median_index=$(( ${#sorted_times[@]} / 2 ))
    median_time="${sorted_times[$median_index]}"

    echo "[INFO] Median execution time for $key: $median_time ms"

    # Store the result in the JSON output
    jq --arg key "$key" --argjson time "$median_time" '. + {($key): {time: $time}}' "$TEMP_FILE" > "$TEMP_FILE.tmp" && mv "$TEMP_FILE.tmp" "$TEMP_FILE"
    sleep 15
done

# Save results to the output JSON file
mv "$TEMP_FILE" "$OUTPUT_FILE"

echo "[INFO] Results saved to $OUTPUT_FILE"
