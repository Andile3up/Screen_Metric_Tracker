import boto3
import sys

if(len(sys.argv)!=4):
	print("Total arguments:", len(sys.argv))
	sys.exit(1)
	
file_name=sys.argv[1]
file_split=file_name.split("/")

data_group=sys.argv[2]

device_id=sys.argv[3]

process_file_name=file_split[-1]
process_file_name=process_file_name.split(".")
process_file_name_no_file_type=process_file_name[0]
print(process_file_name_no_file_type)
process_file_name_no_file_type=process_file_name_no_file_type.split('_')

final_file_name=process_file_name_no_file_type[1]+".parquet"

date=process_file_name_no_file_type[2].split('-')

year=date[0]
month=date[1]
day=date[2]

print(data_group)
print('vehicle/'+data_group+'/device_id='+device_id+'/year='+year+'/month='+month+'/day='+day+"/"+final_file_name)

s3 = boto3.client('s3')
s3.upload_file(file_name, 'threeupads-south-africa-data', 'vehicle/'+data_group+'/device_id='+device_id+'/year='+year+'/month='+month+'/day='+day+"/"+final_file_name)
sys.exit(0)
