import time
import serial
import uuid
from datetime import date
import datetime
from time import sleep
# Returns the current local date
today = date.today()
print("Today date is: ", today)
#print ("The random id using uuid1() is : ",end="")
trip_id=uuid.uuid1()

ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
Impressions_file = open("3up_workspace/data/Impressions/raw/raw_"+str(trip_id)+"_"+str(today)+".txt", "a")
GPS_file = open("3up_workspace/data/GPS/raw/raw_"+str(trip_id)+"_"+str(today)+".txt", "a")
while 1:
        try:
                x=ser.readline()
                line=x.decode(encoding="utf-8")
                if(line[:6]=='$GPGGA'):
                        #print(line[:-1])
                        line_col=line.split(',')
                        print(line_col)
                        GPS_file.write(line_col[1]+","+line_col[2]+","+line_col[3]+","+line_col[4]+","+line_col[5]+'\n')
                elif(line[0]=='$'):
                        print("nothing")
                else:
                        now_time = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
                        print(now_time+" "+line[:-1])
                        Impressions_file.write(now_time+" "+line)
        except serial.serialutil.SerialException:
                sleep(10)
        except UnicodeDecodeError:
                print("error decoding input")
        except:
                print("unknown error")
        
Impressions_file.close()
GPS_file.close()
