import sys
import site
sys.path.append(site.getsitepackages()[0] + "/smaract")
import ctl
from mcs import MCS, Axis
from layout import RET
import numpy as np
import cv2
import cvui


def intensity_profile(Frame, frameRet, videoTop):
        """
        This function is used for drwaing the live intensity profile on the percieved camera view
        """
        profile_v = np.mean(videoTop[:,int(frameRet[RET.CAM][RET.VIDW_0]/3):int(2*frameRet[RET.CAM][RET.VIDW_0]/3),1], axis=1)
        profile_v = np.append(profile_v, [0, 255])
        cvui.sparkline(Frame, profile_v/255.0, frameRet[RET.CAM][RET.VIDX_1], frameRet[RET.CAM][RET.VIDY_1],
                        frameRet[RET.CAM][RET.VIDW_1], int(frameRet[RET.CAM][RET.VIDH_1]/2), 0xff0000)
        profile_h = np.mean(videoTop[int(frameRet[RET.CAM][RET.VIDH_0]/3):int(2*frameRet[RET.CAM][RET.VIDH_0]/3),:,1], axis=0)
        profile_h = np.append(profile_h, [0, 255])
        cvui.sparkline(Frame, profile_h/255.0, frameRet[RET.CAM][RET.VIDX_1], frameRet[RET.CAM][RET.VIDY_1]+int(frameRet[RET.CAM][RET.VIDH_1]/2),
                        frameRet[RET.CAM][RET.VIDW_1], int(frameRet[RET.CAM][RET.VIDH_1]/2), 0x00ff00)
        
        for i in range(0,11):
            grid = i/10
            points_v = np.ones(profile_v.shape)*grid
            points_v = np.append(points_v, [0,1])
            points_h = np.ones(profile_h.shape)*grid
            points_h = np.append(points_h, [0,1])
            cvui.sparkline(Frame, points_v, frameRet[RET.CAM][RET.VIDX_1], frameRet[RET.CAM][RET.VIDY_1],
                        frameRet[RET.CAM][RET.VIDW_1], int(frameRet[RET.CAM][RET.VIDH_1]/2), 0x0000ff)
            cvui.sparkline(Frame, points_h, frameRet[RET.CAM][RET.VIDX_1], frameRet[RET.CAM][RET.VIDY_1]+int(frameRet[RET.CAM][RET.VIDH_1]/2),
                    frameRet[RET.CAM][RET.VIDW_1], int(frameRet[RET.CAM][RET.VIDH_1]/2), 0x0000ff)
class ImgTools():
    """
    This class includes the methods for applying some manipulation techniques on the percieved image 
    such as Ruler measurement and Zoom function in a ROI
    """
    def __init__(self, layout):
        self._myLayout = layout
        self.zoom = 1.0
        self.top = 0
        self.bottom = layout._winVidH_0 - 1
        self.left = 0
        self.right = layout._winVidW_0 - 1
        self._Xpos = -1
        self._Ypos = -1
        self.pointNum = 0
        self.Lines = []
        self.pointerX = -1
        self.pointerY = -1
        self._offsetX = layout._winVidX_0
        self._offsetY = layout._winVidY_0 + 20
        self._scale = (1,1)


    def _boundary(self, **kwargs):
        new_w, new_h = kwargs['zoom'] * kwargs['w'], kwargs['zoom'] * kwargs['h']
        center = (kwargs['zoom'] * kwargs['x'], kwargs['zoom'] * kwargs['y'])
        if center[1] - kwargs['h']/2 <= 0:    top = 0
        elif center[1] + kwargs['h']/2 >= new_h - 1:  top = new_h - kwargs['h']
        else:   top = center[1] - kwargs['h']/2
        bottom = top + kwargs['h'] - 1

        if center[0] - kwargs['w']/2 <= 0:    left = 0
        elif center[0] + kwargs['w']/2 >= new_w:  left = new_w - kwargs['w']
        else:   left = center[0] - kwargs['w']/2
        right = left + kwargs['w'] - 1

        return int(top), int(bottom), int(left), int(right)

    def roi(self, layoutRet):
        status = layoutRet[RET.CAM][RET.STAT_0]
        w = layoutRet[RET.CAM][RET.VIDW_0]
        h = layoutRet[RET.CAM][RET.VIDH_0] - 20

        

        if status == cvui.OVER:
            
            pos = cvui.mouse()
            self.pointerX = pos.x - self._offsetX
            self.pointerY = pos.y - self._offsetY
            #print("Mouse is: OVER ({} , {})".format(pointerX, pointerY))
        
        if status == cvui.WHEEL_UP:
            print("Mouse is: OVER ({} , {})".format(self.pointerX, self.pointerY))
            if self.zoom < 5.0: self.zoom += 0.1
            self.top, self.bottom, self.left, self.right = self._boundary(zoom = self.zoom, x = self.pointerX, y = self.pointerY, w = w, h = h)
            print("Mouse is: WHEEL UP")

        if status == cvui.WHEEL_DOWN:
            print("Mouse is: OVER ({} , {})".format(self.pointerX, self.pointerY))
            if self.zoom > 1.0: self.zoom -= 0.1
            self.top, self.bottom, self.left, self.right = self._boundary(zoom = self.zoom, x = self.pointerX, y = self.pointerY, w = w, h = h)
            print("Mouse is: WHEEL DOWN")
        
        if status == cvui.OUT:
            self.pointerX = -1
            self.pointerY = -1
        
    def _line_measure(self, X, Y):
        self.Lines[-1]['p1'] = (X, Y)
        self.Lines[-1]['d'] = np.sqrt( ((self.Lines[-1]['p1'][0] - self.Lines[-1]['p0'][0]) * self._scale[0])**2 +
                                            ((self.Lines[-1]['p1'][1] - self.Lines[-1]['p0'][1]) * self._scale[1])**2)
        self.Lines[-1]['ang'] = np.degrees( np.arccos( ((self.Lines[-1]['p1'][0] - self.Lines[-1]['p0'][0]) * self._scale[0]) / self.Lines[-1]['d']) ) if (
                                (self.Lines[-1]['p1'][1] - self.Lines[-1]['p0'][1]) * self._scale[1]) <=0 else -np.degrees( np.arccos( ((self.Lines[-1]['p1'][0] - self.Lines[-1]['p0'][0]) * self._scale[0]) / self.Lines[-1]['d']) )
        #print(self._scale)
 
    def measure(self,video_frame, layoutRet, left_stat, right_stat, scale):
        self._scale = scale
        status = layoutRet[RET.CAM][RET.STAT_0]
        #print(left_stat)
        #print(right_stat)
        if status == cvui.OVER:
            Xpos = cvui.mouse().x - self._offsetX
            Ypos = cvui.mouse().y - self._offsetY
            #print("Mouse is: OVER ({} , {})".format(self._Xpos, self._Ypos))
            if self.pointNum % 2:   self._line_measure(X = Xpos, Y = Ypos)
                
            
        if status == cvui.CLICK and left_stat:
            Xpos = cvui.mouse().x - self._offsetX
            Ypos = cvui.mouse().y - self._offsetY
            self.pointNum += 1
            #print("Mouse Clicked: ({} , {})".format(Xpos, Ypos))
            if self.pointNum % 2:   self.Lines.append( {'p0':(Xpos, Ypos), 'p1':(Xpos, Ypos), 'd':0.0, 'ang':0.0})
            else:   self._line_measure(X = Xpos, Y = Ypos)


        if status == cvui.CLICK and right_stat:
            self.pointNum = 0
            self.Lines = []
        #print(self.Lines)

        if self.pointNum > 0:
            #print("points = {}".format(self.pointNum))
            #print(self._vals['lines'][0][0])
            #print(self._vals['lines'][0][1])
            for line in self.Lines:
                cv2.line(video_frame, line['p0'], line['p1'], (0,0,255), 1)
                cv2.putText(video_frame, text = "{:.1f}".format(line['d']),
                    org = ( int(np.mean([ line['p0'][0],line['p1'][0] ])) - 10, int(np.mean([ line['p0'][1],line['p1'][1] ])) + 5 ),
                    fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.5, color = (0,0,255), thickness = 2)
                cv2.putText(video_frame, text = "{:.1f}".format(line['ang']),
                    org = ( int(np.mean([ line['p0'][0],line['p1'][0] ])) - 10, int(np.mean([ line['p0'][1],line['p1'][1] ])) + 20 ),
                    fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.5, color = (0,0,255), thickness = 2)


        return video_frame

    

class SELECT:
    area = -1
    param = 0

class Manual():
    """
    This class includes the the atributes and methods for manual controlling of the connected actuators 
    through mouse scrolling on the Action Areas dedicated to each actuator.
    """
    def __init__(self, layout, actuator):
        self._prop = SELECT
        self._gripper_range = [1, 2, 5, 10, 20, 50, 100]
        self._stage_range = [100, 200, 500, 1000, 2000]
        self._motion_range = [5, 10, 20, 100, 200, 500, 1000, 2000, 380.7]
        self._myLayout = layout
        self._myAct = actuator
        self._inc = [self._gripper_range[1], self._gripper_range[1], self._stage_range[1],
                        self._motion_range[4], self._motion_range[2], self._motion_range[0], self._motion_range[0]]
        #self.lg_pos = float(actuator.lg_axis.get_position()) / 1000000 #lg
        #self.rg_pos = float(actuator.rg_axis.get_position()) / 1000000 #rg
        #self.s_pos = float(actuator.s_axis.get_position()) / 1000000 #s
        self.x_pos = float(actuator.x_axis.get_position()) / 1000000
        self.y_pos = float(actuator.y_axis.get_position()) / 1000000
        self.z_pos = float(actuator.z_axis.get_position()) / 1000000
        self.p_pos = 0 # float(actuator.p_axis.get_position()) / 1000000
        self._pos = [self.x_pos, self.y_pos, self.z_pos, self.x_pos, self.y_pos, self.z_pos, self.p_pos] #self.lg_pos, self.rg_pos, self.s_pos, 
        self._myLayout.update_values(pos_vals = self._pos, inc_vals = self._inc)
        self._inc_indx = [0, 0, 0, 0, 0, 0, 0]
        #self._inc_vals = layout.return_values()

    def update(self):
        status, inc = self._myLayout.return_values()
        for indx in range(7): #[0,1,2,4,5,6]:
            if status[indx] == cvui.OVER:
                self._prop.area = indx
                #print("ok")
            if status[indx] == cvui.CLICK:
                print("click")
                print(self._prop.param)
                self._prop.param += 1
                print(self._prop.param)
                print("clicked")
                self._prop.param %= 2
                print(self._prop.param)
            elif status[indx] == cvui.WHEEL_UP:
                print(cvui.mouse().x)
                if self._prop.param:
                    print("Hi")
                    self._inc_indx[indx] += 1
                    self._inc_indx[indx] %= len(self._gripper_range)
                    inc[indx] = self._gripper_range[self._inc_indx[indx]]
                else:
                    self._myAct.axes[indx].move_mode(ctl.MoveMode.CL_RELATIVE)
                    self._myAct.axes[indx].set_speed(0)
                    self._myAct.axes[indx].move(displacement_size=int(inc[indx]), direction=0)
                    #self._pos[indx] += self._inc[self._inc_indx[indx]]
                    self._update_values()
            elif status[indx] == cvui.WHEEL_DOWN:
                if self._prop.param:
                    self._inc_indx[indx] -= 1
                    self._inc_indx[indx] %= len(self._gripper_range)
                    inc[RET.LG] = self._gripper_range[self._inc_indx[indx]]
                else:
                    self._myAct.axes[indx].move_mode(ctl.MoveMode.CL_RELATIVE)
                    self._myAct.axes[indx].set_speed(0)
                    self._myAct.axes[indx].move(displacement_size=int(inc[indx]), direction=1)
                    #self._pos[indx] -= self._inc[self._inc_indx[indx]]
                    self._update_values()
        
        if status[self._prop.area] == cvui.OUT:
            
            #print("out")
            self._prop.area = -1
            self._prop.param = 0
        
        
        self._myLayout.update_values(area_num = self._prop.area, pos_vals = self._pos, inc_vals = self._inc)

    def _update_values(self):
        for i in range(7):
            print(i)
            self._pos[i] = float( self._myAct.axes[i].get_position() ) / 1000000
        




