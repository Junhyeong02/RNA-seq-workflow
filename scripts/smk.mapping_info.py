import sys
import os
from glob import glob

fw = open(snakemake.output.out, "w")

fw.write("Sample\tNumber of mapped read\tAlignment rate\n")

for log in snakemake.input:
    with open(log) as f:
        lines = f.readlines()
        read_type = "Single" if "unpaired" in lines[1] else "Paired"
        alignment_rate = lines[-1].split()[0].strip("%")
        lines = list(map(lambda x: x.strip().split()[0], lines[:-1]))
        
        sample = log.split("/")[-1].strip(".log")
        
        if read_type == "Paired":
            read_number = int(lines[3]) + int(lines[4]) + int(lines[7]) + (int(lines[12]) + int(lines[13]))//2

        elif read_type == "Single":
            read_number = int(lines[3]) + int(lines[4])

        fw.write('\t'.join([sample, str(read_number), alignment_rate]) + "\n")
