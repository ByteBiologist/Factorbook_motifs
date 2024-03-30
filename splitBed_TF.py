# Split cell type sepcific bed files by Transcription Factors
#Usage: python splitBed_TF.py ByCellType/

import os
import argparse
import subprocess
import gzip

def split_bed_file(input_bed_file, output_folder):
    # Decompress the input BED file
    with gzip.open(input_bed_file, 'rt') as f:
        lines = f.readlines()

    # Extract header and unique TF names from column 7
    header = lines[0]
    tf_names = set(line.split()[3] for line in lines[1:])  # Skip header

    # Create a dictionary to store lines for each TF
    tf_lines = {tf: [] for tf in tf_names}

    # Group lines by TF
    for line in lines[1:]:  # Skip header
        tf = line.split()[3]
        tf_lines[tf].append(line)

    # Write lines to separate files for each TF
    for tf, lines in tf_lines.items():
        output_file = os.path.join(output_folder, f"{tf}_{os.path.basename(input_bed_file)[:-7]}.bed")
        with open(output_file, 'w') as f:
            f.write(header)  # Write header
            for line in lines:
                f.write(line)

        # Compress the output .bed file using bgzip
        subprocess.run(["bgzip", output_file])

def process_bed_files_in_folder(folder_path):
    output_folder = os.path.join(folder_path, "TF")
    os.makedirs(output_folder, exist_ok=True)
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".bed.gz"):
            input_bed_file = os.path.join(folder_path, file_name)
            split_bed_file(input_bed_file, output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split BED files by TF and create output files.")
    parser.add_argument("folder_path", help="Path to the folder containing BED files")
    args = parser.parse_args()

    process_bed_files_in_folder(args.folder_path)

