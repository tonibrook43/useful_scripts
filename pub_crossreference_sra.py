#!/usr/bin/env python

import time
from Bio import Entrez
import csv
import logging

logger = logging.basicConfig(filename="crossreference_sra.log", format='%(asctime)s - %(message)s', level=logging.INFO)

# Global Variables
BATCH_SIZE = 100  #number of sequences to download per batch
SLEEP_INTERVAL = 10  #time in seconds to sleep between batches

#Function to read the file containing the list of titles
def read_titles_file(file_path):
    with open(file_path, 'r') as file:
        titles = file.read()
    return titles

logging.info("starting csv file read")

#function to read the CSV file containing the list of publications
def read_titles_csv(file_path):
    titles = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        next(reader) #this will skip the first line of the csv file
        for row in reader:
            titles.append(row['Title'])
    return titles

logging.info("starting SRA cross reference")

#function to cross-reference the publication titles with the SRA database
def cross_reference_with_sra(titles):
    with open("SRA_matches.txt", "w") as output_file:
        for i in range(0, len(titles), BATCH_SIZE):
            batch = titles[i:i + BATCH_SIZE]
            for title in batch:
                output_file.write(f"Checking SRA entries for the publication: {title}\n")
                handle = Entrez.esearch(db="sra", term=title)
                record = Entrez.read(handle)
                handle.close()
                if record["IdList"]:
                    output_file.write(f"Found SRA entries for the publication: {', '.join(record['IdList'])}\n")
                else:
                    output_file.write("No SRA entries found for this publication.\n")
            time.sleep(SLEEP_INTERVAL)

logging.info("finished SRA cross reference")

file_path = 'path to your csv file'
publication_titles = read_titles_csv(file_path)


#Cross-reference with the SRA database
Entrez.email = "email" 
cross_reference_with_sra(publication_titles)
