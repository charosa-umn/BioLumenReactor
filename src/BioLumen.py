import os
import glob
import time
import csv
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

#pH configuration
mcp = Adafruit_MCP3008.MCP3008(18, 25, 23, 24)

##Run the system commands to init the interface
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

##These are the paths to the temp sensor
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

##Get the raw data provided by the sensor in the terminal
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        ##Convert to C
        temp_c = float(temp_string) / 1000.0
        return temp_c


def main():
    start_time = time.time()  ##Time the program started
    with open('data_file.csv', mode='w') as data_file:
        ##Add column headings to the csv
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['Hour', 'Min', 'Second', 'Total Seconds', 'Temp', 'pH'])
        i=0
        while i<5:
            ##Gather time
            cur_time = time.localtime(time.time())
            total_seconds = time.time()-start_time
            ##Gather temp
            cur_temp = read_temp()
            ##Gather ph
            cur_pH = mcp.read_adc(0) * 0.013671875
            
            ##Print realtime stats
            print("Time:", cur_time.tm_hour, " ", cur_time.tm_min, " ", cur_time.tm_sec, " ", cur_temp, " ", cur_pH)

            ##Write the data to the csv
            data_writer.writerow([cur_time.tm_hour, cur_time.tm_min, cur_time.tm_sec, total_seconds, cur_temp, cur_pH])
            i+=1
            time.sleep(1)

if __name__ == "__main__":
    main()
