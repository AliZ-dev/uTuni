import spacenavigator
import time
import cv2



def main():

    success = spacenavigator.open()
    spacenavigator.describe_connection()
    if success:
        while 1:
            state = spacenavigator.read()
            print("X = {}, Y = {}, Z= {}, Roll= {}, Pitch= {}, YAW={}".format(\
                state.x, state.y, state.z, state.roll, state.pitch, state.yaw))
            time.sleep(0.2)
            #if (input('') == 'q'):
            #   break

if __name__ == '__main__':
    main()