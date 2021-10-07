import sys
import os
from glob import glob
import numpy as np
import pandas as pd

group_data = sys.argv[1]
path1 = sys.argv[2]
path2 = sys.argv[3]

print(group_data)
print(path1)

data_list = [path1, path2]# glob(path1) + glob(path2)

print(data_list)
sample_group = dict()

df = pd.read_csv(group_data, sep = "\t", index_col = 'sample')

with open(group_data) as f:
    f.readline()
    for line in f.readlines():
        temp = line.strip().split('\t')

        sample = temp[1].strip()
        group = temp[3].strip()
        
        if sample == "Leaf1":
            continue

        sample_group[sample] = group
        


for file_path in data_list:
    out_path = file_path.replace(".txt", ".avg.txt")

    print(out_path)
    
    fw = open(out_path, "w")

    with open(file_path) as f:
        HEADER = f.readline().strip().split("\t")
        new_HEADER = ["GeneID"]
        
        data_dict = dict()
    
        for head in HEADER[1:]:
            if head == "Leaf1": ###############################CM334.tissue 
                continue

            if sample_group[head] not in new_HEADER:
                new_HEADER.append(sample_group[head])

            data_dict[sample_group[head]] = list()

        fw.write('\t'.join(new_HEADER) + "\n")
        
        
        for line in f.readlines():
            data_dict = dict()
            line = line.strip().split('\t')
            
            new_line = [line[0]]

            for val, index in zip(line[1:], HEADER[1:]):
                if index == "Leaf1": #################### CM334.tissue
                    continue

                if sample_group[index] not in data_dict:
                    data_dict[sample_group[index]] = list()

                data_dict[sample_group[index]].append(float(val))
                # print(val)

            for new_head in new_HEADER[1:]:
                # print(data_dict[new_head])
                new_line.append("{:.6f}".format(sum(data_dict[new_head])/len(data_dict[new_head])))
            
            # print(line[0])
            
            fw.write("\t".join(new_line) + "\n")
            
    fw.close()
    
