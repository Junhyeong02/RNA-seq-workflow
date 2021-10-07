import sys
import os
import subprocess

# input_path_dir = sys.argv[1]       ######## ../00.Raw_data/PE/ECW.PL/
# output_path_dir = sys.argv[2]      ######## ../01.Preprocessed_data/PE/ECW.PL/

Qcut = snakemake.Qcut                 ######## 20
CPU = snakemake.CPU                   ######## 2
cut_ratio = float(snakemake.cut_ratio)     ######## 0.7
PairType = snakemake.Pair_type             ######## PE or SE

if PairType == "SE":
    out_files = snakemake.output[0] # files.replace(".fastq.", ".filter.fastq.").replace(input_path_dir, output_path_dir)
    html_file = out_files.replace(".fastq.gz", ".html")
    json_file = out_files.replace(".fastq.gz", ".json")
        
    len_cut = int(subprocess.check_output(["gunzip", "-c", snakemake.input[0], "|head", "-n", "2", "|", "tail", "-n", "1", "|", "wc", "-L"]))*cut_ratio
    ReadQual = subprocess.check_output(["gunzip", "-c", snakemake.input[0], "|", "head", "-n", "1000", "|", "sed", "-n", "'4~4p'", "|", "tr", "-d", "'\\n'"])
    Phred = "" if (max(ord(c) for c in ReadQual)-33) <= 41 else "-6"
        
    p = subProcess.Popen("fastp -i {} -o {} -l {} -q {} -w {} -h {} -j {}".format(snakemake.input[0], out_files, len_cut, Qcut,\
                                                                        CPU, html_file, json_file, Phred))

    # print("fastp -i {} -o {} -l {} -q {} -w {} -h {} -j {}".format(files, out_files, int(len_cut), Qcut,\
    #                                                                     CPU, html_file, json_file, Phred))

elif PairType == "PE":
            html_file = out_files1.replace(".fastq.gz", ".html")
            json_file = out_files1.replace(".fastq.gz", ".json")            

            len_cut1 = int(os.popen("gunzip -c {} |head -n 2 |tail -n 1|wc -L".format(files1)).read())*cut_ratio
            # len_cut2 = int(os.popen("gunzip -c {} |head -n 2 |tail -n 1|wc -L".format(files2)).read())*cut_ratio
            
            ReadQual = os.popen("gunzip -c {} | head -n 1000 | sed -n '4~4p' | tr -d '\\n'".format(files1)).read()
            Phred = "" if (max(ord(c) for c in ReadQual)-33) <= 41 else "-6"
        
            # if len_cut1 != len_cut2:
            #     print("len_cut error")

            os.system("fastp -i {} -I {} -o {} -O {} -l {} -q {} -w {} -h {} -j {} {}".format(files1, files2,\
                      out_files1, out_files2, int(len_cut1), Qcut, CPU, html_file, json_file, Phred))

            print("fastp -i {} -I {} -o {} -O {} -l {} -q {} -w {} -h {} -j {} {}".format(files1, files2,\
                      out_files1, out_files2, int(len_cut1), Qcut, CPU, html_file, json_file, Phred))

    else:
        print("PairType option must be SE or PE")
        break

