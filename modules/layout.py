
import numpy as np
import cv2
import cvui

class Frame():
    def __init__(self):
        
        self._width = 1600
        self._height = 1000
        self._frame = np.zeros((self._height, self._width, 3), np.uint8)
        self._frame[:] = (49, 52, 49)
        self._name = "uTuni-MEA"


        self._winImgX = int(self._width / 2) + 20
        self._winImgY = 10
        self._winImgW = int(self._width / 2) - 30
        self._winImgH = int(self._height / 6)
        
        self._winImgBtnX_0 = self._winImgX + 5
        self._winImgBtnY_0 = self._winImgY + 25
        self._winImgChkX_0 = self._winImgX + int(self._winImgW / 5) + 10
        self._winImgChkY_0 = self._winImgY + 35
        self._winImgChk_0 = [False]
        self._winImgChkX_1 = self._winImgX + 2 * (int(self._winImgW / 5) + 10)
        self._winImgChkY_1 = self._winImgY + 35
        self._winImgChk_1 = [False]
        self._winImgChkX_2 = self._winImgX + 3 * (int(self._winImgW / 5) + 10)
        self._winImgChkY_2 = self._winImgY + 35
        self._winImgChk_2 = [False]
        self._winImgCntX_0 = self._winImgX + 4 * (int(self._winImgW / 5) + 10)
        self._winImgCntY_0 = self._winImgY + 35
        self._winImgCnt_0 = [0]
        self._winImgTrkX_0 = (self._winImgX + 30)
        self._winImgTrkX_1 = self._winImgW/2 + self._winImgX + 30
        self._winImgTrk_0 = [50.]
        self._winImgTrk_1 = [50.]

        
        self._winIllX = self._winImgX
        self._winIllY = self._winImgY + self._winImgH + 5
        self._winIllW = self._winImgW
        self._winIllH = int(self._height / 6)

        self._winIllChk_0 = [False]
        self._winIllChk_1 = [True]
        self._winIllChk_2 = [False]
        self._winIllChkX_0 = self._winIllX + int(self._winIllW/4) + 10
        self._winIllChkX_1 = self._winIllX + 2 * (int(self._winIllW/4) + 10)
        self._winIllChkX_2 = self._winIllX + 3 * (int(self._winIllW/4) + 10)
        self._winIllTrkY = self._winIllY + (self._winIllH/2)
        self._winIllTrk_0 = [5]
        self._winIllTrk_1 =  [0.] # [int(polarizer_angle)]


        self._winManX = 10
        self._winManY = 10
        self._winManW = int(self._width / 2) - 30
        self._winManH = int(self._height / 3) + 5

        self._winManFrmW = int(self._winManW / 6)
        self._winManFrmH = int(self._winManH / 2) - 40
        self._winManFrmX_0 = self._winManX + 10
        self._winManFrmY_0 = self._winManY + 30
        self._winManFrmPosTxtX_0 = self._winManFrmX_0 + 10
        self._winManFrmPosTxtY_0 = self._winManFrmY_0 + 25
        self._winManFrmIncTxtX_0 = self._winManFrmX_0 + 10
        self._winManFrmIncTxtY_0 = self._winManFrmY_0 +     int(self._winManFrmH)/2 + 18

        self._winManFrmX_1 = self._winManX + (self._winManFrmW + 20)
        self._winManFrmY_1 = self._winManFrmY_0
        self._winManFrmPosTxtX_1 = self._winManFrmX_1 + 10
        self._winManFrmPosTxtY_1 = self._winManFrmY_1 + 25
        self._winManFrmIncTxtX_1 = self._winManFrmX_1 + 10
        self._winManFrmIncTxtY_1 = self._winManFrmY_1 +     int(self._winManFrmH)/2 + 18

        self._winManFrmX_2 = self._winManX + 2 * (self._winManFrmW + 15)
        self._winManFrmY_2 = self._winManFrmY_0
        self._winManFrmPosTxtX_2 = self._winManFrmX_2 + 10
        self._winManFrmPosTxtY_2 = self._winManFrmY_2 + 25
        self._winManFrmIncTxtX_2 = self._winManFrmX_2 + 10
        self._winManFrmIncTxtY_2 = self._winManFrmY_2 +     int(self._winManFrmH)/2 + 18

        self._winManFrmX_3 = self._winManFrmX_0
        self._winManFrmY_3 = self._winManY + (self._winManFrmH + 60)
        self._winManFrmPosTxtX_3 = self._winManFrmX_3 + 10
        self._winManFrmPosTxtY_3 = self._winManFrmY_3 + 25
        self._winManFrmIncTxtX_3 = self._winManFrmX_3 + 10
        self._winManFrmIncTxtY_3 = self._winManFrmY_3 +     int(self._winManFrmH)/2 + 18

        self._winManFrmX_4 = self._winManX + (self._winManFrmW + 20)
        self._winManFrmY_4 = self._winManFrmY_3
        self._winManFrmPosTxtX_4 = self._winManFrmX_4 + 10
        self._winManFrmPosTxtY_4 = self._winManFrmY_4 + 25
        self._winManFrmIncTxtX_4 = self._winManFrmX_4 + 10
        self._winManFrmIncTxtY_4 = self._winManFrmY_4 +     int(self._winManFrmH)/2 + 18

        self._winManFrmX_5 = self._winManX + 2 * (self._winManFrmW + 15)
        self._winManFrmY_5 = self._winManFrmY_3
        self._winManFrmPosTxtX_5 = self._winManFrmX_5 + 10
        self._winManFrmPosTxtY_5 = self._winManFrmY_5 + 25
        self._winManFrmIncTxtX_5 = self._winManFrmX_5 + 10
        self._winManFrmIncTxtY_5 = self._winManFrmY_5 +     int(self._winManFrmH)/2 + 18

        self._winManFrmX_6 = self._winManX + 3 * (self._winManFrmW + 15)
        self._winManFrmY_6 = self._winManFrmY_3
        self._winManFrmPosTxtX_6 = self._winManFrmX_6 + 10
        self._winManFrmPosTxtY_6 = self._winManFrmY_6 + 25
        self._winManFrmIncTxtX_6 = self._winManFrmX_6 + 10
        self._winManFrmIncTxtY_6 = self._winManFrmY_6 +     int(self._winManFrmH)/2 + 18

        self._winManBtnX_0 = self._winManX + 5 * (self._winManFrmW + 5)
        self._winManBtnY_0 = self._winManFrmY_0
        self._winManBtnY_1 = self._winManFrmY_0 +     (self._winManFrmH/3)
        self._winManBtnY_2 = self._winManFrmY_0 + 2 * (self._winManFrmH/3)
        self._winManBtnY_3 = self._winManFrmY_0 + 3 * (self._winManFrmH/3 + 8)
        self._winManBtnY_4 = self._winManFrmY_0 + 4 * (self._winManFrmH/3 + 8)
        self._winManBtnY_5 = self._winManFrmY_0 + 5 * (self._winManFrmH/3 + 8)
        self._winManChkX_0 = self._winManX + 4 * (self._winManFrmW + 15)
        self._winManChkY_0 = self._winManBtnY_0
        self._winManChkY_1 = self._winManBtnY_0 +     (self._winManFrmH/6)
        self._winManChkY_2 = self._winManBtnY_0 + 2 * (self._winManFrmH/6)
        self._winManChkY_3 = self._winManBtnY_2
        self._winManChkY_4 = self._winManFrmY_0 + 3 * (self._winManFrmH/3)
        self._winManChk_0 = [False]
        self._winManChk_1 = [False]
        self._winManChk_2 = [False]
        self._winManChk_3 = [False]
        self._winManChk_4 = [False]

        self._winVidX_0 = self._winManX
        self._winVidY_0 = self._winManH + 30
        self._winVidW_0 = self._winManW
        self._winVidH_0 = (self._height -  self._winManH) - 50
        self._winVidX_1 = self._winImgX
        self._winVidY_1 = self._winVidY_0
        self._winVidW_1 = self._winVidW_0
        self._winVidH_1 = self._winVidH_0

        self._winManFrmX = [self._winManFrmX_0, self._winManFrmX_1, self._winManFrmX_2, self._winManFrmX_3, self._winManFrmX_4, self._winManFrmX_5, self._winManFrmX_6]
        self._winManFrmY = [self._winManFrmY_0, self._winManFrmY_1, self._winManFrmY_2, self._winManFrmY_3, self._winManFrmY_4, self._winManFrmY_5, self._winManFrmY_6]
        #self._data = data_points
        self._area_num = -1


        self.lg_pos = 0
        self.rg_pos = 0
        self.s_pos = 0
        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0
        self.p_pos = 0

        self.lg_inc = 1
        self.rg_inc = 1
        self.s_inc = 1
        self.x_inc = 1
        self.y_inc = 1
        self.z_inc = 1
        self.p_inc = 1

        self._vals = {'test_num': 0, 'zoom': 1.0, 'points': 0, 'lines':[], 'exp_t': 5, 'pol_ang': 0, 'area_num': -1, 'pos_vals': [], 'inc_vals': []}

    
    def name(self):
        return self._name
    
    def content(self):
        return self._frame

    def imageSetting (self):

        cvui.window(self._frame, self._winImgX, self._winImgY, self._winImgW, self._winImgH, "Image Settings")
        btn_0 = cvui.button(self._frame, self._winImgBtnX_0, self._winImgBtnY_0, "Save Image")
        chk_0 = cvui.checkbox(self._frame, self._winImgChkX_0, self._winImgChkY_0, "Record Video", self._winImgChk_0)
        chk_1 = cvui.checkbox(self._frame, self._winImgChkX_1, self._winImgChkY_1, "Crop/Zoom (X{:.1f})".format(self._vals['zoom']), self._winImgChk_1)
        chk_2 = cvui.checkbox(self._frame, self._winImgChkX_2, self._winImgChkY_2, "Ruler", self._winImgChk_2)
        cnt_0 = cvui.counter(self._frame, self._winImgCntX_0, self._winImgCntY_0, self._winImgCnt_0, 1, '%i')
        cvui.text(self._frame, self._winImgTrkX_0, (self._winImgH/2), 'Zoom')
        cvui.trackbar(self._frame, self._winImgTrkX_0, (self._winImgH/2 + 20), (self._winImgW/2 - 40), self._winImgTrk_0, 0., 100., 4, '%.2Lf')
        cvui.text(self._frame, self._winImgTrkX_1, (self._winImgH/2), 'Focus')
        cvui.trackbar(self._frame, self._winImgTrkX_1, (self._winImgH/2 + 20), (self._winImgW/2 - 40), self._winImgTrk_1, 0., 100., 4, '%.2Lf')

        return [btn_0, chk_0, chk_1, chk_2, cnt_0, self._winImgTrk_0, self._winImgTrk_1]
    
    def illumSetting (self):

        cvui.window(self._frame, self._winIllX, self._winIllY, self._winIllW, self._winIllH, "Illumination Settings")
        cvui.text(self._frame, (self._winIllX+5), (self._winIllY+40), 'Wavelengths:')
        chk_0 = cvui.checkbox(self._frame, self._winIllChkX_0, (self._winIllY+40), "RED", self._winIllChk_0)
        chk_1 = cvui.checkbox(self._frame, self._winIllChkX_1, (self._winIllY+40), "Green", self._winIllChk_1)
        chk_2 = cvui.checkbox(self._frame, self._winIllChkX_2, (self._winIllY+40), "Blue", self._winIllChk_2)

        cvui.text(self._frame, self._winImgTrkX_0, self._winIllTrkY, 'Exposure Time')
        winIllTrk_0_ret = cvui.trackbar(self._frame, self._winImgTrkX_0, (self._winIllTrkY + 20), (self._winImgW/2 - 40), self._winIllTrk_0, 5., 155., 5., '%.0Lf', cvui.TRACKBAR_DISCRETE, 5)
        cvui.text(self._frame, self._winImgTrkX_1, self._winIllTrkY, 'Polarizer Angle')
        winIllTrk_1_ret = cvui.trackbar(self._frame, self._winImgTrkX_1, (self._winIllTrkY + 20), (self._winImgW/2 - 40), self._winIllTrk_1, -180, 180, 8, '%i', cvui.TRACKBAR_DISCRETE, 5)

        return [chk_0, chk_1, chk_2, self._winIllTrk_0, winIllTrk_0_ret, self._winIllTrk_1, winIllTrk_1_ret]
    
    def manipulSetting (self):

        cvui.window(self._frame, self._winManX, self._winManY, self._winManW, self._winManH, "Manipulation")
        cvui.window(self._frame, self._winManFrmX_0, self._winManFrmY_0, self._winManFrmW, self._winManFrmH, "Left Gripper")
        self._stat_0 = cvui.iarea(self._winManFrmX_0, self._winManFrmY_0, self._winManFrmW, self._winManFrmH)
        cvui.text(self._frame, self._winManFrmPosTxtX_0, self._winManFrmPosTxtY_0, "Position:", 0.4, 0xffffff)
        cvui.printf(self._frame, self._winManFrmPosTxtX_0, self._winManFrmPosTxtY_0 + 14, 0.4, 0xffffff,"%.1f um", self.lg_pos)
        cvui.text(self._frame, self._winManFrmIncTxtX_0, self._winManFrmIncTxtY_0, "Increment:", 0.4, 0xffffff)
        cvui.printf(self._frame, self._winManFrmIncTxtX_0, self._winManFrmIncTxtY_0 + 14, 0.4, 0xffffff,"%.1f um", self.lg_inc)

        cvui.window(self._frame, self._winManFrmX_1, self._winManFrmY_1, self._winManFrmW, self._winManFrmH, "Right Gripper")
        self._stat_1 = cvui.iarea(self._winManFrmX_1, self._winManFrmY_1, self._winManFrmW, self._winManFrmH)
        cvui.text(self._frame, self._winManFrmPosTxtX_1, self._winManFrmPosTxtY_1, "Position:", 0.4, 0xffffff)
        cvui.printf(self._frame, self._winManFrmPosTxtX_1, self._winManFrmPosTxtY_1 + 14, 0.4, 0xffffff,"%.1f um", self.rg_pos)
        cvui.text(self._frame, self._winManFrmIncTxtX_1, self._winManFrmIncTxtY_1, "Increment:", 0.4, 0xffffff)
        cvui.printf(self._frame, self._winManFrmIncTxtX_1, self._winManFrmIncTxtY_1 + 14, 0.4, 0xffffff,"%.1f um", self.rg_inc)

        cvui.window(self._frame, self._winManFrmX_2, self._winManFrmY_2, self._winManFrmW, self._winManFrmH, "Sample Stage")
        self._stat_2 = cvui.iarea(self._winManFrmX_2, self._winManFrmY_2, self._winManFrmW, self._winManFrmH) 
        cvui.text(self._frame, self._winManFrmPosTxtX_2, self._winManFrmPosTxtY_2, "Position:", 0.4, 0xffffff)
        cvui.printf(self._frame, self._winManFrmPosTxtX_2, self._winManFrmPosTxtY_2 + 14, 0.4, 0xffffff,"%.1f um", self.s_pos)
        cvui.text(self._frame, self._winManFrmIncTxtX_2, self._winManFrmIncTxtY_2, "Increment:", 0.4, 0xffffff)
        cvui.printf(self._frame, self._winManFrmIncTxtX_2, self._winManFrmIncTxtY_2 + 14, 0.4, 0xffffff,"%.1f um", self.s_inc)
        
        cvui.window(self._frame, self._winManFrmX_3, self._winManFrmY_3, self._winManFrmW, self._winManFrmH, "X - Axis")
        self._stat_3 = cvui.iarea(self._winManFrmX_3, self._winManFrmY_3, self._winManFrmW, self._winManFrmH)
        cvui.text(self._frame, self._winManFrmPosTxtX_3, self._winManFrmPosTxtY_3, "Position:", 0.4, 0xffffff)
        cvui.printf(self._frame, self._winManFrmPosTxtX_3, self._winManFrmPosTxtY_3 + 14, 0.4, 0xffffff,"%.1f um", self.x_pos)
        cvui.text(self._frame, self._winManFrmIncTxtX_3, self._winManFrmIncTxtY_3, "Increment:", 0.4, 0xffffff)
        cvui.printf(self._frame, self._winManFrmIncTxtX_3, self._winManFrmIncTxtY_3 + 14, 0.4, 0xffffff,"%.1f um", self.x_inc)
        
        cvui.window(self._frame, self._winManFrmX_4, self._winManFrmY_4, self._winManFrmW, self._winManFrmH, "Y - Axis")
        self._stat_4 = cvui.iarea(self._winManFrmX_4, self._winManFrmY_4, self._winManFrmW, self._winManFrmH)
        cvui.text(self._frame, self._winManFrmPosTxtX_4, self._winManFrmPosTxtY_4, "Position:", 0.4, 0xffffff)
        cvui.printf(self._frame, self._winManFrmPosTxtX_4, self._winManFrmPosTxtY_4 + 14, 0.4, 0xffffff,"%.1f um", self.y_pos)
        cvui.text(self._frame, self._winManFrmIncTxtX_4, self._winManFrmIncTxtY_4, "Increment:", 0.4, 0xffffff)
        cvui.printf(self._frame, self._winManFrmIncTxtX_4, self._winManFrmIncTxtY_4 + 14, 0.4, 0xffffff,"%.1f um", self.y_inc)
        
        cvui.window(self._frame, self._winManFrmX_5, self._winManFrmY_5, self._winManFrmW, self._winManFrmH, "Z - Axis")
        self._stat_5 = cvui.iarea(self._winManFrmX_5, self._winManFrmY_5, self._winManFrmW, self._winManFrmH)
        cvui.text(self._frame, self._winManFrmPosTxtX_5, self._winManFrmPosTxtY_5, "Position:", 0.4, 0xffffff)
        cvui.printf(self._frame, self._winManFrmPosTxtX_5, self._winManFrmPosTxtY_5 + 14, 0.4, 0xffffff,"%.1f um", self.z_pos)
        cvui.text(self._frame, self._winManFrmIncTxtX_5, self._winManFrmIncTxtY_5, "Increment:", 0.4, 0xffffff)
        cvui.printf(self._frame, self._winManFrmIncTxtX_5, self._winManFrmIncTxtY_5 + 14, 0.4, 0xffffff,"%.1f um", self.z_inc)
        
        cvui.window(self._frame, self._winManFrmX_6, self._winManFrmY_6, self._winManFrmW, self._winManFrmH, "Pitch")
        self._stat_6 = cvui.iarea(self._winManFrmX_6, self._winManFrmY_6, self._winManFrmW, self._winManFrmH)
        cvui.text(self._frame, self._winManFrmPosTxtX_6, self._winManFrmPosTxtY_6, "Position:", 0.4, 0xffffff)
        cvui.printf(self._frame, self._winManFrmPosTxtX_6, self._winManFrmPosTxtY_6 + 14, 0.4, 0xffffff,"%.1f um", self.p_pos)
        cvui.text(self._frame, self._winManFrmIncTxtX_6, self._winManFrmIncTxtY_6, "Increment:", 0.4, 0xffffff)
        cvui.printf(self._frame, self._winManFrmIncTxtX_6, self._winManFrmIncTxtY_6 + 14, 0.4, 0xffffff,"%.1f um", self.p_inc)


        btn_0 = cvui.button(self._frame, self._winManBtnX_0, self._winManBtnY_0, "Tensile")
        btn_1 = cvui.button(self._frame, self._winManBtnX_0, self._winManBtnY_1, "Stop")
        btn_2 = cvui.button(self._frame, self._winManBtnX_0, self._winManBtnY_2, "MFA")
        btn_3 = cvui.button(self._frame, self._winManBtnX_0, self._winManBtnY_3, "Uniformity")
        btn_4 = cvui.button(self._frame, self._winManBtnX_0, self._winManBtnY_4, "Help")
        btn_5 = cvui.button(self._frame, self._winManBtnX_0, self._winManBtnY_5, "Exit")


        chk_0 = cvui.checkbox(self._frame, self._winManChkX_0, self._winManChkY_0, "Cyclic", self._winManChk_0)
        chk_1 = cvui.checkbox(self._frame, self._winManChkX_0, self._winManChkY_1, "Step", self._winManChk_1)
        chk_2 = cvui.checkbox(self._frame, self._winManChkX_0, self._winManChkY_2, "Cyclic-Step", self._winManChk_2)
        #cvui.text(self._frame, self._winManChkX_0, self._winManChkY_2+25, "Test # {}".format(self._vals['test_num']))
        btn_6 = cvui.button(self._frame, self._winManChkX_0, self._winManChkY_3, "data")
        chk_4 = cvui.checkbox(self._frame, self._winManChkX_0, self._winManChkY_4, "Manual", self._winManChk_4)

        if self._area_num >=0:
            #print('area_num = {}'.format(self._area_num))
            cvui.rect(self._frame, self._winManFrmX[self._area_num], self._winManFrmY[self._area_num], self._winManFrmW, self._winManFrmH, 0xff0000)

        return [btn_0, btn_1, btn_2, btn_3, btn_4, btn_5, chk_0, chk_1, chk_2, btn_6, chk_4]

    def camFrame(self):
        cvui.window(self._frame, self._winVidX_0, self._winVidY_0, self._winVidW_0, self._winVidH_0, "Top View Camera")
        mouse_stat_0 = cvui.iarea(self._winVidX_0, self._winVidY_0, self._winVidW_0, self._winVidH_0)
        #cvui.window(self._frame, self._winVidX_1, self._winVidY_1, self._winVidW_1, self._winVidH_1, "Side View Camera")
        #cvui.sparkline(self._frame, self.data, self._winVidX_1, self._winVidY_1, self._winVidW_1, self._winVidH_1, 0x00ff00)
        mouse_stat_1 = cvui.iarea(self._winVidX_1, self._winVidY_1, self._winVidW_1, self._winVidH_1)

        return [self._winVidX_0, self._winVidY_0, self._winVidW_0, self._winVidH_0,
                    self._winVidX_1, self._winVidY_1, self._winVidW_1, self._winVidH_1,
                        mouse_stat_0, mouse_stat_1]

    
    def draw(self):
        #cvui.init(self._frame.name())
        self._frame[:] = (49, 52, 49)
        imageRet = self.imageSetting()
        illumRet = self.illumSetting()
        manRet = self.manipulSetting()
        camRet = self.camFrame()

        return [imageRet, illumRet, manRet, camRet]

    def return_values(self):
        
        mouse_status = [self._stat_0, self._stat_1, self._stat_2, self._stat_3, self._stat_4, self._stat_5, self._stat_6]
        wheel_step = [self.lg_inc, self.rg_inc, self.s_inc, self.x_inc, self.y_inc, self.z_inc, self.p_inc]

        return mouse_status, wheel_step

    def update_values(self, **kwargs): #  exp_t, pol_ang, pos_vals, inc_vals
        
        self._vals.update(kwargs)
        self._winIllTrk_0, self._winIllTrk_1 = [self._vals['exp_t']], [self._vals['pol_ang']]
        self._area_num = self._vals['area_num']
        #self._test_num = self._vals['test_num']
        [self.lg_pos, self.rg_pos, self.s_pos, self.x_pos, self.y_pos, self.z_pos, self.p_pos] = self._vals['pos_vals']
        [self.lg_inc, self.rg_inc, self.s_inc, self.x_inc, self.y_inc, self.z_inc, self.p_inc] = self._vals['inc_vals']



class RET:

    # Frames
    IMG = 0
    Ill = 1
    MAN = 2
    CAM = 3
    # Image frame/Buttons
    SAVE = 0
    REC = 1
    CROP = 2
    RULER = 3
    COUNT = 4
    # Image frame/Trackbars
    ZOOM = 5
    FOCUS = 6
    # Illumination frame/Checkboxes
    RED = 0
    GREEN = 1
    BLUE = 2
    # Illumination frame/Trackbars
    EXP_V = 3
    EXP_R = 4
    POL_V = 5
    POL_R = 6
    # Manipulation frame/Buttons
    TENSILE = 0
    STOP = 1
    MFA = 2
    UNIF = 3
    HELP = 4
    EXIT = 5
    # Manipulation frame/Checkboxes
    CYCLIC = 6
    STEP = 7
    CYCSTEP = 8
    DATA = 9
    MANUAL = 10
    # Manipulation frame/Mouse Pads
    LG = 0
    RG = 1
    S = 2
    X = 3
    Y = 4
    Z = 5
    P = 6
    # Camera frame/Positions
    VIDX_0 = 0
    VIDY_0 = 1
    VIDW_0 = 2
    VIDH_0 = 3
    VIDX_1 = 4
    VIDY_1 = 5
    VIDW_1 = 6
    VIDH_1 = 7
    STAT_0 = 8
    STAT_1 = 9
    #VIDEO = 10

