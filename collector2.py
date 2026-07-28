import sys
import pandas as pd

print("Total arguments:", len(sys.argv))
print("Script name:", sys.argv[0])
print("Arguments:", sys.argv[1])
file_name=sys.argv[1]

file_split=file_name.split("/")
process_file_name=file_split[-1]
process_file_name=process_file_name.split(".")
process_file_name=process_file_name[0]
print(process_file_name)

df = pd.read_csv(file_name, header=None,names=["mac_addr_hash","mac_addr_device","start_time","end_time"])
print(df)
print(df.dtypes)
df.to_parquet("../data/Impressions/upload/"+process_file_name+".parquet", compression='gzip')
#sys.exit(1)
