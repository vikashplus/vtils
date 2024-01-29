import threading
import time
from inputs import devices, get_gamepad

monitor_events = [  'ABS_X', 'ABS_Y',
                    'ABS_HAT0X', 'ABS_HAT0Y',
                    'ABS_RY', 'ABS_RX',
                    'BTN_EAST', 'BTN_WEST', 'BTN_NORTH', 'BTN_SOUTH',
                    'BTN_TL', 'BTN_TR',
                    'BTN_START', 'BTN_SELECT',
                    'BTN_THUMBL', 'BTN_THUMBR',
                    'BTN_MODE', # Home (XBox) menu button
                    "ABS_Z", 'ABS_RZ']

class GamePad():
    """
    Poll gamepad in the backgroud and maintain latest key status
    """
    # Cached client that is shared for the application lifetime.
    _GAMEPAD_CLIENT = None
    def __init__(self):
        if self._GAMEPAD_CLIENT is None:
            for device in devices:
                if device.name in ["Logitech Gamepad F710", "Microsoft X-Box 360 pad"]:
                    self._GAMEPAD_CLIENT = device
                    print("Gamepad {} found".format(device))
            if self._GAMEPAD_CLIENT is None:
                print("Gamepad not found. Check connection")
                quit()
            else: # start the listener
                self.start_listener()
        else:
            print("Connection to Gamepad exists")
        self.sensor_data = {}
        for items in monitor_events:
            self.sensor_data[items] = 0
        self.sensor_data['is_new'] = True

    def okay(self):
        if (self._GAMEPAD_CLIENT is None):
            return False
        else:
            return True

    def start_listener(self):
            # start polling data
            self.read_thread = threading.Thread(target=self.poll_sensors, args=())
            self.read_thread.start()

    def poll_sensors(self):
        print("Start polling gamepad sensor data")
        self.poll = True
        while self.poll:
            self.read_sensor()
        print("Finished polling gamepad sensor data")

    def read_sensor(self):
        events = self._GAMEPAD_CLIENT.read()
        
        for event in events:
            if event.code in monitor_events:
                self.sensor_data['is_new'] = True # mark addition of new data
                if event.code == 'ABS_RX' or event.code == 'ABS_RY':
                    self.sensor_data[event.code] = event.state/32767.0
                elif event.code == 'ABS_X' or event.code == 'ABS_Y':
                    self.sensor_data[event.code] = event.state/32767.0
                elif event.code == 'ABS_RZ' or event.code == "ABS_Z":
                    self.sensor_data[event.code] = event.state/255.0
                else:
                    self.sensor_data[event.code] = event.state
            # else:
            #     print(event.ev_type, event.code, event.state)
            #     import ipdb; ipdb.set_trace()

    # get latest sensor value)
    def get_sensors(self):
        sen = self.sensor_data.copy()
        self.sensor_data['is_new'] = False
        return sen

    def apply_commands(self):
        raise NotImplementedError

    def close(self):
        if self.okay():
            self.poll = False
            self.read_thread.join() # wait for the thread to finish
            print("GamePad {} Disconnected".format(self._GAMEPAD_CLIENT))
            self._GAMEPAD_CLIENT = None
        return True

    def __del__(self):
        self.close()

if __name__ == '__main__':
    pad = GamePad()
    quit = False
    while not quit:
        sensor_data = pad.get_sensors()
        print(sensor_data)
        time.sleep(.25)
        if sensor_data['BTN_EAST'] == 1:
            quit = True

    pad.close()