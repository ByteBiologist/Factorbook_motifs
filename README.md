# Factorbook UCSC

Transcription Factor ChIP-seq Clusters (161 factors) from ENCODE with Factorbook Motifs.

This repository contains scripts to process TF data from UCSC https://genome.ucsc.edu/cgi-bin/hgTrackUi?hgsid=2057466232_cZzcnxdDVYXVhETfI6CnhaQ9isID&c=chr1&g=wgEncodeRegTfbsClusteredV3

## Installation
1. Clone this repository:
    ```bash
    git clone git@github.com:ByteBiologist/Factorbook_v1_UCSC.git
    cd factorbook_v1_UCSC
    ```
2. Dependencies:
   * bedtools
   * samtools
   * hg19 reference genome "hg19.fa"


##Usage:

#### Step 1) ChIP-seq peaks
Download and process peak dataset. The output is processed peak data split by cell type.
  * **bash tf_peak_processing.sh**

#### Step 1a) Split peak data further by Transcription factors
Provide output directory as an argument.
  * **python splitBed_TF.py ByCellType**

#### Step 2) Factorbook motifs
Download, normalize and process Factorbook motifs.
  * **python motif_processing.py**

#### Step 3) pfm 
Downlad position frequency matrix for motis and write individual pfm files.
  * **bash pwm_processing.sh**

#### Step 4) overlap motifs with peak
Perform bedtools intersect to find the overlapping regions with motifs.
  * **python overlap.py**
