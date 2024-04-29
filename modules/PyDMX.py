import serial
#from pylibftdi import Device
import time
import numpy as np


class DMX:
    def __init__(self,COM='/dev/dmx/ttydmx',Brate=250000,Bsize=8,StopB=2): #/dev/dmx/ttydmx
        #start serial
        self.ser = serial.Serial(COM,baudrate=Brate,bytesize=Bsize,stopbits=StopB)
        #with Device(Cable="FT2URZCA",mode='t') as self.ser:#,bytesize=Bsize,stopbits=StopB), device_id="FT2URZCA",
        #    self.ser.ftdi_fn.ftdi_set_line_property(8, 2, 0)
        #    self.ser.baudrate = Brate
        #self.ser.open()
        self.data = np.zeros([513],dtype='uint8')
        self.data[0] = 0 # StartCode
        self.sleepms = 50.0
        self.breakus = 176.0
        self.MABus = 16.0
        
    def set_random_data(self):
        self.data[1:513]= np.random.rand(512)*255

    def set_data(self,id,data):
        self.data[id]=data

    def send(self):
        # Send Break : 88us - 1s
        self.ser.break_condition = True
        time.sleep(self.breakus/1000000.0)
        
        # Send MAB : 8us - 1s
        self.ser.break_condition = False
        time.sleep(self.MABus/1000000.0)
        
        # Send Data
        self.ser.write(bytearray(self.data))
        
        # Sleep
        time.sleep(self.sleepms/1000.0) # between 0 - 1 sec

    def next_channel(self, channel = 1):
        tmp_data = np.array([0,0,0])     # Benchmark---Methodology---Fatigue
        if channel == 1: value = 140     # 120---------115-----------140
        elif channel == 2: value = 245   # 200---------205-----------245
        elif channel == 3: value = 120   # 105---------105-----------120
        tmp_data[channel-1] = value
        self.data[1:4] = tmp_data
        self.send()
        time.sleep(0.005)
        self.send()

    def sendzero(self):
        self.data = np.zeros([513],dtype='uint8')
        self.send()

    def __del__(self):
        print('Close serial server!')
        self.sendzero()
        self.ser.close()


#if __name__ == '__main__':
    #dmx = DMX('/dev/dmx/ttydmx')#serial/by-id/usb-FTDI_USB-RS485_Cable_FT2URZCA-if00-port0')
    #dmx.next_channel(2)
    #for i in range(0,10):
    #    dmx.set_random_data()
    #    dmx.send()
    #for i in range(1,4):
    #    dmx.sendzero()
    #    dmx.data[1:4] = np.zeros([3],dtype='uint8')
    
#    dmx.data[1:4] = np.array([100, 0, 0])
#    dmx.send()
#    time.sleep(0.5)
    #dmx.data[1:4] = np.array([100, 0, 0])
#    dmx.send()
#    time.sleep(20.5)
#    dmx.data[1:4] = np.array([0, 100, 0])
#    dmx.send()
#    time.sleep(0.5)
    #dmx.data[1:4] = np.array([0, 100, 0])
#    dmx.send()
#    time.sleep(20.5)
#    dmx.data[1:4] = np.array([0, 0, 100])
#    dmx.send()
#    time.sleep(0.5)
    #dmx.data[1:4] = np.array([0, 0, 100])
#    dmx.send()
#    time.sleep(20.5)

        
    
#    del dmx
