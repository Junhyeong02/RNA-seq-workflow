import sys
import os

read_info = sys.argv[1]
mapping_info = sys.argv[2]

assert os.path.exists(read_info)
assert os.path.exists(mapping_info)

read_f = open(read_info)
mapping_f = open(mapping_info)

read_f.readline()
mapping_f.readline()

HEADER = "name\tsample\tread_type\tread_length\traw_reads\tfiltered_read\tmapping_read\tmapping_rate"

print(HEADER)

for read_line, mapping_line in zip(sorted(read_f.readlines()), sorted(mapping_f.readlines())):
    read_data = read_line.strip().split('\t')
    mapping_data = mapping_line.strip().split('\t')
    
    try:
        assert read_data[0] == mapping_data[0]
        assert read_data[1].strip() == mapping_data[1]
        assert read_data[2] == mapping_data[2]
    except AssertionError:
        print(read_data[0], mapping_data[0], read_data[1], mapping_data[1], read_data[2], mapping_data[2], sep = ",")
        raise AssertionError

    if read_data[1] == "tissue":
        name = read_data[0]
    
    else:
        name = read_data[0] + "." + read_data[1]

    print('\t'.join([name] + read_data[2:] + mapping_data[3:]))


read_f.close()
mapping_f.close()
    
    
