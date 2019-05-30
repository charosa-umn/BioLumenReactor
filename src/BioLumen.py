import time
import csv
import RPi.GPIO as io
from pumps import *
from temp import *
#pH configuration
mcp = Adafruit_MCP3008.MCP3008(18, 25, 23, 24)

def start_up():
    io.setwarnings(False)
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(10,GPIO.OUT)
    initiatePumps()

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
                pumpBase(0.5)
            elif cur_pH < 6.0:
                pumpAcid(0.5)
            elif cur_pH <= 7.5 and cur_pH >= 6.5:
                turnOff()
                
            ##Print realtime stats
            print("Time:", cur_time.tm_hour, " ", cur_time.tm_min, " ", cur_time.tm_sec, " ", cur_temp, " ", cur_pH)

            ##Write the data to the csv
            data_writer.writerow([cur_time.tm_hour, cur_time.tm_min, cur_time.tm_sec, total_seconds, cur_temp, cur_pH])


if __name__ == "__main__":
    try:
        start_up()
        print("Ready")#light up led
        io.output(10, True)
        io.wait_for_edge(22, GPIO.RISING)
        io.output(10, False)
        main()
    except KeyboardInterrupt:  
        io.cleanup()       # clean up GPIO on CTRL+C exit  
    io.cleanup()           # clean up GPIO on normal exit  
