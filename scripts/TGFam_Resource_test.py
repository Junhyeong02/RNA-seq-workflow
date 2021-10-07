import sys
import os
import re
from PyCode.Filehandle3 import *
from Bio import SeqIO

def DoTest(gff_path, fasta_path, CDS_path, Protein_path, HEAD, Result_path):
    if not os.path.exists("temp"):
        os.mkdir("temp")

    test_result_CDS = Result_path + HEAD+ "_CDS.txt"
    test_result_Protein = Result_path + HEAD+ "_PEP.txt"

    ####### make CDS file ##########
    print("\nmake CDS file...")
    GeneData = GffReader(gff_path)
    out_path = CDSextracter(GeneData, fasta_path, "temp/{}_CDS.fasta".format(HEAD), show_terminal = False)
    print(out_path)
    # print("CDS :{} ".format(len(GeneData)))
    
    ###### make Protein file (translation)#######
    print("\ntranslation")    
    out_path_pep = "temp/{}_PEP.fasta".format(HEAD)

    print(out_path_pep)
    fw_protein = open(out_path_pep, 'w')
    
    for record in SeqIO.parse(out_path, "fasta"):
        fw_protein.write(">{}\n{}\n".format(record.id, record.seq.translate(stop_symbol = "*")))

    fw_protein.close()

    ###### do test (CDS) ##########
    mySeq = {record.id : record.seq for record in SeqIO.parse(out_path, "fasta")}
    print("\nstart cds test")

    fw = open(test_result_CDS, "w")
    
    error_count = 0
    Nodata_count = 0

    for record in SeqIO.parse(CDS_path, "fasta"):
        if record.id in mySeq:
            if record.seq != mySeq[record.id]:
                fw.write(">{}\n{}\n{}\n".format(record.id, mySeq[record.id], record.seq))
                error_count += 1
        else:
            fw.write(">{}\nNo Data\n{}\n".format(record.id, record.seq))
            Nodata_count += 1
        # print(record.id)

    print("\nCDS test Result")
    print("{} CDS Seq Error".format(error_count))
    print("{} CDS Seq Not Found".format(Nodata_count))
    print("my CDS : {}, Original CDS : {}".format(len(mySeq), len(list(SeqIO.parse(CDS_path, "fasta")))))

    fw.close()

    ###### do test (Protein) ##########
    
    mySeq = {record.id : record.seq for record in SeqIO.parse(out_path_pep, "fasta")}
    print("\nstart pep test")

    fw = open(test_result_Protein, "w")
    
    error_count = 0
    Nodata_count = 0

    for record in SeqIO.parse(Protein_path, "fasta"):
        if record.id in mySeq:
            if record.seq != mySeq[record.id]:
                fw.write(">{}\n{}\n{}\n".format(record.id, mySeq[record.id], record.seq))
                error_count += 1
        else:
            fw.write(">{}\nNo Data\n{}\n".format(record.id, record.seq))
            Nodata_count += 1
        # print(record.id)

    print("\nProtein test Result")
    print("{} Protein Seq Error".format(error_count))
    print("{} Protein Seq Not Found".format(Nodata_count))
    print("my Protein : {}, Original Protein : {}".format(len(mySeq), len(list(SeqIO.parse(Protein_path, "fasta")))))

    print(gff_path+" end")
    return 


if __name__ == "__main__":
    print("start")
    GFF_PATH = sys.argv[1]
    FASTA_PATH = sys.argv[2]
    CDS_PATH = sys.argv[3]
    PEP_PATH = sys.argv[4]
    HEAD = sys.argv[5]
    
    if not os.path.exists("result"):
        os.mkdir("result")

    DoTest(GFF_PATH, FASTA_PATH, CDS_PATH, PEP_PATH, HEAD, "result/")

    print("end")




