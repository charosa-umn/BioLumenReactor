import os
import glob
#import Adafruit_GPIO.SPI as SPI  #May be unused
#import Adafruit_MCP3008

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
