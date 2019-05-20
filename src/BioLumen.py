import os
import glob
import time
import csv
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as io
h1 = 16
h2 = 20
oh1 = 19
oh2 = 26
load = 21
io.setup(h1, io.OUT)
io.setup(h2, io.OUT)
io.setup(oh1, io.OUT)
io.setup(oh2, io.OUT)
io.setup(load, io.OUT)
io.cleanup()
#pH configuration
mcp = Adafruit_MCP3008.MCP3008(18, 25, 23, 24)

##Run the system commands to init the interface
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

##These are the paths to the temp sensor
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def pumpAcid(time):
    io.output(h1, True)
    io.output(h2, False)
    io.output(oh1, False)
    io.output(oh2, False)
    io.output(load, True)
    time.sleep(time)
    turnOff()

def pumpBase(time):
    io.output(oh1, True)
    io.output(oh2, False)
    io.output(h1, False)
    io.output(h2, False)
    io.output(load, True)
    time.sleep(time)
    turnOff()

def turnOff():
    io.output(oh1, False)
    io.output(oh2, False)
    io.output(oh1, False)
    io.output(oh2, False)
    io.output(load, False)

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
            ##Gather ph average over a set time 
            for j in range(5):
                total+=mcp.read_adc(0)-300
                time.sleep(0.2)
            cur_pH = (-(((total_pH/5) * 0.013671875) - 7)+7)
            if cur_pH > 8.0:
                pumpBase()
            elif cur_pH < 6.0:
                pumpAcid()
            elif cur_pH <= 7.5 and cur_pH >= 6.5:
                turnOff()
                
            ##Print realtime stats
            print("Time:", cur_time.tm_hour, " ", cur_time.tm_min, " ", cur_time.tm_sec, " ", cur_temp, " ", cur_pH)

            ##Write the data to the csv
            data_writer.writerow([cur_time.tm_hour, cur_time.tm_min, cur_time.tm_sec, total_seconds, cur_temp, cur_pH])


if __name__ == "__main__":
    main()
