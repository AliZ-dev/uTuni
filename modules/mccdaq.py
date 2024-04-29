import numpy as np
from uldaq import (get_daq_device_inventory, DaqDevice, InterfaceType,
                   AiInputMode, Range, AInFlag)




class Data():
    def __init__(self, channel = 0):
        self._chan = channel
        # Get a list of available DAQ devices
        self._dev = get_daq_device_inventory(InterfaceType.USB)
        # Create a DaqDevice Object and connect to the device
        self._daq_dev = DaqDevice(self._dev[0])
        self._daq_dev.connect()
        # Get AiDevice and AiInfo objects for the analog input subsystem
        self._ai_dev = self._daq_dev.get_ai_device()
        #ai_info = ai_device.get_info()
        #channel = 0
        # Read and display voltage values for all analog input channels
        #for channel in range(ai_info.get_num_chans()):

    def read(self, buffer_size = 1):
        #data = []#np.zeros((buffer_size,1),dtype=np.float)
        #for i in range(buffer_size):
        #print(i)
        data = self._ai_dev.a_in(self._chan, AiInputMode.DIFFERENTIAL,Range.BIP10VOLTS, AInFlag.DEFAULT)
            
        return data