import sys
import subprocess

Qcut = snakemake.params.qcut 
CPU = snakemake.threads  
cut_ratio = float(snakemake.params.cut_ratio)
PairType = snakemake.params.read_type

fq = snakemake.input.fq
fq2 = snakemake.params.pair

len_cut = int(int(subprocess.check_output(f"gunzip -c {fq} |head -n 2 |tail -n 1 | wc -L", shell = True))*cut_ratio)
ReadQual = str(subprocess.check_output(f"gunzip -c {fq} | head -n 1000 |sed -n '4~4p' | tr -d '\\n'", shell = True), "utf-8")
Phred = "" if (max(ord(c) for c in ReadQual)-33) <= 41 else "-6"

out1 = snakemake.output.fq1
out2 = snakemake.output.fq2
html = snakemake.output.html
json = snakemake.output.json


subprocess.run('echo "{} {}" > ../test.txt'.format(len_cut, Phred), shell = True)
if PairType == "Single":
    p = subprocess.run(f"fastp -i {fq} -o {out1} -l {len_cut} -q {Qcut} -w {CPU} -h {html} -j {json} {Phred}", shell = True)
    subprocess.run(f"touch {out2}", shell = True)

elif PairType == "Paired":    
    p = subprocess.run(f"fastp -i {fq} -I {fq2} -o {out1} -O {out2} -l {len_cut} -q {Qcut} -w {CPU}" + \
                       f" -h {html} -j {json} {Phred}", shell = True)

