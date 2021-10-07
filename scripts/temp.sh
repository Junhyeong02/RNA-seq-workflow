### 2021.08.20 ECW.PL.L1 ###


# python3 04_sub.Hisat2.py ../03.Genome_Index/ECW.v.1.0_genomic ../01.Preprocessed_data/PE/ECW.PL/NoUse/ ../04.Mapping/ECW.PL/ 10 PE

python3 05_sub.stringtie.py ../02.Genome_data/ECW_0820.gtf ../04.Mapping/ECW.PL/\*L1 10 CaECW

# python3 07_sub.READ_info.py ../01.Preprocessed_data/\*E/\*/\*.json ../01.Preprocessed_data/PE/ECW.PL/NoUse/\*.json > ../SupplData/READ_info.txt

# python3 07_sub.Mapping_info.py ../04.Mapping/\*/\*.log > ../SupplData/MAPPING_INFO.txt

# python3 07_sub.Table.py ../SupplData/READ_info.txt ../SupplData/MAPPING_INFO.txt  > ../SupplData/TABLE.txt
