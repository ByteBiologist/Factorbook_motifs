# Factorbook UCSC

Transcription Factor ChIP-seq Clusters (161 factors) from ENCODE with Factorbook Motifs
This repository contains scripts to process TF data from UCSC https://genome.ucsc.edu/cgi-bin/hgTrackUi?hgsid=2057466232_cZzcnxdDVYXVhETfI6CnhaQ9isID&c=chr1&g=wgEncodeRegTfbsClusteredV3

Usage:

Step 1) ChIP-seq peaks - to download, and process peak dataset. The output is processed peak data split by cell type
  * **bash tf_peak_processing.sh**
Step 1a) Split cell type split peak data further by Transcription factors, provide output directory as an argument
  * **python splitBed_TF.py ByCellType**
Step 2) Factorbook motifs - to download, normalize and process motifs. Adds the binding sequence and calcualtes qvalue
  * **python motif_processing.py**
Step 3) pfm - to downlad position frequency matrix for motis and write an individual pfm files
  * **bash pwm_processing.sh**
Step 4) overlap motifs with peak - do bedtools intersect to find the overlapping regions with motifs
  * **python overlap.py**
