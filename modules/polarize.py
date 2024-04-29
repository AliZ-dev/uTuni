from ctypes import *
import time
import os
import sys
import platform
import tempfile
import re

try: 
    from pyximc import *
except ImportError as err:
    print ("Can't import pyximc module. The most probable reason is that you changed the relative location of the testpython.py and pyximc.py files. See developers' documentation for details.")
    exit()
except OSError as err:
    # print(err.errno, err.filename, err.strerror, err.winerror) # Allows you to display detailed information by mistake.
    if platform.system() == "Windows":
        if err.winerror == 193:   # The bit depth of one of the libraries bindy.dll, libximc.dll, xiwrapper.dll does not correspond to the operating system bit.
            print("Err: The bit depth of one of the libraries bindy.dll, libximc.dll, xiwrapper.dll does not correspond to the operating system bit.")
            # print(err)
        elif err.winerror == 126: # One of the library bindy.dll, libximc.dll, xiwrapper.dll files is missing.
            print("Err: One of the library bindy.dll, libximc.dll, xiwrapper.dll is missing.")
            # print(err)
        else:           # Other errors the value of which can be viewed in the code.
            print(err)
        print("Warning: If you are using the example as the basis for your module, make sure that the dependencies installed in the dependencies section of the example match your directory structure.")
        print("For correct work with the library you need: pyximc.py, bindy.dll, libximc.dll, xiwrapper.dll")
    else:
        print(err)
        print ("Can't load libximc library. Please add all shared libraries to the appropriate places. It is decribed in detail in developers' documentation. On Linux make sure you installed libximc-dev package.\nmake sure that the architecture of the system and the interpreter is the same")
    exit()

if sys.version_info >= (3,0):
    import urllib.parse


class Rotor():
    def __init__(self):
        print("Hi")
        #cur_dir = os.path.abspath(os.path.dirname(__file__)) # Specifies the current directory.
        root_dir = os.path.join(os.getcwd(), "..")
        ximc_package_dir = os.getcwd() # Specifies the current directory.
        sys.path.append(ximc_package_dir)  # add pyximc.py wrapper to python path

        if platform.system() == "Windows":
            # Determining the directory with dependencies for windows depending on the bit depth.
            arch_dir = "ximc_win64"# if "64" in platform.architecture()[0] else "win32" # 
            libdir = os.path.join(root_dir, "lib", arch_dir)
            os.environ["Path"] = libdir + ";" + os.environ["Path"] # add dll path into an environment variable

            # variable 'lib' points to a loaded library
        
        # note that ximc uses stdcall on win
        self._lib = ximc_shared_lib()
        print("Library loaded")

        sbuf = create_string_buffer(64)
        self._lib.ximc_version(sbuf)
        print("Library version: " + sbuf.raw.decode().rstrip("\0"))

        # Set bindy (network) keyfile. Must be called before any call to "enumerate_devices" or "open_device" if you
        # wish to use network-attached controllers. Accepts both absolute and relative paths, relative paths are resolved
        # relative to the process working directory. If you do not need network devices then "set_bindy_key" is optional.
        # In Python make sure to pass byte-array object to this function (b"string literal").
        self._lib.set_bindy_key(os.path.join(root_dir, "win32", "keyfile.sqlite").encode("utf-8"))

        # This is device search and enumeration with probing. It gives more information about devices.
        probe_flags = EnumerateFlags.ENUMERATE_PROBE + EnumerateFlags.ENUMERATE_NETWORK
        enum_hints = b"addr=192.168.0.1,172.16.2.3"
        # enum_hints = b"addr=" # Use this hint string for broadcast enumerate
        devenum = self._lib.enumerate_devices(probe_flags, enum_hints)
        print("Device enum handle: " + repr(devenum))
        print("Device enum handle type: " + repr(type(devenum)))

        dev_count = self._lib.get_device_count(devenum)
        print("Device count: " + repr(dev_count))

        controller_name = controller_name_t()
        for dev_ind in range(0, dev_count):
            enum_name = self._lib.get_device_name(devenum, dev_ind)
            result = self._lib.get_enumerate_device_controller_name(devenum, dev_ind, byref(controller_name))
            if result == Result.Ok:
                print("Enumerated device #{} name (port name): ".format(self._dev_ind) + repr(enum_name) +\
                                ". Friendly name: " + repr(controller_name.ControllerName) + ".")

        open_name = "xi-com:///dev/ximc/000049E8" #None xi-com:///./COM5
        #if len(sys.argv) > 1:
        #    open_name = sys.argv[1]
        #elif dev_count > 0:
        #    open_name = self._lib.get_device_name(devenum, 0)
        #elif sys.version_info >= (3,0):
            # use URI for virtual device when there is new urllib python3 API
        #    tempdir = tempfile.gettempdir() + "/testdevice.bin"
        #    if os.altsep:
        #        tempdir = tempdir.replace(os.sep, os.altsep)
            # urlparse build wrong path if scheme is not file
        #    uri = urllib.parse.urlunparse(urllib.parse.ParseResult(scheme="file", \
        #            netloc=None, path=tempdir, params=None, query=None, fragment=None))
        #    open_name = re.sub(r'^file', 'xi-emu', uri).encode()

        if not open_name:
            exit(1)

        if type(open_name) is str:
            open_name = open_name.encode()

        print("\nOpen device " + repr(open_name))
        self._device_id = self._lib.open_device(open_name)
        print("Device id: " + repr(self._device_id))

    def get_info(self):
        lib=self._lib
        device_id=self._device_id
        print("\nGet device info")
        x_device_information = device_information_t()
        result = lib.get_device_information(device_id, byref(x_device_information))
        print("Result: " + repr(result))
        if result == Result.Ok:
            print("Device information:")
            print(" Manufacturer: " +
                    repr(string_at(x_device_information.Manufacturer).decode()))
            print(" ManufacturerId: " +
                    repr(string_at(x_device_information.ManufacturerId).decode()))
            print(" ProductDescription: " +
                    repr(string_at(x_device_information.ProductDescription).decode()))
            print(" Major: " + repr(x_device_information.Major))
            print(" Minor: " + repr(x_device_information.Minor))
            print(" Release: " + repr(x_device_information.Release))

    def get_status(self):
        lib=self._lib
        device_id=self._device_id
        print("\nGet status")
        x_status = status_t()
        result = lib.get_status(device_id, byref(x_status))
        print("Result: " + repr(result))
        if result == Result.Ok:
            print("Status.Ipwr: " + repr(x_status.Ipwr))
            print("Status.Upwr: " + repr(x_status.Upwr))
            print("Status.Iusb: " + repr(x_status.Iusb))
            print("Status.Flags: " + repr(hex(x_status.Flags)))

    def get_position(self):
        lib=self._lib
        device_id=self._device_id
        print("\nRead position")
        x_pos = get_position_t()
        result = lib.get_position(device_id, byref(x_pos))
        print("Result: " + repr(result))
        if result == Result.Ok:
            print("Position: {0} steps, {1} microsteps".format(x_pos.Position, x_pos.uPosition))
        return int(x_pos.Position)

    def go_left(self):
        lib=self._lib
        device_id=self._device_id
        print("\nMoving left")
        result = lib.command_left(device_id)
        print("Result: " + repr(result))

    def move(self, position=300, uposition=0):
        lib=self._lib
        device_id=self._device_id
        print("\nGoing to {0} steps, {1} microsteps".format(position, uposition))
        result = lib.command_move(device_id, position, uposition)
        print("Result: " + repr(result))
    
    def shift(self, delta=400, udelta=0):
        lib=self._lib
        device_id=self._device_id
        print("\nShifting {0} steps, {1} microsteps".format(delta, udelta))
        result = lib.command_movr(device_id, delta, udelta)
        print("Result: " + repr(result))

    def wait_for_stop(self, interval):
        lib=self._lib
        device_id=self._device_id
        print("\nWaiting for stop")
        result = lib.command_wait_for_stop(device_id, interval)
        print("Result: " + repr(result))

    def get_serial(self):
        lib=self._lib
        device_id=self._device_id
        print("\nReading serial")
        x_serial = c_uint()
        result = lib.get_serial_number(device_id, byref(x_serial))
        if result == Result.Ok:
            print("Serial: " + repr(x_serial.value))

    def set_max_speed(self, max_speed=5000):
        lib=self._lib
        device_id=self._device_id
        print("\nSet engine settings")
        # Create move settings structure
        engst = engine_settings_t()
        # Get current move settings from controller
        result = lib.get_engine_settings(device_id, byref(engst))
        # Print command return status. It will be 0 if all is OK
        print("Read command result: " + repr(result))
        print("The speed was equal to {0}. We will change it to {1}".format(engst.NomSpeed, max_speed))
        # Change current speed
        engst.NomSpeed = (c_uint)(max_speed)#,max_speed,max_speed,max_speed,max_speed,max_speed,max_speed,max_speed,max_speed,max_speed)
        # Write new move settings to controller
        result = lib.set_engine_settings(device_id, byref(engst))
        # Print command return status. It will be 0 if all is OK
        print("Write command result: " + repr(result))
    
    def get_speed(self):
        lib=self._lib
        device_id=self._device_id
        print("\nGet speed")
        # Create move settings structure
        mvst = move_settings_t()
        # Get current move settings from controller
        result = lib.get_move_settings(device_id, byref(mvst))
        # Print command return status. It will be 0 if all is OK
        print("Read command result: " + repr(result))    
        
        return mvst.Speed
            
    def set_speed(self, speed=4000, accel=5000, decel=5000):
        lib=self._lib
        device_id=self._device_id
        print("\nSet speed")
        # Create move settings structure
        mvst = move_settings_t()
        
        # Get current move settings from controller
        result = lib.get_move_settings(device_id, byref(mvst))
        # Print command return status. It will be 0 if all is OK
        print("Read command result: " + repr(result))
        print("The speed was equal to {0}. We will change it to {1}".format(mvst.Speed, speed))
        # Change current speed
        mvst.Speed = (c_uint)(speed)
        # Set acceleration and deceleration values
        mvst.Accel = (c_uint)(accel)
        mvst.Decel = (c_uint)(decel)
        # Write new move settings to controller
        result = lib.set_move_settings(device_id, byref(mvst))
        print("Write command result: " + repr(result)) 
        mvst = move_settings_t()
        result = lib.get_move_settings(device_id, byref(mvst))
        # Print command return status. It will be 0 if all is OK
        print("Read command result: " + repr(result))
        print("The Acceleration is equal to {0}".format(mvst.Accel))
        # Print command return status. It will be 0 if all is OK

    def set_ustep_mode(self, mode=MicrostepMode.MICROSTEP_MODE_FULL):
        lib=self._lib
        device_id=self._device_id
        print("\nSet microstep mode to 256")
        # Create engine settings structure
        eng = engine_settings_t()
        # Get current engine settings from controller
        result = lib.get_engine_settings(device_id, byref(eng))
        # Print command return status. It will be 0 if all is OK
        print("Read command result: " + repr(result))
        # Change MicrostepMode parameter to MICROSTEP_MODE_FRAC_256
        # (use MICROSTEP_MODE_FRAC_128, MICROSTEP_MODE_FRAC_64 ... for other microstep modes)
        eng.MicrostepMode = mode
        # Write new engine settings to controller
        result = lib.set_engine_settings(device_id, byref(eng))
        # Print command return status. It will be 0 if all is OK
        print("Write command result: " + repr(result))    

    def set_up(self):
        self.get_info()
        self.set_max_speed(max_speed=4000)
        self.set_ustep_mode() # set the microstep to MICROSTEP_MODE_FULL (without microsteps)
        self.get_speed()
        self.set_speed(speed=4000, accel=4000, decel=8000)
        

    def Release(self):
        lib = self._lib
        device_id = self._device_id
        print("\nClosing")
        lib.close_device(byref(cast(device_id, POINTER(c_int))))
        print("Done")


"""
    get_info()
    get_status()
    set_ustep_mode()
    startpos, ustartpos = get_position()
    # first move
    go_left()
    time.sleep(3)
    get_position()
    # second move
    current_speed = get_speed()
    set_speed(speed=current_speed / 2)
    move(distance=10000, udistance=ustartpos) # startpos
    wait_for_stop(intervsl=100)
    get_status()
    get_serial()
"""
