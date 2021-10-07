import sys
import json
import os
from glob import glob

path = sys.argv[1]
path2 = sys.argv[2]

# assert os.path.exists(path)

files = sorted(glob(path) + glob(path2))
# print(files)

print("name\tType\tsample\tRead_type\tRead_length\t#Raw_reads\t#Filtered_reads")

for file_path in files:
    # print(file_path)    
    temp = file_path.replace("NoUse/", "").split("/")

    sample = temp[-1].split("_")[0].replace(".filter", "").strip(".json")
    name, Type = temp[-2].strip().split(".")
    Read_type = temp[-3]

    with open(file_path) as f:
        try:
             json_object = json.load(f)
        except ValueError:
             print(file_path)

        Raw_reads = str(json_object["summary"]["before_filtering"]["total_reads"])
        Read_length = str(json_object["summary"]["before_filtering"]["read1_mean_length"])
        
        if Read_type == "PE":        
            assert Read_length == str(json_object["summary"]["before_filtering"]["read2_mean_length"])

        Filtered_read = str(json_object["summary"]["after_filtering"]["total_reads"])

        print('\t'.join([name, Type, sample, Read_type, Read_length, Raw_reads, Filtered_read]))   
