import sys

path = sys.argv[1]

with open(path) as f:
    f.readline()
    for line in f.read().strip().split("\n"):
        data = line.strip().split("\t")
        
        print('\t'.join([data[0], data[6], data[7], data[8], data[9], data[10]]))
