"""Driver class for SpaceMouse controller.

This class provides a driver support to SpaceMouse. (developed on mac os)
To set up a new SpaceMouse controller:
    1. Download and install driver from https://www.3dconnexion.com/service/drivers.html
    2. Install hidapi library through pip
       (make sure you run uninstall hid first if it is installed).
    3. Make sure SpaceMouse is connected before running the script
    4. (Optional) Based on the model of SpaceMouse, you might need to change the
       vendor id and product id that correspond to the device.

For Linux support, you can find open-source Linux drivers and SDKs online.
    See http://spacenav.sourceforge.net/

Credits: This driver class is based on the hardware_spacenav.py in robosuite (https://github.com/ARISE-Initiative/robosuite)
"""

import threading
import time
import collections
import pprint
try:
    import hid
except ModuleNotFoundError as exc:
    raise ImportError(
        "Unable to load module hid, required to interface with SpaceMouse. "
        "Only macOS is officially supported. Install the additional "
        "requirements with `pip install -r requirements-extra.txt`"
    ) from exc

class SpaceMouse():
    """
    Polls spacemouse in the backgroud and maintain latest values
    """
    # Cached client that is shared for the application lifetime.
    _SPACEMOUSE_CLIENT = None
    def __init__(self, vendor_id:int=1133, product_id:int=50726,):
        """
        Connect to the SpaceMouse

        Args:
            vendor_id (int): device vendor_id
            product_id (int): device product_id
        """
        if self._SPACEMOUSE_CLIENT is None:
            print("Opening SpaceMouse device")
            try:
                self.device = hid.device()
            except:
                for device in hid.enumerate():
                    if device.product_string == 'Space Navigator':
                        print(device)
                print(f"Can't find device using vendor_id={vendor_id}, product_id={product_id}. Search the devices printed about for correct configurations")
                quit()
            self.device.open(vendor_id, product_id)  # SpaceMouse
            print("Manufacturer: %s" % self.device.get_manufacturer_string())
            print("Product: %s" % self.device.get_product_string())
            self.start_listener()
        else:
            print("Connection to SpaceMouse exists. Using prior connection")
        self.sensor_data = collections.OrderedDict({
            'x':0, 'y':0, 'z':0,
            'roll':0, 'pitch':0, 'yaw':0,
            'left':False, 'right':False,
            'is_new':True, 'time':0})

    def okay(self):
        if (self._SPACEMOUSE_CLIENT is None):
            return False
        else:
            return True

    def start_listener(self):
            # start polling data
            self.read_thread = threading.Thread(target=self.poll_sensors, args=())
            self.read_thread.daemon = True
            self.read_thread.start()

    def poll_sensors(self):
        print("Start polling SpaceMouse sensor data")
        self.poll = True
        while self.poll:
            self.read_sensor()
        print("Finished polling SpaceMouse sensor data")


    def normalize(self, sensor_data, scale=1.0/350, min_val=-1, max_val=1):
        def normalizse_val(val):
            val = val*scale
            val = min(max(val, min_val), max_val)
            return val

        sensor_data['x'] = normalizse_val(sensor_data['x'])
        sensor_data['y'] = normalizse_val(sensor_data['y'])
        sensor_data['z'] = normalizse_val(sensor_data['z'])
        sensor_data['roll'] = normalizse_val(sensor_data['roll'])
        sensor_data['pitch'] = normalizse_val(sensor_data['pitch'])
        sensor_data['yaw'] = normalizse_val(sensor_data['yaw'])
        return sensor_data

    def bytes2int16(self, y1, y2):
        """
        Convert two 8 bit bytes to a signed 16 bit integer.

        Args:
            y1 (int): 8-bit byte
            y2 (int): 8-bit byte

        Returns:
            int: 16-bit integer
        """
        x = (y1) | (y2 << 8)
        if x >= 32768:
            x = -(65536 - x)
        return x


    def read_sensor(self):
        """
        Read the device once and update the sensor_data
        """
        data = self.device.read(13)
        if data is not None:
            if data[0] == 1: # readings from 6-DoF sensor
                self.sensor_data['x'] = self.bytes2int16(data[1], data[2])
                self.sensor_data['y'] = self.bytes2int16(data[3], data[4]) * -1.0
                self.sensor_data['z'] = self.bytes2int16(data[5], data[6]) * -1.0
                # print("{:.2f}, {:.2f}, {:.2f}".format(self.x, self.y, self.z))

            elif data[0] == 2: # readings from 6-DoF sensor
                self.sensor_data['roll'] = self.bytes2int16(data[1], data[2])
                self.sensor_data['pitch'] = self.bytes2int16(data[3], data[4])* -1.0
                self.sensor_data['yaw'] = self.bytes2int16(data[5], data[6])* -1.0
                # print("{:.2f}, {:.2f}, {:.2f}".format(self.roll, self.pitch, self.yaw))

            elif data[0] == 3:  # readings from the side buttons
                # clear buttons
                if data[1] == 0:
                    self.sensor_data['left'] = False
                    self.sensor_data['right'] = False
                # press left button
                elif data[1] == 1:
                    self.sensor_data['left'] = True
                # press right button
                elif data[1] == 2:
                    self.sensor_data['right'] = True

            self.sensor_data['time'] = time.time()
            self.sensor_data['is_new'] = True

    # get latest sensor value)
    def get_sensors(self, normalized=True, scale=1.0/350, min_val=-1, max_val=1):
        sen = self.sensor_data.copy()
        if normalized:
            sen = self.normalize(sen, scale, min_val, max_val)
        self.sensor_data['is_new'] = False
        return sen

    def apply_commands(self):
        raise NotImplementedError

    def close(self):
        if self.okay():
            self.poll = False
            self.read_thread.join() # wait for the thread to finish
            print("SpaceMouse {} Disconnected".format(self._SPACEMOUSE_CLIENT))
            self._SPACEMOUSE_CLIENT = None
        return True

    def __del__(self):
        self.close()

if __name__ == '__main__':
    sm = SpaceMouse()
    quit = False
    print("Press left button to stop")
    while not quit:
        sensor_data = sm.get_sensors(normalized=True)
        pprint.pprint(sensor_data)
        time.sleep(.25)
        if sensor_data['left'] == True:
            quit = True

    sm.close()