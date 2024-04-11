import os
import urllib.request
import gzip
import subprocess

# Folders
motif_file = "motif"
peaks_folder = "peaks/ByCellType/TF/test"

# Check if file exists
def file_exists(file_path):
    return os.path.isfile(file_path)

# File download
def download_file(url, folder):
    filename = os.path.basename(url)
    file_path = os.path.join(folder, filename)

    if file_exists(file_path):
        print(f"File {filename} already exists in {folder}. Skipping download.")
    else:
        try:
            urllib.request.urlretrieve(url, file_path)
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            exit(1)

# Process motif file
def process_motiffile(input_file, output_file):
    with gzip.open(input_file, 'rt') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            fields = line.strip().split()
#            f_out.write('\t'.join(fields[1:8] + [fields[0]]) + '\n')
            f_out.write('\t'.join(fields[1:] ) + '\n')

    print(f"Motif positions are written to {output_file}")

# Get reference sequence
def get_reference(sequenceID):
    fa = "hg19.fa"
    output = subprocess.check_output(["samtools", "faidx", fa, sequenceID]).decode("utf-8")
    lines = output.split('\n')
    ref_sequence = ''.join(lines[1:])
    return ref_sequence.upper()

# Get reverse complement sequence
def get_reverse_complement(sequence):
    complement = {'a': 't', 'c': 'g', 'g': 'c', 't': 'a'}
    reverse_complement = ''
    sequence = sequence.lower()
    for base in reversed(sequence):
        if base in complement:
            reverse_complement += complement[base]
        else:
            reverse_complement += base
    return reverse_complement.upper()


# Process bed file
def add_reference(input_file, output_file):
    # Motifs lacking pfm
    motifs = {"UA14", "UAK18", "UAK19", "UAK20"}

    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:

        # Define the header
        header = "#chrom\tchromStart\tchromEnd\tname\tscore\tstrand\tbinding_sequence"

        # Write the header to the output file
        f_out.write(header + '\n')

        for line in f_in:
            fields = line.strip().split('\t')
            chromosome = fields[0]
            start = fields[1]
            end = fields[2]
            name = fields[3]
            score = float(fields[4])  
            strand = fields[5]
            start_position = int(start) + 1 # to convert from 0 to 1-based coordinates for samtools
            sequenceID = f"{chromosome}:{start_position}-{end}"
            #sequenceID = f"{chromosome}:{start}-{end}"

            if name in motifs:
                # Skip line if name matches
                continue
            
            if strand == '+':
                hg19_sequence = get_reference(sequenceID)
            elif strand == '-':
                ref_sequence = get_reference(sequenceID)
                hg19_sequence = get_reverse_complement(ref_sequence)
            else:
                print("Invalid strand information.")
                continue
            
            # Append the hg19_sequence to the fields
            fields.append(hg19_sequence)
            
            # Filter the motifs with score less than -log(0.2)
            if score >= 0.69:
                f_out.write('\t'.join(fields) + '\n')

    print(f"Processed data written to {output_file}")

    bgzip_cmd = f"bgzip -f {output_file}"
    subprocess.run(bgzip_cmd, shell=True)

    print(f"Compressed data written to {output_file}.gz")

# Create directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Define an array of folder names
folders = [motif_file]

# Loop through each folder name
for folder in folders:
    # Check if the directory exists
    create_directory(folder)

# Download experiment table 
download_file("http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/factorbookMotifPos.txt.gz", motif_file)

# Process the downloaded file
input_file_path = os.path.join(motif_file, "factorbookMotifPos.txt.gz")
output_file_path = os.path.join(motif_file, "factorbookMotifPos.bed")
process_motiffile(input_file_path, output_file_path)

# Add reference and filter motifs
output_path = os.path.join(motif_file, "factorbookMotifPosWithSequence.bed" )
add_reference(output_file_path, output_path)