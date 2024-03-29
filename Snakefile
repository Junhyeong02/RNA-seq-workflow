# snakefile

import sys
import subprocess
from glob import glob

configfile: "config.yaml"

fastq = list(glob(config["path"]["raw_data"] + "*_R1.fastq.gz"))
tissue_list = sorted([fq.split("/")[-1].replace("_R1.fastq.gz", "") for fq in fastq])
core_ratio = 1/len(tissue_list)

rule all:
    input:
        config["path"]["exp_data"] + "CM334.tissue.TPM.txt",
        config["path"]["log"] + "CM334.tissue.log.txt"

rule Indexing:
    input:
        config["path"]["genome_data"] + config["target_genome"] + ".fa"
    output:
        expand(config["path"]["indexing_data"] + config["target_genome"] + ".{num}.ht2", num = [i for i in range(1, 9)])
    message: ""
    params: 
        genome = config["target_genome"]
    shell:
        "hisat2-build -f {input} {params.genome}" 

rule Preprocessing:
    input:
        fq = config["path"]["raw_data"] + "{filename}_R1.fastq.gz"
    output:
        fq1 = config["path"]["preprocessed_data"] + "{filename}_R1.filter.fastq.gz",
        fq2 = config["path"]["preprocessed_data"] + "{filename}_R2.filter.fastq.gz",
        json = config["path"]["preprocessed_data"] + "{filename}.filter.json",
        html = config["path"]["preprocessed_data"] + "{filename}.filter.html"
    params:
        pair = config["path"]["raw_data"] + "{filename}_R2.fastq.gz",
        qcut = config["fastp"]["Qcut"],
        cut_ratio = config["fastp"]["cut_ratio"],
        read_type = config["read_type"]

    threads: workflow.cores * core_ratio
    message: ""
    script:
        "scripts/smk.fastp.py"

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
           shell("hisat2 -p {threads} --dta -x {params.index_path}"+\
                 " --rna-strandness R --summary-file {output.log}" +\
                 " -U {input.fq1} -S {output.sam}")

        else:
           shell("hisat2 -p {threads} --dta -x {params.index_path}" + \
                 " --rna-strandness RF --summary-file {output.log}" + \
                 " -1 {input.fq1} -2 {input.fq2} -S {output.sam}")
        
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
        "stringtie -p {threads} -e -G {input.GTF} -o {output} -l {params.Prefix} {input.bam}"

rule Result_assemble:
    input:
        expand(config["path"]["mapping_data"] + "{tissue}." + config["target_gtf"] + ".gtf", tissue = tissue_list)
    output:
        FPKM = config["path"]["exp_data"] + "{filename}.FPKM.txt",
        TPM  = config["path"]["exp_data"] + "{filename}.TPM.txt"
    params:
        gtf_path = config["path"]["mapping_data"],
        target_gtf = config["target_gtf"]
    message: ""
    script:
        "scripts/smk.result.py"

rule create_Preprocessing_log:
    input:
        expand(config["path"]["preprocessed_data"] + "{tissue}.filter.json", tissue = tissue_list)
    output:
        out = config["path"]["log"] + "preprocessing_rate.txt"
    params:
        read_type = config["read_type"]
    message: ""
    script:
        "scripts/smk.read_info.py"

rule create_Mapping_log:
    input:
        expand(config["path"]["mapping_data"] + "{tissue}.log", tissue = tissue_list)
    output:
        out = config["path"]["log"] + "mapping_rate.txt"
    message: ""
    script:
        "scripts/smk.mapping_info.py"

rule create_log:
    input:
        pre = config["path"]["log"] + "preprocessing_rate.txt",
        mapping = config["path"]["log"] + "mapping_rate.txt"
    output:
        config["path"]["log"] + "{filename}.log.txt"
    message: ""
    script:
        "scripts/smk.create_log.py"

