import os
import subprocess

# Function to perform bedtools intersect
def perform_bedtools_intersect(motif_file, input_file, output_file):
    cmd = [
        "bedtools",
        "intersect",
        "-a", motif_file,
        "-b", input_file,
        "-wo"
    ]
    with open(output_file, "w") as output:
        process = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
        
        # Define the header
        header = "#chrom\tchromStart\tchromEnd\tmotif_id\tscore\tstrand\tbinding_sequence\tpeak_region"
        
        # Write the header to the output file
        output.write(header + '\n')
        
        for line in process.stdout.split('\n'):
            if line:
                # Split the line into columns
                columns = line.split('\t')
                
                # Format columns 9, 10, and 11 as "chr1:10006-10614"
                coordinates = f"{columns[8]}:{columns[9]}-{columns[10]}"
                
                # Concatenate columns starting from the 14th column using ';'
                concatenated_columns = ";".join([coordinates] + columns[11:])
                
                # Replace the columns in the output line
                modified_line = "\t".join(columns[0:6] + [columns[7]] + [concatenated_columns])
                
                # Write the modified line to the output file
                output.write(modified_line + '\n')

    print(f"Intersection complete for {input_file}. Results saved to {output_file}.gz")

    # Sort the output file
    sort_command = f"LC_ALL=C sort -k1,1 -k2,2n -k3,3n {output_file} -o {output_file}"
    subprocess.run(sort_command, shell=True)

    # Bgzip the sorted output file
    bgzip_cmd = ["bgzip", output_file]
    subprocess.run(bgzip_cmd)


# Define the paths to the motif file and the directory containing Accessible chromatin files
motif_file = "motif/factorbookMotifPosWithSequence.bed"
peak_dir = "peaks/ByCellType/TF"
output_dir = "mapping"  # New directory for output files

# Create the "mapping" directory if it doesn't exist
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# List all the Accessible chromatin files in the directory
peak_files = [f for f in os.listdir(peak_dir) if f.endswith(".bed.gz")]

# Loop through the chromatin files and perform bedtools intersect
for peak_file in peak_files:
    input_file = os.path.join(peak_dir, peak_file)

    # Extract the sample ID from the input file name (Sample_XXXX)
    filename = "_".join(peak_file.split(".")[:3])

    # Construct the output file name
    output_file = os.path.join(output_dir, f"{filename}.withMotif.bed")

    # Perform bedtools intersect
    perform_bedtools_intersect(motif_file, input_file, output_file)
