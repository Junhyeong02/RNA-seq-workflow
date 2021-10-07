import sys
import os
from glob import glob

path_index = sys.argv[1]
path_input = sys.argv[2]
path_output = sys.argv[3]
CPU = sys.argv[4]
PairType = sys.argv[5]
"""
if not os.path.exists(path_index):
    print("{} path not exists".format(path_index))
    exit()
"""
if not os.path.exists(path_input):
    print("{} path not exists".format(path_input))
    exit()

if not os.path.exists(path_output):
    print("{} path not exists".format(path_output))
    exit()

if PairType not in ("PE", "SE"):
    print("PairType option must be 'PE' or 'SE'")
    exit()

input_file_list = sorted(glob("{}*.filter.fq.gz".format(path_input)))
print(input_file_list)

for i, input_file in enumerate(input_file_list):
    out_file_name = input_file.replace(path_input, "").replace(".filter.fq.gz", "").split("_")[0]
    out_file_name = "{}{}".format(path_output, out_file_name)

    if PairType == "SE":
        # print("hisat2 -p {} --dta -x {} --rna-strandness R --summary-file {}.log -U {} -S {}.sam".format(CPU,\
        #       path_index, out_file_name, input_file, out_file_name))
        
        
        os.system("hisat2 -p {} --dta -x {} --rna-strandness R --summary-file {}.log -U {} -S {}.sam".format(CPU,\
                   path_index, out_file_name, input_file, out_file_name))
        
    elif PairType == "PE":
        if i % 2 == 0:
            try:
                input_file1 = input_file
                input_file2 = input_file_list[i+1]
            except IndexError:
                print("No paired file exists")
                break
            
            # print("hisat2 -p {} --dta -x {} --rna-strandness RF --summary-file {}.log -1 {} -2 {} -S {}.sam".\
            #               format(CPU, path_index, out_file_name, input_file1, input_file2, out_file_name))
            os.system("hisat2 -p {} --dta -x {} --rna-strandness RF --summary-file {}.log -1 {} -2 {} -S {}.sam".\
                          format(CPU, path_index, out_file_name, input_file1, input_file2, out_file_name))

    # print("samtools sort -@ {} -o {}.bam {}.sam".format(CPU, out_file_name, out_file_name))
    # print("rm -rf {}.sam".format(out_file_name))
    os.system("samtools sort -@ {} -o {}.bam {}.sam".format(CPU, out_file_name, out_file_name))
    os.system("rm -rf {}.sam".format(out_file_name))
