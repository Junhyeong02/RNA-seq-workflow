import json

fw = open(snakemake.output.out, "w")

fw.write("Sample\tMean length of reads\tNumber of raw reads\tNumber of filtered reads\n")

for log in snakemake.input:
    sample = log.split("/")[-1].replace(".filter.json", "")
    Read_type = snakemake.params.read_type

    with open(log) as f:
        try:
             json_object = json.load(f)
        except ValueError:
             print(log)
             continue

        Raw_reads = str(json_object["summary"]["before_filtering"]["total_reads"])
        Read_length = str(json_object["summary"]["before_filtering"]["read1_mean_length"])
        
        if Read_type == "Paired":        
            assert Read_length == str(json_object["summary"]["before_filtering"]["read2_mean_length"])

        Filtered_read = str(json_object["summary"]["after_filtering"]["total_reads"])

        fw.write('\t'.join([sample, Read_length, Raw_reads, Filtered_read]) + "\n")   
