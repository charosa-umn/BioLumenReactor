import time
import datetime
import csv
import RPi.GPIO as io
from pumps import *
from temp import *
#Database/website
from firebase import firebase
#pH configuration
import Adafruit_MCP3008
mcp = Adafruit_MCP3008.MCP3008(18, 25, 23, 24)
firebase = firebase.FirebaseApplication('https://biolumenreactor.firebaseio.com')


def start_up():
    firebase.put('','/running',1)
    io.setwarnings(False)
    io.setup(22, io.IN, pull_up_down=io.PUD_DOWN)
    io.setup(10,io.OUT) #LED light
    io.output(10, False)
    initiatePumps()
    ready = False
    while not ready and read_temp() > 26.0 and read_temp() < 29.0:
        for j in range(5):
             total+=mcp.read_adc(0)-300 ##-300 to adjust
             time.sleep(1)
        ##Convert to pH
        cur_pH = (-(((total/5) * 0.013671875) - 7)+7)
        ##Pump base or not
        if cur_pH > 8.0:
            pumpBase(0.5)
            ready = False
        elif cur_pH < 6.0:
            pumpAcid(0.5)
            ready = False
        elif cur_pH <= 7.5 and cur_pH >= 6.5:
            turnOff()
            ready = True


def main():
    end_time = datetime.datetime.now() + datetime.timedelta(hours=8)
    with open('data_file.csv', mode='w') as data_file:
        ##Add column headings to the csv
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['Hour', 'Min', 'Second', 'Total Seconds', 'Temp', 'pH'])
        while (end_time - datetime.datetime.now()).seconds > 0: #while there is still time left
            ##Gather temp
            cur_temp = read_temp()
            ##Gather ph average over a set time
	    total = 0
            for i in range(12):  ##Run for a minute    
                for j in range(5):
                    total+=mcp.read_adc(0)-300 ##-300 to adjust
                    time.sleep(1)

                ##Convert to pH
                cur_pH = (-(((total/5) * 0.013671875) - 7)+7)

                ##Pump base or not
                if cur_pH > 8.0:
                    pumpBase(0.5)
                elif cur_pH < 6.0:
                    pumpAcid(0.5)
                elif cur_pH <= 7.5 and cur_pH >= 6.5:
                    turnOff()
                
            ##Print realtime stats per min
            print("Time:", now.seconds//3600, " ", (now.seconds//60)%60, " ", (now.seconds)%60, " ", cur_temp, " ", cur_pH)

            ##Post to website
            now = end_time-datetime.datetime.now()
            firebase.put('','/hours',now.seconds//3600)
            firebase.put('','/min',(now.seconds//60)%60)
            firebase.put('','/seconds',(now.seconds)%60)
            firebase.put('','/temp',getRandTemp())
            firebase.put('','/ph',getRandpH())
        
            
            ##Write the data to the csv
            data_writer.writerow([now.seconds//3600, (now.seconds//60)%60, now.seconds%60, now.seconds, cur_temp, cur_pH])
    close(data_file)
    print("Process Finished")
    firebase.put('','/running',0)

if __name__ == "__main__":
    try:
        start_up()
        print("Ready")#light up led
        io.output(10, True)
        io.wait_for_edge(22, io.RISING)
        io.output(10, False)
        main()
    except KeyboardInterrupt:
        firebase.put('','/running',-1)
        io.cleanup()       # clean up GPIO on CTRL+C exit  
io.cleanup() # clean up GPIO on normal exit 
