import sys
import os
from glob import glob

path = sys.argv[1]
# print(path)
# :assert os.path.exists(path)

files = sorted(glob(path))
print("name\tType\tsample\tREAD_NUM\tAlign_rate")

for file_path in files:
    read_number = 0

    with open(file_path) as f:
        lines = f.readlines()
        read_type = "SE" if "unpaired" in lines[1] else "PE"
        alignment_rate = lines[-1].split()[0].strip("%")
        lines = list(map(lambda x: x.strip().split()[0], lines[:-1]))
        
        name, sample = file_path.replace("../04.Mapping/", "").split("/")
        name, Type = name.split(".")
        sample = sample.strip(".log")
        
        if read_type == "PE":
            read_number = int(lines[3]) + int(lines[4]) + int(lines[7]) + (int(lines[12]) + int(lines[13]))//2

        elif read_type == "SE":
            read_number = int(lines[3]) + int(lines[4])
        print('\t'.join([name, Type, sample, str(read_number), alignment_rate]))
