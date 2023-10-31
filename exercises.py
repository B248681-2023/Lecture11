#!/usr/bin/python3

import os
import sys
import subprocess
import shutil
import re

try:
    sys.argv[1]
except NameError:
    print("Must provide accession number as first variable")
    exit
else:
    accession = sys.argv[1]

shutil.copy("/localdisk/data/BPSM/Lecture11/plain_genomic_seq.txt","plain_genomic_seq.txt")
with open("plain_genomic_seq.txt") as sequence_file:
    sequence_contents = sequence_file.read()
    exon_1 = sequence_contents[0:63]
    exon_2 = sequence_contents[90:]

sequence_combined=exon_1 + exon_2
with open("sequence_combined.txt", "w") as combined_file:
    combined_file.write(sequence_combined)



subprocess.run(["wget", "-O", f"{accession}.gb", f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={accession}&rettype=gb&retmode=text"])

with open(f"{accession}.gb") as fetched_sequence:
    sequence_info_array = fetched_sequence.readlines()
    sequence_is_now =  "no"
    sequence = ""
    for sequence_info in sequence_info_array:
        if re.search(".*CDS.*", sequence_info):
            CDS_start = int(sequence_info.split()[1].split('.')[0])-1
            CDS_end = int(sequence_info.split()[1].split('.')[2])-1
        elif (sequence_is_now == "yes"):
            sequence = sequence + re.sub(r'[0-9\s\/\/]', "" , sequence_info)
        elif (sequence_is_now == "no" and re.search("^ORIGIN", sequence_info)):
            sequence_is_now = "yes"
coding_region = sequence[CDS_start:CDS_end]
print("Coding region is " + coding_region)
with open(f"{accession}_coding_region.txt", "w") as fileyy:
    fileyy.write(coding_region)
 

sequence_1_result = subprocess.run(["blastx", "-db", "/home/s2611220/Exercises/Lecture06/nem", "-query", f"{accession}_coding_region.txt", "-outfmt", "7", "-out", f"{accession}_new_blast.out"], capture_output=True, text=True)


if sequence_1_result.returncode != 0:
    print(f"Error running blastx: {sequence_1_result.stderr}")
else:
    print("blastx completed successfully!")

sequence_combined_result = subprocess.run(["blastx", "-db", "/home/s2611220/Exercises/Lecture06/nem", "-query", "sequence_combined.txt", "-outfmt", "7", "-out", "combined_sequence_blast_result"], capture_output=True, text=True)

if sequence_combined_result.returncode != 0:
    print(f"Error running blastx: {sequence_combined_result.stderr}")
else:
    print("blastx completed successfully")
