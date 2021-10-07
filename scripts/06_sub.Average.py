#### 

group_data = snakemake.input.Sample_group_data
path1 = snakemake.input.Exp_data
skip = []# snakemake.params.skip

sample_group = dict()

with open(group_data) as f:
    for line in f.readlines():
        temp = line.strip().split('\t')

        sample = temp[1].strip()
        group = temp[3].strip()
        
        if sample in skip:
            continue

        sample_group[sample] = group
        
out_path = snakemake.output[0]

fw = open(out_path, "w")

with open(path1) as f:
    HEADER = f.readline().strip().split("\t")
    new_HEADER = ["GeneID"]
        
    data_dict = dict()
    
    for head in HEADER[1:]:
        if head in skip: 
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
            if index in skip: 
                continue

            if sample_group[index] not in data_dict:
                data_dict[sample_group[index]] = list()

            data_dict[sample_group[index]].append(float(val))
     
        for new_head in new_HEADER[1:]:
            new_line.append("{:.6f}".format(sum(data_dict[new_head])/len(data_dict[new_head])))
            
        fw.write("\t".join(new_line) + "\n")
            
fw.close()
    
