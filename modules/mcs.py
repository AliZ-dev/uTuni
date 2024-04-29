
import sys
import site
#sys.path.append(site.getsitepackages()[0] + "/smaract")
import smaract.ctl as ctl

"""
class ChannelState(enum.IntEnum):
        ACTIVELY_MOVING         = 0x00001
        CLOSED_LOOP_ACTIVE      = 0x00002
        CALIBRATING             = 0x00004
        REFERENCING             = 0x00008
        MOVE_DELAYED            = 0x00010
        SENSOR_PRESENT          = 0x00020
        IS_CALIBRATED           = 0x00040
        IS_REFERENCED           = 0x00080
        END_STOP_REACHED        = 0x00100
        RANGE_LIMIT_REACHED     = 0x00200
        FOLLOWING_LIMIT_REACHED = 0x00400
        MOVEMENT_FAILED         = 0x00800
        IS_STREAMING            = 0x01000
        POSITIONER_OVERLOAD     = 0x02000
        OVER_TEMPERATURE        = 0x04000
        REFERENCE_MARK          = 0x08000
        IS_PHASED               = 0x10000
        POSITIONER_FAULT        = 0x20000
        AMPLIFIER_ENABLED       = 0x40000
"""
class MCS():
    def __init__(self, locator):
   
        try:
            self._dhandle = ctl.Open(locator, "")
            print("MCS2 opened {}.".format(locator))
        except ctl.Error as e:
            # Passing an error code to "GetResultInfo" returns a human readable string
            # specifying the error.
            print("MCS2 {}: {}, error: {} (0x{:04X}) in line: {}. Press return to exit."
                .format(e.func, ctl.GetResultInfo(e.code), ctl.ErrorCode(e.code).name, e.code, (sys.exc_info()[-1].tb_lineno)))

        except Exception as ex:
            print("Unexpected error: {}, {} in line: {}".format(ex, type(ex), (sys.exc_info()[-1].tb_lineno)))
            raise

    def dHandle(self):
        return self._dhandle

    def close(self):
        try:
            ctl.Close(self._dhandle)
        except:
            pass
        print("MCS2 close.")
        print("*******************************************************")

class Axis():
    def __init__(self, dhandle, channel):
        self._dhandle = dhandle
        self._channel = channel
        self._step_size = 5000000 # 5 um
        self._speed = 8000000 # 8 um
        try:
        
        #except:
        #    print("MCS2 failed to open device. press any key to Exit.")
        #    input()
        #    exit(1)

            ch_type = ctl.GetProperty_i32(self._dhandle, channel, ctl.PropertyKey.CHANNEL_TYPE)
            if ch_type == ctl.ChannelModuleType.STICK_SLIP_PIEZO_DRIVER:
                # Set max closed loop frequency (maxCLF) to 6 kHz. This properties sets a limit for the maximum actuator driving frequency.
                # The maxCLF is not persistent thus set to a default value at startup.
                ctl.SetProperty_i32(self._dhandle, channel, ctl.PropertyKey.MAX_CL_FREQUENCY, 6000)
                # The hold time specifies how long the position is actively held after reaching the target.
                # This property is also not persistent and set to zero by default.
                # A value of 0 deactivates the hold time feature, a value of INFINITE (0xffffffff) sets the time to infinite.
                # (Until manually stopped by "Stop") Here we set the hold time to 1000 ms.
                ctl.SetProperty_i32(self._dhandle, channel, ctl.PropertyKey.HOLD_TIME, 1000)
            elif ch_type == ctl.ChannelModuleType.MAGNETIC_DRIVER:
                # Enable the amplifier (and start the phasing sequence).
                ctl.SetProperty_i32(self._dhandle, channel, ctl.PropertyKey.AMPLIFIER_ENABLED, ctl.ENABLED)

            # The move mode states the type of movement performed when sending the "Move" command.
            self._move_mode = ctl.MoveMode.CL_RELATIVE       
            ctl.SetProperty_i32(self._dhandle, channel, ctl.PropertyKey.MOVE_MODE, self._move_mode)
            ctl.SetProperty_i64(self._dhandle, self._channel, ctl.PropertyKey.MOVE_VELOCITY, self._speed)
            print("MCS2 set closed-loop relative move mode.")

        except ctl.Error as e:
            # Passing an error code to "GetResultInfo" returns a human readable string
            # specifying the error.
            print("MCS2 {}: {}, error: {} (0x{:04X}) in line: {}. Press return to exit."
                .format(e.func, ctl.GetResultInfo(e.code), ctl.ErrorCode(e.code).name, e.code, (sys.exc_info()[-1].tb_lineno)))

        except Exception as ex:
            print("Unexpected error: {}, {} in line: {}".format(ex, type(ex), (sys.exc_info()[-1].tb_lineno)))
            raise

    def move_mode(self, mode):
        self._move_mode = mode
        try:   
            ctl.SetProperty_i32(self._dhandle, self._channel, ctl.PropertyKey.MOVE_MODE, self._move_mode)
            print('move mode changed to {}'.format(mode))
        except ctl.Error as e:
            # Passing an error code to "GetResultInfo" returns a human readable string
            # specifying the error.
            print("MCS2 {}: {}, error: {} (0x{:04X}) in line: {}. Press return to exit."
                .format(e.func, ctl.GetResultInfo(e.code), ctl.ErrorCode(e.code).name, e.code, (sys.exc_info()[-1].tb_lineno)))

        except Exception as ex:
            print("Unexpected error: {}, {} in line: {}".format(ex, type(ex), (sys.exc_info()[-1].tb_lineno)))
            raise
    def get_position(self):
        try:
            position = ctl.GetProperty_i64(self._dhandle, self._channel, ctl.PropertyKey.POSITION)
            #print("MCS2 position: {} pm.".format(position))
            return position
        except ctl.Error as e:
            # Passing an error code to "GetResultInfo" returns a human readable string
            # specifying the error.
            print("MCS2 {}: {}, error: {} (0x{:04X}) in line: {}. Press return to exit."
                .format(e.func, ctl.GetResultInfo(e.code), ctl.ErrorCode(e.code).name, e.code, (sys.exc_info()[-1].tb_lineno)))

        except Exception as ex:
            print("Unexpected error: {}, {} in line: {}".format(ex, type(ex), (sys.exc_info()[-1].tb_lineno)))
            raise
    
    def set_speed(self, speed = 8):
        self._speed = speed * 1000000
        # Set move velocity [in pm/s].
        try:
            ctl.SetProperty_i64(self._dhandle, self._channel, ctl.PropertyKey.MOVE_VELOCITY, self._speed)
            print('MCS2 changed speed to {} pm/s'.format(self._speed))
        except ctl.Error as e:
            # Passing an error code to "GetResultInfo" returns a human readable string
            # specifying the error.
            print("MCS2 {}: {}, error: {} (0x{:04X}) in line: {}. Press return to exit."
                .format(e.func, ctl.GetResultInfo(e.code), ctl.ErrorCode(e.code).name, e.code, (sys.exc_info()[-1].tb_lineno)))

        except Exception as ex:
            print("Unexpected error: {}, {} in line: {}".format(ex, type(ex), (sys.exc_info()[-1].tb_lineno)))
            raise
        
    def get_speed(self):
        return self._speed
    
    def move(self, displacement_size, direction = 0):
        try:
            # Set move mode depending properties for the next movement.
            #convert from um to pm
            self._step_size = int(displacement_size * 1000000)
            # Set move acceleration [in pm/s2].
            ctl.SetProperty_i64(self._dhandle, self._channel, ctl.PropertyKey.MOVE_ACCELERATION, 10000000000)
            # Specify relative position distance [in pm] and direction.
            if direction:
                self._step_size = -self._step_size
            print("MCS2 move channel {}, absolute: {} pm.".format(self._channel, self._step_size))
            # Start actual movement.
            ctl.Move(self._dhandle, self._channel, self._step_size, 0)
            #print('after ctl.move')
            # Note that the function call returns immediately, without waiting for the movement to complete.
            # The "ChannelState.ACTIVELY_MOVING" (and "ChannelState.CLOSED_LOOP_ACTIVE") in the channel state
            # can be monitored to determine the end of the movement.
        except ctl.Error as e:
            # Passing an error code to "GetResultInfo" returns a human readable string
            # specifying the error.
            print("MCS2 {}: {}, error: {} (0x{:04X}) in line: {}. Press return to exit."
                .format(e.func, ctl.GetResultInfo(e.code), ctl.ErrorCode(e.code).name, e.code, (sys.exc_info()[-1].tb_lineno)))

        except Exception as ex:
            print("Unexpected error: {}, {} in line: {}".format(ex, type(ex), (sys.exc_info()[-1].tb_lineno)))
            raise

    def stop(self):
        try:
            print("MCS2 stop channel: {}.".format(self._channel))
            ctl.Stop(self._dhandle, self._channel, 0)
        except ctl.Error as e:
            # Passing an error code to "GetResultInfo" returns a human readable string
            # specifying the error.
            print("MCS2 {}: {}, error: {} (0x{:04X}) in line: {}. Press return to exit."
                .format(e.func, ctl.GetResultInfo(e.code), ctl.ErrorCode(e.code).name, e.code, (sys.exc_info()[-1].tb_lineno)))

        except Exception as ex:
            print("Unexpected error: {}, {} in line: {}".format(ex, type(ex), (sys.exc_info()[-1].tb_lineno)))
            raise
    
    

    def eventRet(self):
        timeout = 3000
        event = ctl.GetEventInfo( ctl.GetEventInfo(self._dhandle, 3000) )
        return event

"""
class RET:
    EVENT = 0
"""
"""
def printMenu():
    print("*******************************************************")
    print("WARNING: make sure the positioner can move freely\n \
            without damaging other equipment!")
    print("*******************************************************")
    print("Enter command and return:")
    print("[?] print this menu")
    print("[c] calibrate")
    print("[f] find reference")
    print("[+] perform movement in positive direction")
    print("[-] perform movement in negative direction")
    print("[s] stop")
    print("[p] get current position")
    print("[0] set move mode: closed loop absolute move")
    print("[1] set move mode: closed loop relative move")
    print("[2] set move mode: open loop scan absolute*")
    print("[3] set move mode: open loop scan relative*")
    print("[4] set move mode: open loop step*")
    print("[5] set control mode: standard mode*")
    print("[6] set control mode: quiet mode*")
    print("  * not available for Magnetic Driver channels")
    print("[q] quit")

def calibrate(channel):
    print("MCS2 start calibration on channel: {}.".format(channel))
    # Set calibration options (start direction: forward)
    ctl.SetProperty_i32(d_handle, channel, ctl.PropertyKey.CALIBRATION_OPTIONS, 0)
    # Start calibration sequence
    ctl.Calibrate(d_handle, channel, 0)
    # Note that the function call returns immediately, without waiting for the movement to complete.
    # The "ChannelState.CALIBRATING" in the channel state can be monitored to determine
    # the end of the calibration sequence.

def findReference(channel):
    print("MCS2 find reference on channel: {}.".format(channel))
    # Set find reference options.
    # The reference options specify the behavior of the find reference sequence.
    # The reference flags can be ORed to build the reference options.
    # By default (options = 0) the positioner returns to the position of the reference mark.
    # Note: In contrast to previous controller systems this is not mandatory.
    # The MCS2 controller is able to find the reference position "on-the-fly".
    # See the MCS2 Programmer Guide for a description of the different modes.
    ctl.SetProperty_i32(d_handle, channel, ctl.PropertyKey.REFERENCING_OPTIONS, 0)
    # Set velocity to 1mm/s
    ctl.SetProperty_i64(d_handle, channel, ctl.PropertyKey.MOVE_VELOCITY, 1000000000)
    # Set acceleration to 10mm/s2.
    ctl.SetProperty_i64(d_handle, channel, ctl.PropertyKey.MOVE_ACCELERATION, 10000000000)
    # Start referencing sequence
    ctl.Reference(d_handle, channel, 0)
    # Note that the function call returns immediately, without waiting for the movement to complete.
    # The "ChannelState.REFERENCING" in the channel state can be monitored to determine
    # the end of the referencing sequence.

version = ctl.GetFullVersionString()
print("SmarActCTL library version: '{}'.".format(version))

locators = ["network:sn:MCS2-00000286", "network:sn:MCS2-00002502"]
"""