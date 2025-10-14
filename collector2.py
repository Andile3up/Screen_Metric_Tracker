import pandas as pd
df = pd.read_csv('tracker/output.txt', header=None,names=["mac_addr","start_time","end_time"])
print(df)
print(df.dtypes)
df.to_parquet('output.parquet', compression='gzip')
