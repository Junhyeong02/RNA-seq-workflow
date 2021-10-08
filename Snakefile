# snakefile

import subprocess
import numpy as np
import pandas as pd
from glob import glob

configfile: "config.yaml"

fastq = list(glob(config["path"]["raw_data"] + "*_R1.fastq.gz"))
tissue_list = [fq.split("/")[-1].replace("_R1.fastq.gz", "") for fq in fastq]
core_ratio = 1/len(tissue_list)

rule all:
    input:
        config["path"]["exp_data"] + "CM334.tissue.TPM.txt",
        config["path"]["exp_data"] + "CM334.tissue.log.txt"

rule Indexing:
    input:
        config["path"]["genome_data"] + config["target_genome"] + ".fa"
    output:
        expand(config["path"]["indexing_data"] + config["target_genome"] + ".{num}.ht2", num = [i for i in range(1, 9)])
    message: ""
    shell:
        "hisat2-build -f {input} {wildcards.genome}" 

rule Preprocessing:
    input:
        fq = config["path"]["raw_data"] + "{filename}_R1.fastq.gz"
    output:
        fq1 = config["path"]["preprocessed_data"] + "{filename}_R1.filter.fastq.gz",
        fq2 = config["path"]["preprocessed_data"] + "{filename}_R2.filter.fastq.gz",
        json = config["path"]["preprocessed_data"] + "{filename}.filter.json",
        html = config["path"]["preprocessed_data"] + "{filename}.filter.html"
    params:
        pair = config["path"]["raw_data"] + "{wildcards.filename}_R2.fastq.gz",
        qcut = config["fastp"]["Qcut"],
        len_cut = int(subprocess.check_output("gunzip -c {input.fq} | head -n 2 |tail -n 1 |wc -L", shell = True)) * config["fastp"]["cut_ratio"],
        # len_cut = int(subprocess.check_output(["gunzip", "-c", "{input.fq}", \
        #                                        "|head", "-n", "2", \
        #                                        "|tail", "-n", "1", \
        #                                        "|wc", "-L"], shell = True)) * config["fastp"]["cut_ratio"] , 
        readqual = subprocess.check_output(["gunzip", "-c", "{input.fq}",\
                                            "|head", "-n", "1000", "|", "sed", "-n", "'4~4p'",\
                                            "|tr", "-d", "'\\n'"], shell = True) ,
        phred = (lambda x: \
                "" if (max(ord(c) for c in x)-33) <= 41 else "-6")(params.readqual)

    threads: workflow.cores * core_ratio
    message: ""
    run:
        if config["read_type"] == "Single":
            shell("fastp -i {input.fq} -o {output.fq1} -l {params.len_cut} \
                   -q {params.qcut} -w {threads} \
                   -h {output.html} \
                   -j {output.json} {phred}; \
                   touch {output.fq2}") 
        else:
            shell("fastp -i {input.fq} -I {parmas.pair} -o {output.fq1} -O {output.fq2} \
                   -l {params.lencut} -q {params.qcut} -w {threads}) \
                   -h {output.html} \
                   -j {output.json} {phred};") 

rule Mapping:
    input:
        fq1 = config["path"]["preprocessed_data"] + "{filename}_R1.filter.fastq.gz",
        fq2 = config["path"]["preprocessed_data"] + "{filename}_R2.filter.fastq.gz",
        ht = expand(config["path"]["indexing_data"] + config["target_genome"]+".{num}.ht2", num = [i for i in range(1, 9)])
    output:
        sam = temp(config["path"]["mapping_data"] + "{filename}.sam"),
        log = config["path"]["mapping_data"] + "{filename}.log"
    params: 
        index_path = config["path"]["indexing_data"] + config["target_genome"]
    threads: workflow.cores * core_ratio
    message: ""
    run:
        if config["read_type"] == "Single":         
           shell("hisat2 -p {threads} --dta -x {params.index_path} \
                  --rna-strandness R --summary-file {output.log} \
                  -U {input.fq1} -S {output.sam}")

        else:
           shell("hisat2 -p {threads} --dta -x {params.index_path} \
                  --rna-strandness RF --summary-file {output.log} \
                  -1 {input.fq1} -2 {input.fq2} -S {output.sam}")
        
rule Samtool_sort:
   input:
       config["path"]["mapping_data"] + "{filename}.sam"
   output:
       config["path"]["mapping_data"] + "{filename}.bam"
   threads: workflow.cores * core_ratio
   message: ""
   shell:
       "samtools sort -@ {threads} -o {output} {input}"

rule Quantification:
    input:
        bam = config["path"]["mapping_data"] + "{filename}.bam",
        GTF = config["path"]["genome_data"]+ config["target_gtf"] + ".gtf"
    output:
        config["path"]["mapping_data"] + "{filename}." + config["target_gtf"]+ ".gtf"
    params:
        Prefix = config["stringtie"]["prefix"]
    threads: workflow.cores * core_ratio
    message: ""
    shell:
        "stringtie -p {threads} -e -G {input.GTF} -o {output} {params.Prefix} {input.bam}"

rule Result_assemble:
    input:
        expand(config["path"]["mapping_data"] + "{tissue}." + config["target_gtf"] + ".gtf", tissue = tissue_list)
    output:
        FPKM = config["path"]["exp_data"] + "{filename}.FPKM.txt",
        TPM  = config["path"]["exp_data"] + "{filename}.TPM.txt"
    message: ""
    script:
        "scripts/06_sub.FPKM_TPM.py"

rule create_Preprocessing_log:
    input:
        expand(config["path"]["preprocessed_data"] + "{tissue}.filter.json", tissue = tissue_list)
    output:
        temp("preprocessing_rate.txt")
    params:
        read_type = config["read_type"]
    message: ""
    script:
        "scripts/07_sub.READ_info.py"

rule create_Mapping_log:
    input:
        expand(config["path"]["mapping_data"] + "{tissue}.log", tissue = tissue_list)
    output:
        temp("mapping_rate.txt")
    message: ""
    script:
        "scripts/07_sub.Mapping_info.py"

rule create_log:
    input:
        pre = "preprocessing_rate.txt",
        mapping = "mapping_rate.txt"
    output:
        config["path"]["exp_data"] + "{filename}.log.txt"
    message: ""
    run:
        pre_df = pd.read_csv(input.pre, sep = "\t", index_col = "Sample")
        map_df = pd.read_csv(input.mapping, sep = "\t", index_col = "Sample")
        df = pd.merge(pre_df, map_df, on = "Sample", how = "inner")
        df = df[["Sample", "Mean length of reads", "Number of raw reads", "Number of filtered reads", \
                 "Number of mapped read", "LAlignment rate"]]
        df.to_csv("{output}", sep = "\t", index = None)

# rule Average: 
#     input:
#         Exp_data = config["path"]["exp_data"] + "{filename}.txt",
#         Sample_group_data = "sample_group.txt"
#     output:
#         config["path"]["exp_data"] + "{filename}.avg.txt"
#     script:
#         "scripts/06_sub.Average.py"

