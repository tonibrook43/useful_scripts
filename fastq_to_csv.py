#!/usr/bin/env python

from Bio import SeqIO
import csv
import argparse

#########
# args #
#########

def get_args():
    parser = argparse.ArgumentParser(description="A program to convert a FASTQ file format into a .csv file format")
    parser.add_argument("-f", "--file", help="designates absolute file path to the fastq file", required=True)
    parser.add_argument("-o", "--outfile", help="designates absolute file path to the output csv file", required=False)    
    return parser.parse_args()

args = get_args()

# Input and output file paths
fastq_file = args.file
csv_file = args.outfile

# ./fastq_to_csv.py -f bacteria_reads_test.R1.fq -o test_fq_to_csv.csv


# Open the FASTQ file for reading and the CSV file for writing
with open(fastq_file, "r") as fastq_fh, open(csv_file, "w", newline="") as csv_fh:
    # Create a CSV writer
    csv_writer = csv.writer(csv_fh)

    # Write the CSV header
    #csv_writer.writerow(["Sequence ID", "Label", "Sequence", "Quality Scores", "Sequence Length"])

    # Parse the FASTQ file and write the data to the CSV file
    for record in SeqIO.parse(fastq_fh, "fastq"):
        sequence_id = record.id
        sequence = str(record.seq)
        quality_scores = record.letter_annotations["phred_quality"]
        sequence_length = len(sequence)


        # Write a row to the CSV file for each sequence
        csv_writer.writerow([sequence_id, "test", sequence])

print(f"Conversion from {fastq_file} to {csv_file} complete.")
