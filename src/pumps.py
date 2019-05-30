##import RPi.GPIO as io
##To turn a pump on, one of
##the pins of the pump (H or OH)
##must be high and the other
##low. Additionally, the load
##pin must be high. All pins
##are set to low in the turnOff
##method.


def initiatePumps():
    io.setup(16, io.OUT)    #H 1
    io.setup(20, io.OUT)    #H 2
    io.setup(19, io.OUT)    #OH 1
    io.setup(26, io.OUT)    #OH 2
    io.setup(21, io.OUT)  #Acid Load
    io.setup(13, io.OUT)  #Base Load
    io.cleanup()
    turnOff()

def pumpAcid(time):
    io.output(16, True)     #H 1
    io.output(20, False)    #H 2
    io.output(19, False)    #OH 1
    io.output(26, False)    #OH 2
    io.output(21, True)   #Acid Load
    time.sleep(time)
    turnOff()

def pumpBase(time):
    io.output(19, True)     #OH 1
    io.output(26, False)    #OH 2
    io.output(16, False)    #H 1
    io.output(20, False)    #H 2
    io.output(13, True)   #Base Load
    time.sleep(time)
    turnOff()

def turnOff():
    io.output(19, False)    #OH 1
    io.output(26, False)    #OH 2
    io.output(16, False)    #H 1
    io.output(20, False)    #H 2
    io.output(21, False)  #Acid Load
    io.output(13, False)  #Base Load
