import datetime
import re
import sys

print("Total arguments:", len(sys.argv))
print("Script name:", sys.argv[0])
print("Arguments:", sys.argv[1])
file_name=sys.argv[1]

pattern = "^[[][0-9]{4}[-][0-9]{2}[-][0-9]{2}\s[0-9]{2}[:][0-9]{2}[:][0-9]{2}[\]]\s\w{2}\s\w{2}\s\w{2}\s\w{2}\s\w{2}\s\w{2}\s$"  # Pattern to check if the string starts with an uppercase letter
string = "[2025-09-21 00:17:20]"

match = re.match(pattern, string)

if match:
    print("Match found")
else:
    print("No match")
# using now() to get current time
current_time = datetime.datetime.now()

# Printing value of now.
print("Time now at greenwich meridian is:", current_time)
big={}
tub=[]
with open(file_name, 'r') as file:
    print("summarising file: ",file_name)
    for line in file:
        #print(line)
        match = re.match(pattern, line)
        if(match):
            mac=line[22:].strip()
            time=line[1:20].strip()
            dt = datetime.datetime(int(time[0:4]),int(time[5:7]),int(time[8:10]),int(time[11:13]),int(time[14:16]),int(time[17:19]))
            #print(time,dt.timestamp())
            if(not(mac in big)):
                big[mac]=[dt.timestamp(),dt.timestamp()]
            else:
                if(big[mac][1]+60*3<dt.timestamp()):
                    tub.append([mac,big[mac]])
                    del(big[mac])
                    big[mac]=[dt.timestamp(),dt.timestamp()]
                else:
                    big[mac][1]=dt.timestamp()
print(tub)
for itht in tub:
    print(itht)
    
file_split=file_name.split("/")
process_file_name=file_split[-1][3:]
print(process_file_name)
    
Impressions_file = open("data/Impressions/processed/processed"+process_file_name, "a")
for key, value in big.items():
    print(key,value,value[1]-value[0])
    Impressions_file.write(key+","+str(int(value[0]))+","+str(int(value[1]))+"\n")
    
Impressions_file.close()
