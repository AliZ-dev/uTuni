
import sys
import site
sys.path.append(site.getsitepackages()[0] + "/smaract")
import ctl
import os
import time
from datetime import datetime as dt
from cv2 import waitKey
import imageio
import csv
from mcs import *
import mccdaq
import PyDMX
from mfa_calib import image_scan
import numpy as np
from simple_pid import PID
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


    
class Tensile():
    def __init__(self, tensile_axis, data):
        self._force_data = data
        self._axis = tensile_axis
        self._init_pos = int(tensile_axis.get_position() / 1000000)
        self._displacement = 10
        self._end_pos = self._init_pos + self._displacement
        self._stations = list( range(self._init_pos, self._end_pos-1, self._displacement) )
        self._next_step = 0
        self._force_stations = []
        self._force_step = 0
        self._speed = tensile_axis.get_speed()
        self._tensile_pos = tensile_axis.get_position()
        self._init_time = 0
        self._break = True
        self._first_time = True
        #self.mfasession = MFAsession
        #self.TEST_NUM = test_num

    def is_station(self):
        #condition = self._rotor.get_position() in self._stations
        #print("f:{}, fd:{}, fStep:{}, p:{}. pd:{}, pStep:{}".format(round(self._force_data.read(),2), 
        #                                        round(self._force_stations[self._force_step],2), self._force_step, 
        #                                        int(self._tensile_pos / 1000000), self._stations[self._next_step], self._next_step))
        """
        if round(self._force_data.read(),2) == round(self._force_stations[self._force_step],2): #) >= 0
            self.stop()
            print("force_step: {}".format(self._force_step))
            #self._force_step += 1
            print("Reached to {} force".format( self._force_data.read() ))
            return True
        el
        """
        if int(self._tensile_pos / 1000000) == self._stations[self._next_step]:#int(self._tensile_pos / 1000000) in self._stations:
            #if current_pos in self._stations:
            print("Pos_step: {}".format(self._next_step))
            print( "Reached to {} station".format( self._tensile_pos) )#self._axis.get_position() ) )
            #self._next_step += 1
            return True
        
        else:
            #print("Tensile Not Yet!")
            return False
    def next_station(self):
        
        self._axis.move(displacement_size = self._stations[self._next_step], direction = 0)

    def tensile_end(self):

        if self._next_step == len(self._stations):
            print( "Reached to {}, final station!".format( self._tensile_pos) )
            return True
        else:
            return False
        
        """
        if self._next_step == len(self._stations) \
                or self._force_step == len(self._force_stations):
            print( "Reached to {}, final station!".format( self._tensile_pos) )
            return True
        else:
            return False
        """
    
    def normal(self, displacement = 1000):
        self._init_pos = int(self._axis.get_position() / 1000000)
        print('get pos 0')
        self._displacement = displacement
        self._end_pos = self._init_pos - self._displacement
        self._axis.move_mode(mode = ctl.MoveMode.CL_ABSOLUTE)
        self._axis.set_speed(speed=16) #um/s
        self._stations = list( range(self._init_pos, self._end_pos-1, -self._displacement) )
        print('stations: {}'.format(self._stations))
        #self._axis.move(displacement_size = displacement, direction = 0)

    def cyclic(self, cycles_per_session = 10, sessions = 10, displacement = 100, freq = 1):
        self._init_pos = int(self._axis.get_position() / 1000000)
        self._displacement = displacement
        self._end_pos = self._init_pos - self._displacement
        self._axis.move_mode(mode = ctl.MoveMode.CL_ABSOLUTE) #force-controlled: CL_RELATIVE, normal: CL_ABSOLUTE
        self._axis.set_speed(speed=100) #um/s
        cycles = cycles_per_session * sessions
        self._end_time = cycles * freq
        self._time_stations = np.arange(1/freq,self._end_time+1/freq, 1/freq)
        print(self._time_stations)
        init_force = round(self._force_data.read(),2)
        force_limit = 0.3
        top_force = init_force + force_limit
        cyclic_force_station = list ( np.arange(init_force, top_force+0.02, force_limit) )
        cyclic_station = list( np.arange(self._init_pos, self._end_pos-1, -self._displacement) )
        self._force_step = 0
        self._force_stations = []
        self._stations = []
        self._Tmfa = cycles_per_session * 2
        for _ in range(cycles):
            self._stations.append(cyclic_station[0])
            self._stations.append(cyclic_station[1])
            self._force_stations.append(cyclic_force_station[0])
            self._force_stations.append(cyclic_force_station[1])
        self._stations.append(cyclic_station[0])
        self._force_stations.append(cyclic_force_station[0])
        print(self._stations)
        print(self._force_stations)
    
    def stepwise(self, displacement = 90, increment = 30, hold_time = 30):
        self._init_pos = int(self._axis.get_position() / 1000000)
        self._displacement = displacement
        self._end_pos = self._init_pos - self._displacement
        self._axis.move_mode(mode = ctl.MoveMode.CL_ABSOLUTE)
        self._axis.set_speed(speed=5) #um/s
        self._stations = list( range(self._init_pos, self._end_pos-1, -increment) )

    def cyclic_stepwise(self, displacement = 10, increment = 2, hold_time = 30):
        self._init_pos = int(self._axis.get_position() / 1000000)
        self._displacement = displacement
        self._end_pos = self._init_pos - self._displacement
        self._axis.move_mode(mode = ctl.MoveMode.CL_ABSOLUTE)
        self._axis.set_speed(speed=2) #um/s
        self._stations = list( range(self._init_pos, self._end_pos-1, -increment) )
        print(len(self._stations))
        for i in range(2,len(self._stations)+2+1,2):
            self._stations.insert(i,self._init_pos)

    def force_control(self):
        pid = PID(2, 0.15, 0.001, setpoint=1)
        #pid.setpoint = setpoint
        pid.output_limits = (-1, 1)
        #pid.sample_time = 0.003
        #pid = PIDController()

        return pid
    
    def target_force(self, first_time=False, f0=0, f1 = 0):
        ts = self._time_stations
        fd = f1
        time = (dt.now().second + dt.now().microsecond/1e6 - self._init_time)%10
        if first_time:
            print('first_time')
            time = 0
            self._first_time = False
            self._init_time = dt.now().second + dt.now().microsecond/1e6
        if time < ts[0]: fd = 0
        elif time < ts[-1]: fd = 0.1
        else: fd = self._force_data.read() - f0
        return fd, time

    def stop(self):
        self._axis.stop()
        #self._break = False
    
    def write_data(self, flagObj, TEST_NUM):
        #forceData = self._force_data
        #TEST_NUM -= 1
        filename = os.getcwd().replace("/script", "/data/") + "tensile_" + str(TEST_NUM).zfill(4) + ".csv"
        print('welcome to write')
        #time.sleep(0.01)
        #print('get pos 1')
        #print(type(mydict))
        while flagObj.tensile:
            with open(filename, 'a') as csvfile:  
                # creating a csv dict writer object  
                writer = csv.writer(csvfile, delimiter=',')
                self._tensile_pos = self._axis.get_position()
                #print(str(dt.now())[:-2].replace(":", "."))
                #mydict = {'dateNtime': str(dt.now())[:-2].replace(":", "."), 'displacement': axisObj.get_position(), 'force': forceObj.read()}
                mydata = [str(dt.now())[:-2].replace(":", "."), self._axis.get_position(), self._force_data.read()]
                #print('get pos 1')
                #print(type(mydict))
                writer.writerow(mydata)
                #if not flagObj.tensile:
                #    break
                #print('ready to next while')
                #data_lock.acquire()
                #print('acquired by write')
        print(self._stations)
        #print(self._force_stations)
        #print(self._force_step)
        #print(self._time_stations)
        #print("f:{}, fd:{}, fStep:{}, p:{}. pd:{}, pStep:{}".format(round(self._force_data.read(),2), 
        #                                        round(self._force_stations[self._force_step-1],2), self._force_step, 
        #                                        int(self._tensile_pos / 1000000), self._stations[self._next_step-1], self._next_step))
        print('write done!')

    def fatigue_transit(self, flagObj):
        #flagObj.mfa = True
        print("\nMFA flag on")
        time.sleep(1)
        #flagObj.mfa = False
        print("\nMFA flag off")
        time.sleep(1)
        #if self.cycle_session == 0:
        #    self._next_step = 0
        #    self._force_step = 0
        #if self.cycle_session != 0: # and (self._next_step == len(self._stations)-1):
        self._next_step = self._next_step % len(self._stations)
        self._force_step = self._force_step % len(self._stations)
        
    def run(self, mode, flagObj):
        print('run')
        print(mode)
        print(flagObj.tensile)
        n = 0
        self.cycle_session = 0
        max_cycle_session = 2 # all cycles = max_cycle_sessoin * cyclic().cycles
        #time.sleep(1)
        pid = self.force_control()
        #force_smooth = np.array()
        init_force = self._force_data.read()
        init_time = dt.now().second + float(dt.now().microsecond)/1e6
        #print (init_force)
        t = 0 #(dt.now().second + float(dt.now().microsecond)/1e6 - init_time)
        fd =init_force
        while flagObj.force_control and flagObj.tensile and \
                    t < self._end_time: #(dt.now().second + dt.now().microsecond/1e6 - init_time)%10
            if ( mode != "normal" ):
                print("force_controlled")
                fd, t = self.target_force(first_time=self._first_time, f0 = init_force, f1=fd)
                pid.setpoint = fd
                control_signal = pid( (self._force_data.read() - init_force) )
                self._axis.move(displacement_size = -round(control_signal,6), direction = 0)
                #time.sleep(0.00010)
                print("fd=, pidOut={}".format(self._force_data.read(), control_signal))
        #if t > self._end_time: flagObj.tensile = False

        while flagObj.tensile:
            #print(mode)
            #self._tensile_pos = self._axis.get_position()
            if ( mode == "normal" ):
                if ( self.is_station() ):
                    self._next_step += 1
                    if self.tensile_end():
                        flagObj.tensile = False
                        break
                    print("\nGo to the next step")
                    self.next_station()
                    flagObj.tensile = True
                else:
                    flagObj.tensile = True
                time.sleep(0.01)

            if ( mode != "normal" and mode != "fatigue" ):
                #print("is station?")
                if ( self.is_station() ):
                    #flagObj.mfa = True
                    #print("\nMFA flag on")
                    #time.sleep(25)
                    #self.session += 1
                    #flagObj.mfa = False
                    #print("\nMFA flag off")
                    self._next_step += 1
                    self._force_step += 1
                    if self.tensile_end():
                        flagObj.tensile = False
                        #self.mfasession = 0
                        break
                    print("\nGo to the next step")
                    self.next_station()
                    #time.sleep(1) # this sleep is for preventing to detect the current station in slow movements
                    flagObj.tensile = True
                else:
                    flagObj.tensile = True
            
            if ( mode == "fatigue" ):
                #print("is station?")
                if ( self.is_station() ):
                    print("session:{}".format(self.cycle_session))
                    if n == 0: # or n == 1:
                        flagObj.mfa = True
                        print("\nMFA flag on")
                        time.sleep(26)
                        flagObj.mfa = False
                        print("\nMFA flag off")
                        time.sleep(1)
                        self.cycle_session += 1
                    if n == self._Tmfa: #((self._force_step)%self._Tmfa == 0 or (self._force_step)%self._Tmfa == 4):
                        #self.fatigue_transit(flagObj=flagObj)
                        #time.sleep(5)
                        flagObj.mfa = True
                        print("\nMFA flag on")
                        time.sleep(26)
                        flagObj.mfa = False
                        print("\nMFA flag off")
                        time.sleep(1)
                        self.cycle_session += 1
                        n = 0
                    n += 1
                    #elif ((self._force_step/2)%self._Tmfa == 1):
                        #self.fatigue_transit(flagObj=flagObj)
                        #time.sleep(5)
                     
                    self._next_step += 1
                    self._force_step += 1
                    if self.tensile_end():
                        flagObj.tensile = False
                        #self.mfasession = 0
                        break
                    print("\nGo to the next step")
                    self.next_station()
                    #time.sleep(1)
                    flagObj.tensile = True
                else:
                    flagObj.tensile = True




class MFA():
    def __init__(self, polarizer, pol_step):
        self._rotor = polarizer.rotor
        self._start = polarizer.start
        self._stop = polarizer.end
        self._step = polarizer.step
        self._pol_step = pol_step
        self._stations = range(self._start, self._stop+1, self._step)
        self._channel = 1
        self.dmx = PyDMX.DMX()
        self.dmx.next_channel(1)
        self._color = ["r", "g", "b"]
        self.mfasession = 0
        self._imgScan = image_scan()
        #print("stations = {}".format(self._stations))

    def next(self):
        self._rotor.shift(delta=self._step)

    def is_station(self):
        #condition = self._rotor.get_position() in self._stations
        #print(condition)
        if self._rotor.get_position() in self._stations:
            print("Reached to {} station".format(self._rotor.get_position()))
            return True
        else:
            print("MFA Not Yet!")
            return False
    def mfa_end(self):
        if self._rotor.get_position() == self._stop:
            return True
        else:
            return False

    def run(self, videoFrame):
        
        if self.is_station():
            save_path = os.getcwd().replace("/script", "/data/") +  \
                        self._color[self._channel-1] + "_" + str(int((self._rotor.get_position() - self._start)/80)).zfill(4) + \
                        "_step_" + str(self.mfasession).zfill(3) + "_" + str(dt.now())[:-4].replace(":", ".") + ".tiff" # "-" + color + "0" + str(self._counter) 
            print(save_path)
            imageio.imwrite(save_path, videoFrame[:,:,3-self._channel])
            #self._channel += 1
            print("MFA Captured!")
            self.next()
            if self.mfa_end():
                self._rotor.move(position=self._start)
                print("MFA next channel!")
                time.sleep(3.5)
                self._channel += 1
                if self._channel == 4: # 4
                    self._channel = 1  # 1
                    self.dmx.next_channel(self._channel)
                    self.mfasession += 1
                    print("MFA next session!")
                    
                    #self._imgScan.uniformity()
                    #self._imgScan.polarization(pol_step = self._pol_step)
                    return False
            self.dmx.next_channel(self._channel)
            print("\nGo to the next station")
            time.sleep(0.5)
        return True


