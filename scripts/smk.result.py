from glob import glob

GTF_PATH = "04.Mapping/"

gtf_list = snakemake.input

HEADER = "GeneID\t" + '\t'.join([gtf.replace(GTF_PATH, "") for gtf in gtf_list])

PATH_FPKM = snakemake.output.FPKM
PATH_TPM = snakemake.output.TPM

fw_FPKM = open(PATH_FPKM, "w")
fw_TPM = open(PATH_TPM, "w")

FPKM = {}
TPM = {}
gene_order = list()

print(fw_FPKM.write(HEADER + '\n'))
print(fw_TPM.write(HEADER + '\n'))

for gtf in gtf_list:
    print(gtf)
    
    with open(gtf) as f:
        for line in f.readlines():
            if line[0] == "#" or " FPKM " not in line:
                continue

            data = line.strip().split('\t')[-1].split("; ")
            

            gene_name = data[0].split()[1].strip('"')
            FPKM_data = data[-2].split()[1].strip('"')
            TPM_data = data[-1].split()[1].replace(";", "").strip('"')

            if gene_name not in gene_order:
                gene_order.append(gene_name)
                FPKM[gene_name] = list()
                TPM[gene_name] = list()

            FPKM[gene_name].append(FPKM_data)
            TPM[gene_name].append(TPM_data)

for gene_name in gene_order:
    fw_FPKM.write(gene_name + '\t' + '\t'.join(FPKM[gene_name]) + '\n')
    fw_TPM.write(gene_name + '\t' + '\t'.join(TPM[gene_name]) + '\n')

fw_FPKM.close()
fw_TPM.close()
