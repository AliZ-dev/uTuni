#!~/programs/anaconda3/envs/ocv/bin/python3.8
import os
import sys
from modules.mfa_calib import image_scan
import numpy as np
from threading import Thread
#import multiprocessing
sys.path.append("./modules") 
from layout import Frame, RET
from experiment import Tensile, MFA
import initialize
from manual import Manual, ImgTools
import cv2
import cvui
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import imageio
import mccdaq
from cam import idsCam
from mfa_calib import image_scan
import time
import csv
from datetime import datetime as dt


class FLAGS:
    thread = False
    tensile = False
    mfa = False
    manual = False
    color = True
    force_control = False
    #plot = False
    


def main():
    save_path = str()
    print(os.getcwd())
    

    frame = Frame()
    pol_step = 45
    tuniPol = initialize.Polarizer(start_angle = -109, end_angle = 26, step_angle = pol_step) # 3 * 180 degrees
    tuniMFA = MFA(polarizer=tuniPol, pol_step=pol_step)
    stepPerDegree = 80
    tuniAct = initialize.Actuator()
    manualMove = Manual(frame, tuniAct)
    forceData = mccdaq.Data()
    flag = FLAGS
    cvui.init(frame.name())

    topCamera = idsCam(0)
    topCamera.set_exposure(exp_time = 40)

    
    video_rec_flag = False
    video_side_flag = False

    imageTools = ImgTools(frame)
    imgScan = image_scan()
   
    TEST_NUM = 0
    COPY_NUM = 0
    #VIDEO_NUM = 16
    #print('before while')
    time.sleep(5)
    frame.update_values(test_num = TEST_NUM, exp_t = topCamera.get_exposure(), pol_ang = tuniPol.rotor.get_position() / stepPerDegree)
    while True: # The CVUI window should be run through an infinite while loop in th main thread
        frameRet = frame.draw()
        H = int( frameRet[RET.CAM][RET.VIDH_0] * imageTools.zoom ) - 20
        W = int( frameRet[RET.CAM][RET.VIDW_0] * imageTools.zoom )
        SCALE = (topCamera._width / W, topCamera._height / H)
        TEST_NUM = int( frameRet[RET.IMG][RET.COUNT])
        tensile_mode = "normal" # alternatives: normal fatigue
        left_click = cvui.mouse(cvui.LEFT_BUTTON, cvui.CLICK)
        right_click = cvui.mouse(cvui.RIGHT_BUTTON, cvui.CLICK)
        #print(left_click)

        videoTop = topCamera.grab()
        videoTopFrame = videoTop
        videoTop = cv2.resize(videoTop, ( W, H ))
        if (frameRet[RET.IMG][RET.RULER]): # The ruler checkbox is checked here, then the pixel size and line angle could be measured by clicking on the camera-view
            videoTop = imageTools.measure(video_frame = videoTop, layoutRet = frameRet, left_stat = left_click, right_stat = right_click, scale = SCALE)

        cvui.image(frame.content(), frameRet[RET.CAM][RET.VIDX_0], frameRet[RET.CAM][RET.VIDY_0] + 20,
                    videoTop[ imageTools.top:imageTools.bottom, imageTools.left:imageTools.right])

        cvui.imshow(frame.name(), frame.content())        
        #cvui.text(frame.content(), frame._winManChkX_0, frame._winManChkY_2+10, "Test # {}".format(TEST_NUM))
        if (frameRet[RET.IMG][RET.CROP]):# The Zoom checkbox is checked here, then the ROI crop of the camera-view could be changes by scrolling on the view
            imageTools.roi(frameRet)
            frame.update_values(zoom = imageTools.zoom)


        if (frameRet[RET.MAN][RET.MANUAL]):
            manualMove.update()
        # Incomplete part for including the side-view camera:
        """
        if (frameRet[RET.IMG][RET.SIDE]):
            if not video_side_flag:
                sideCamera = idsCam(1)
                video_side_flag = True
            print("What do you think?")
            videoSide = sideCamera.grab()
            videoSide = cv2.resize(videoSide, ( frameRet[RET.CAM][RET.VIDW_1], frameRet[RET.CAM][RET.VIDH_1] - 20 ))
            cvui.image(frame.content(), frameRet[RET.CAM][RET.VIDX_1], frameRet[RET.CAM][RET.VIDY_1] + 20, videoSide)
        elif (video_side_flag):
            print("Close Side View")
            sideCamera._clean()
            del sideCamera
            video_side_flag = False
        """
        if (frameRet[RET.Ill][RET.RED]): color = "r"
        if (frameRet[RET.Ill][RET.GREEN]): color = "g"
        if (frameRet[RET.Ill][RET.BLUE]): color = "b"

        if (frameRet[RET.IMG][RET.SAVE]):
            #save_path = os.getcwd().replace("/script", "/data/") + str(dt.now())[:-7].replace(":", ".") + ".tiff"
            save_path = os.getcwd().replace("/script", "/data/IMG_R_") + str(TEST_NUM).zfill(4) + ".tiff"
            save_path_G = os.getcwd().replace("/script", "/data/IMG_G_") + str(TEST_NUM).zfill(4) + ".tiff"
            save_path_B = os.getcwd().replace("/script", "/data/IMG_B_") + str(TEST_NUM).zfill(4) + ".tiff"
            while True:
                    if os.path.isfile(save_path):
                        save_path = os.getcwd().replace("/script", "/data/IMG_") + str(TEST_NUM).zfill(4) + '_(' + str(COPY_NUM) + ").tiff"
                        COPY_NUM += 1
                    else:
                        COPY_NUM = 0
                        break
            print(save_path)
            imageio.imwrite(save_path, videoTopFrame[:,:,0])
            imageio.imwrite(save_path_G, videoTopFrame[:,:,1])
            imageio.imwrite(save_path_B, videoTopFrame[:,:,2])
            #cv2.imwrite(save_path, videoTop)
            print("saved")
            print(W)
            print(H)
        if (frameRet[RET.MAN][RET.UNIF]):
            #save_path = os.getcwd().replace("/script", "/data/") + str(dt.now())[:-7].replace(":", ".") + ".tiff"
            Hline = int(videoTopFrame.shape[0]/2)
            Vline = int(videoTopFrame.shape[1]/2)
            print(np.shape(videoTopFrame[Hline-50:Hline+50,:,:]))
            save_path = os.getcwd().replace("/script", "/data/") + "uniformity.tiff"
            mean_out = imgScan.mean_walk( input=cv2.cvtColor(videoTopFrame[Hline-100:Hline+100,:,:], cv2.COLOR_BGR2GRAY) ) #[Hline-40:Hline+40,0:Vline,:]
            print(np.shape(mean_out))
            imgScan.uniformity(input=mean_out)
            print("saved")

        if (frameRet[RET.IMG][RET.REC]):
            print("REC = True!")
            if not video_rec_flag:
                #VIDEO_NUM += 1
                video_path = os.getcwd().replace("/script", "/data/")\
                                 + "video_" + str(TEST_NUM).zfill(4) + ".avi"
                
                while True:
                    if os.path.isfile(video_path):
                        video_path = os.getcwd().replace("/script", "/data/")\
                                    + "video_" + str(TEST_NUM).zfill(4) + '_(' + str(COPY_NUM) + ").avi"
                        COPY_NUM += 1
                    else:
                        COPY_NUM = 0
                        break


                # str(dt.now())[:-4].replace(":", ".")
                #  str(VIDEO_NUM)
                # cv2.VideoWriter_fourcc('X','V','I','D')
                video_out_0 = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc('M','P','E','G'),\
                                                     40, ( frameRet[RET.CAM][RET.VIDW_0], (frameRet[RET.CAM][RET.VIDH_0]-20) ) ) # 400, 300 / 
                video_rec_flag = True
            video_out_0.write(videoTop)
        elif (video_rec_flag):
            video_out_0.release()
            video_rec_flag = False

        if (frameRet[RET.Ill][RET.EXP_R]):  
            topCamera.set_exposure(float(frameRet[RET.Ill][RET.EXP_V][0]))
            frame.update_values(exp_t = frameRet[RET.Ill][RET.EXP_V][0])

        if (frameRet[RET.Ill][RET.POL_R]):
            tuniPol.rotor.move(position=frameRet[RET.Ill][RET.POL_V][0] * stepPerDegree)
            frame.update_values(pol_ang = frameRet[RET.Ill][RET.POL_V][0])
            

        if ((not flag.tensile) and (not flag.mfa) and frameRet[RET.MAN][RET.MFA]):
            tuniPol.rotor.move(position=tuniPol.start)
            flag.mfa = True
        
        if flag.mfa: flag.mfa = tuniMFA.run( videoTopFrame )

        if (frameRet[RET.MAN][RET.CYCLIC]): tensile_mode = "cyclic"
        if (frameRet[RET.MAN][RET.STEP]): tensile_mode = "stepwise"
        if (frameRet[RET.MAN][RET.CYCSTEP]): tensile_mode = "cyclic_stepwise"

        if ((not flag.tensile) and frameRet[RET.MAN][RET.TENSILE]):
            flag.tensile = True
            #TEST_NUM += 1
            tuniTensile = Tensile(tuniAct.x_axis, forceData)
            if tensile_mode == "normal": tuniTensile.normal()
            if tensile_mode == "cyclic" or tensile_mode == "fatigue": tuniTensile.cyclic()
            if tensile_mode == "stepwise": tuniTensile.stepwise()
            if tensile_mode == "cyclic_stepwise": tuniTensile.cyclic_stepwise()
            #print(tensile_mode)
            try:
                data_thread = Thread(target=tuniTensile.write_data, args = (flag, TEST_NUM))
                data_thread.start()
                tensile_thread = Thread(target=tuniTensile.run, args = (tensile_mode, flag))
                tensile_thread.start()
                flag.thread = True
            except:
                print("Error: unable to start thread")
        # Incomplete part for force-controlled movements:
        #if (frameRet[RET.IMG][RET.FORCE]): 
        #    if not flag.plot:
        #        chart = []
        #        flag.plot = True
        #    chart.append(forceData.read())    
        #else: flag.plot = False
        
        if (frameRet[RET.MAN][RET.DATA]):

            image_path = os.getcwd().replace("/script", "/data/") + str(TEST_NUM).zfill(4) + ".tiff"
            while True:
                    if os.path.isfile(image_path):
                        image_path = os.getcwd().replace("/script", "/data/") + str(TEST_NUM).zfill(4) + '_(' + str(COPY_NUM) + ").tiff"
                        COPY_NUM += 1
                    else:
                        COPY_NUM = 0
                        break
            print(save_path)
            imageio.imwrite(image_path, videoTopFrame[:,:,0])        
            filename = os.getcwd().replace("/script", "/data/") + "data_" + str(TEST_NUM).zfill(4) + ".csv"
            while True:
                    if os.path.isfile(filename):
                        filename = os.getcwd().replace("/script", "/data/") + "data_" + str(TEST_NUM).zfill(4) + '_(' + str(COPY_NUM) + ").csv"
                        COPY_NUM += 1
                    else:
                        COPY_NUM = 0
                        break
            with open(filename, 'a') as csvfile: 
                writer = csv.writer(csvfile, delimiter=',')
                mydata = [str(dt.now())[:-2].replace(":", "."), str(TEST_NUM).zfill(4), tuniAct.x_axis.get_position() , forceData.read()]
                ###################################################################### "=>tuniAct.lg_axis.get_position(), tuniAct.rg_axis.get_position(), 
                writer.writerow(mydata)
            #TEST_NUM += 1
            #frame.update_values(test_num = TEST_NUM)

        if (frameRet[RET.MAN][RET.STOP]):
            flag.mfa = False
            tuniPol.rotor.move(position=tuniPol.start)
            flag.tensile = False
            tuniAct.x_axis.stop()

        #if flag.tensile: flag.tensile = tuniTensile.run(tensile_mode, flag)

        if (frameRet[RET.MAN][RET.EXIT]):
            #cap.release()            
            break

        if cv2.waitKey(5) & 0xFF == ord('q'):
            #cap.release()
            break
    if (flag.thread):
        data_thread.join()
        tensile_thread.join()

    cv2.destroyAllWindows()
    tuniAct.close()
    tuniPol.rotor.Release()
    topCamera.release()

    

if __name__ == "__main__":
    main()
    print('after main')
    exit(0)
    print('after exit')