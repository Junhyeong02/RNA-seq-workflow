##### 2021.08.20 #####

#grep "overall alignment rate" ../04.Mapping/*.*/*.log ../04.Mapping/Heinz/*.log > ../SupplData/alignment_rate.txt

# alingment_rate.txt %s/Heinz/Heinz.tissue/g

# python3 07_sub.Mapping_rate.py ../SupplData/alignment_rate.txt ../SupplData/alignment_rate_total.txt

python3 07_sub.READ_info.py ../01.Preprocessed_data/\*E/\*/\*.json ../01.Preprocessed_data/PE/ECW.PL/NoUse/\*.json > ../SupplData/READ_info.txt

# cp ../04.Mapping/*.*/*.log ../04.Mapping/Heinz/*.log ../TEST/04.Mapping/

python3 07_sub.Mapping_info.py ../04.Mapping/\*/\*.log > ../SupplData/MAPPING_INFO.txt

python3 07_sub.Table.py ../SupplData/READ_info.txt ../SupplData/MAPPING_INFO.txt > ../SupplData/TABLE.txt



