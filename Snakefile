# snakefile

import subprocess
from glob import glob

configfile: "config.yaml"

fastq = list(glob(config["path"]["raw_data"] + "*_R1.fastq.gz"))
tissue_list = [fq.split("/")[-1].replace("_R1.fastq.gz", "") for fq in fastq]

rule all:
    input:
        config["path"]["exp_data"] + "CM334.tissue.TPM.txt"

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
        config["path"]["raw_data"] + "{filename}_R1.fastq.gz"
    output:
        fq1 = config["path"]["preprocessed_data"] + "{filename}_R1.filter.fastq.gz",
        fq2 = config["path"]["preprocessed_data"] + "{filename}_R2.filter.fastq.gz"
    params:
        pair = config["path"]["raw_data"] + "{filename}_R2.fastq.gz",
        output_path = config["path"]["preprocessed_data"],
        Qcut = config["fastp"]["Qcut"],
        len_cut = lambda input: \
                  int(subprocess.check_output(["gunzip", "-c", input, \
                                               "|head", "-n", "2", \
                                               "|tail", "-n", "1", \
                                               "|wc", "-L"]))*config["fastp"]["cut_ratio"] , 
        ReadQual = lambda input: \
                   subprocess.check_output(["gunzip", "-c", input,\
                                            "|head", "-n", "1000", "|", "sed", "-n", "'4~4p'",\
                                            "|tr", "-d", "'\\n'"]) ,
        Phred = lambda params: \
                "" if (max(ord(c) for c in params.ReadQual)-33) <= 41 else "-6"
    threads: 10
    message: ""
    run:
        if config["read_type"] == "Single":
            shell("fastp -i {input} -o {output.fq1} -l {params.len_cut} \
                   -q {params.Qcut} -w {threads} \
                   -h {params.output_path}{wildcards.filename}.filter.html \
                   -j {params.output_path}{wildcards.filename}.filter.json; \
                   touch {output.fq2}") 
        else:
            shell("fastp -i {input} -I {parmas.pair} -o {output.fq1} -O {output.fq2} \
                   -l {params.lencut} -q {params.Qcut} -w {threads}) \
                   -h {params.output_path}{wildcards.filename}.filter.html \
                   -j {params.output_path}{wildcards.filename}.filter.json;") 

rule Mapping:
    input:
        fq1 = config["path"]["preprocessed_data"] + "{filename}_R1.filter.fastq.gz",
        fq2 = config["path"]["preprocessed_data"] + "{filename}_R2.filter.fastq.gz",
        ht = expand(config["path"]["indexing_data"] + config["target_genome"]+".{num}.ht2", num = [i for i in range(1, 9)])
    output:
        temp(config["path"]["mapping_data"] + "{filename}.sam")
    params: 
        index_path = config["path"]["indexing_data"] + config["target_genome"]
    threads: 20
    message: ""
    run:
        if config["read_type"] == "Single":         
           shell("hisat2 -p {threads} --dta -x {params.index_path} \
                  --rna-strandness R --summary-file {wildcards.filename}.log \
                  -U {input.fq1} -S {wildcards.filename}.sam")

        else:
           shell("hisat2 -p {threads} --dta -x {index_path} \
                  --rna-strandness RF --summary-file {wildcards.filename}.log \
                  -1 {input.fq1} -2 {input.fq2} -S {output}")
        
rule Sort_sam:
   input:
       config["path"]["mapping_data"] + "{filename}.sam"
   output:
       config["path"]["mapping_data"] + "{filename}.bam"
   threads: 20
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
    threads: 20
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
    output:
    message:
    script:

rule create_Mapping_log:
    input:
    output:
    message:
    script:


# rule Average: 
#     input:
#         Exp_data = config["path"]["exp_data"] + "{filename}.txt",
#         Sample_group_data = "sample_group.txt"
#     output:
#         config["path"]["exp_data"] + "{filename}.avg.txt"
#     script:
#         "scripts/06_sub.Average.py"

