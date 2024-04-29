
from pyueye import ueye
import numpy as np
import cv2
import sys



def adjust_gamma(image, gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)

class idsCam():

    def __init__(self, hCam = 0):
        self._hCam = hCam
        self._width = 2048   #2456 2048 2592 2448
        self._height = 2048  #2054 2048 2048 2048

    #def _init(self):
        self.hcam = ueye.HIDS(self._hCam)
        ret = ueye.is_InitCamera(self.hcam, None)
        print(f"initCamera returns {ret}")

        # set color mode
        ret = ueye.is_SetColorMode(self.hcam, ueye.IS_CM_BGR8_PACKED)
        print(f"SetColorMode IS_CM_BGR8_PACKED returns {ret}")

        # set region of interest
        width = self._width
        height = self._height
        rect_aoi = ueye.IS_RECT()
        rect_aoi.s32X = ueye.int(0)
        rect_aoi.s32Y = ueye.int(0)
        rect_aoi.s32Width = ueye.int(width)
        rect_aoi.s32Height = ueye.int(height)
        ret = ueye.is_AOI(self.hcam, ueye.IS_AOI_IMAGE_SET_AOI, rect_aoi, ueye.sizeof(rect_aoi))
        print(f"AOI IS_AOI_IMAGE_SET_AOI returns {ret}")

        sensor_info = ueye.SENSORINFO()
        ret = ueye.is_GetSensorInfo(self.hcam, sensor_info)
        print(f"is_GetSensorInfo returns {ret}")
        for info in sensor_info._fields_:
            print(info[0],eval("sensor_info.%s"%info[0]))

        #num_cam = ueye.c_int()
        #ueye.is_GetNumberOfCameras(num_cam)
        #print(f" is_GetNumberOfCameras  returns {ret}")
        #print(num_cam)

        
        

        value = ueye.c_double(0)
        return_value = ueye.c_double()
        ret = ueye.is_SetAutoParameter(self.hcam, ueye.IS_SET_ENABLE_AUTO_SHUTTER, value, return_value)
        print(f"AUTO_SHUTTER is_SetAutoParameter returns {ret}")

        value = ueye.c_double(0)
        return_value = ueye.c_double()
        ret = ueye.is_SetAutoParameter(self.hcam, ueye.IS_SET_AUTO_SHUTTER_MAX, value, return_value)
        print(f"SHUTTER_MAX is_SetAutoParameter returns {ret}")

        value = ueye.c_double(0)
        return_value = ueye.c_double()
        ret = ueye.is_SetAutoParameter(self.hcam, ueye.IS_SET_AUTO_GAIN_MAX, value, return_value)
        print(f"GAIN_MAX is_SetAutoParameter returns {ret}")

        value = ueye.c_double(0)
        return_value = ueye.c_double()
        ret = ueye.is_SetAutoParameter(self.hcam, ueye.IS_SET_ENABLE_AUTO_GAIN, value, return_value)
        print(f"AUTOGAIN is_SetAutoParameter returns {ret}")


        #exp_time = ueye.IS_EXP_TIME()
        master_gain = ueye.c_int(0)
        red_gain = ueye.c_int(0)
        green_gain = ueye.c_int(0)
        blue_gain = ueye.c_int(0)
        ret = ueye.is_SetHardwareGain(self.hcam, master_gain, red_gain, green_gain, blue_gain)
        print(f"GAIN is_SetHardwareGain returns {ret}")

        fps_in = ueye.c_double(20.0) #
        fps_out = ueye.c_double()
        ret = ueye.is_SetFrameRate(self.hcam, fps_in, fps_out)
        print(f"FrameRate is_SetFrameRate  returns {ret}")
        print("new FPS: {}".format(fps_out))

        #IS_PARAMETERSET_CMD_SAVE_FILE
        #ret = ueye.is_ParameterSet()
        

        

        # allocate memory
        self._mem_ptr = ueye.c_mem_p()
        mem_id = ueye.int()
        self._bitspixel = 24 # for colormode = IS_CM_BGR8_PACKED
        ret = ueye.is_AllocImageMem(self.hcam, width, height, self._bitspixel,
                                    self._mem_ptr, mem_id)
        print(f"AllocImageMem returns {ret}")
        
        # set active memory region
        ret = ueye.is_SetImageMem(self.hcam, self._mem_ptr, mem_id)
        print(f"SetImageMem returns {ret}")

        # continuous capture to memory
        ret = ueye.is_CaptureVideo(self.hcam, ueye.IS_DONT_WAIT)
        print(f"CaptureVideo returns {ret}")
        
        # get data from camera and display
        self._lineinc = width * int((self._bitspixel + 7) / 8)

        #return [mem_ptr, bitspixel, lineinc]

    def grab(self):
        
        mem_ptr, bitspixel, lineinc = self._mem_ptr , self._bitspixel, self._lineinc#self.__init__()
        width, height = self._width, self._height
        #print('before get_data')
        img = ueye.get_data(mem_ptr, width, height, bitspixel, lineinc, copy=True)
        #print('after get_data')
        img = np.reshape(img, (height, width, 3))
        #img = cv2.resize(img, (int(width*0.4), int(height*0.4)) )
        #img = adjust_gamma(img, 2.8)
        return img

    def get_exposure(self):

        current_exp_time = ueye.c_double()
        ret = ueye.is_Exposure(self.hcam, ueye.IS_EXPOSURE_CMD_GET_EXPOSURE, current_exp_time, 8)
        print(f"EXPOSURE IS_EXPOSURE_CMD_GET_EXPOSURE  returns {ret}")
        print(current_exp_time)

        return current_exp_time
        
    def set_exposure(self, exp_time):

        current_exp_time = self.get_exposure()

        exp_time = ueye.c_double(exp_time)
        ret = ueye.is_Exposure(self.hcam, ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, exp_time, 8) # ueye.sizeof(exp_time)
        print(f"EXPOSURE IS_EXPOSURE_CMD_SET_EXPOSURE  returns {ret}")
        print(exp_time)

        current_exp_time = self.get_exposure()

    def release(self):
        self.hcam = self._hCam
        # cleanup
        print(f"hCam = {self.hcam}")
        ret = ueye.is_StopLiveVideo(self.hcam, ueye.IS_FORCE_VIDEO_STOP)
        print(f"StopLiveVideo returns {ret}")
        ret = ueye.is_ExitCamera(self.hcam)
        print(f"ExitCamera returns {ret}")