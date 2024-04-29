
from polarize import Rotor
from mcs import MCS, Axis


class Polarizer():
    def __init__(self, start_angle = -90, end_angle = 90, step_angle = 5):
        self.rotor = Rotor()
        self.rotor.set_up()
        self.start = int(start_angle * 80) # 1 degree = 80 steps
        self.end = int(end_angle * 80)
        self.step = step_angle * 80
        self.rotor.move(position=self.start)

class Actuator():
    def __init__(self):
        self._controller_0 = MCS(locator="network:sn:MCS2-00000286")
        self._dhandle_0 = self._controller_0.dHandle()
        self._controller_1 = MCS(locator="network:sn:MCS2-00002502")
        self._dhandle_1 = self._controller_1.dHandle()
        #self._controller_2 = MCS(locator="usb:sn:MCS2-00000014")
        #self._dhandle_2 = self._controller_2.dHandle()
        self.x_axis = Axis(dhandle=self._dhandle_0, channel=0)
        print('x_axis!')
        self.y_axis = Axis(dhandle=self._dhandle_0, channel=1)
        print('y_axis!')
        self.z_axis = Axis(dhandle=self._dhandle_0, channel=2)
        print('z_axis!')
        self.p_axis = Axis(dhandle=self._dhandle_1, channel=2)
        print('p_axis!')
        #self.lg_axis = Axis(dhandle=self._dhandle_2, channel=0)
        print('lg_axis!')
        #self.rg_axis = Axis(dhandle=self._dhandle_2, channel=1)
        print('rg_axis!')
        #self.s_axis = Axis(dhandle=self._dhandle_2, channel=2)
        print('s_axis!')

        self.axes = [self.x_axis, self.y_axis, self.z_axis, self.x_axis, self.y_axis, self.z_axis, self.p_axis ] #self.lg_axis, self.rg_axis, self.s_axis, 

    def close(self):
        self._controller_0.close()
        self._controller_1.close()