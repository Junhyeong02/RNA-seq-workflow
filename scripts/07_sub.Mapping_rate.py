import sys

path = sys.argv[1]
out = sys.argv[2]

fw = open(out, "w")

with open(path) as f:
    for line in f.readlines():
        sample, rate = line.strip().split(':')

        name, sample = sample.replace("../04.Mapping/", "").split("/")
        name, Type = name.split(".")
        sample = sample.strip(".log")

        rate = rate.split()[0].strip("%")

        fw.write('\t'.join([name, Type, sample, rate])+ "\n")

fw.close()
