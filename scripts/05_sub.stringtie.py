import sys
import os
import subprocess
from glob import glob

GTF_FILE = sys.argv[1]
PATH = sys.argv[2]
CPU = sys.argv[3]
Prefix = sys.argv[4]

print(GTF_FILE, PATH)

Input_list = glob(PATH+"*.bam")
Ref = GTF_FILE.split("/")[-1]
print(Input_list)

for bam in Input_list:
    print(bam)
    OUT_FILE = bam.replace("bam", Ref)
    
    # print("stringtie -p {} -e -G {} -o {} -l {} {}".format(CPU, GTF_FILE, OUT_FILE, Prefix, bam))
    # os.system("stringtie -p {} -e -G {} -o {} -l {} {}".format(CPU, GTF_FILE, OUT_FILE, Prefix, bam))
    p = subprocess.Popen(["stringtie", "-p", CPU, "-e", "-G",  GTF_FILE, "-o", OUT_FILE, "-l", Prefix, bam])
    print(OUT_FILE)
    p.wait()
