###	Note: you must run this script after "conda activate MS3.4" to use fastp
# perl 03_sub.Pre.pl ../00.Raw_data/SE/CM334.tissue/ ../01.Preprocessed_data/CM334.tissue/ 18 51 20 SE

python3 03_sub.fastp.py ../00.Raw_data/PE/Bac.tissue/ ../01.Preprocessed_data/PE/Bac.tissue/ 20 2 0.7 PE
