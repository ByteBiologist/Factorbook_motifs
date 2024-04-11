# Function to check if a file exists
file_exists() {
    [[ -f "$1" ]]
}

# Function to download file
download_file() {
    local url=$1
    local filename=$(basename "$url")

    if file_exists "$filename"; then
        echo "File $filename already exists. Skipping download."
    else
        wget "$url" || { echo "Error downloading $url"; exit 1; }
    fi

    # Decompress the downloaded file
    if [[ "$filename" == *.gz ]]; then
        gunzip -f "$filename"
        filename="${filename%.gz}"
    fi

    # Move the downloaded file to the pwm folder
    mv "$filename" "pwm/$filename"
}

# Define an array of folder names
folders=("pwm")

# Loop through each folder name
for folder in "${folders[@]}"; do
    # Check if the directory exists
    if [ ! -d "$folder" ]; then
        # Create the directory if it doesn't exist  
        mkdir "$folder"
    fi
done

# Function to process the file
process_pwm() {
    local input_file=$1
    local output_dir=$2

    # Check if output directory exists
    if [ ! -d "$output_dir" ]; then
        mkdir -p "$output_dir"
    fi

    # Iterate through each line in the input file
    while IFS=$'\t' read -r motif length pwm; do
        # Create output file name
        output_file="$output_dir/$motif.pwm"
        
        # Write motif and length to the output file
        echo -e ">$motif\t$length" > "$output_file"
        
        # Split the pwm by tabs, replace commas with spaces, and write each element to a new line in the output file
        IFS=$'\t' read -ra pwm_array <<< "$pwm"
        for rows in "${pwm_array[@]}"; do
            # Replace commas with spaces in each rows
            #formatted_rows=$(printf "%.2f" $(echo "$rows" | tr ',' ' '))
            formatted_rows=$(echo "$rows" | tr ',' ' ')
            echo "$formatted_rows" >> "$output_file"
        done
    done < "$input_file"
    
}

# Download PWM file
download_file "https://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/factorbookMotifPwm.txt.gz"

# Process PWM file
process_pwm "pwm/factorbookMotifPwm.txt" "pwm"

