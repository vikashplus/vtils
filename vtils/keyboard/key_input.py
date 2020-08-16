# Non Blocking keyboard listener
# based on https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard
# Running pynput over SSH generally will not work: https://pynput.readthedocs.io/en/latest/limitations.html
#   Workaround: The environment variable $DISPLAY must be set
#   example:: DISPLAY=:0 python key_input.py (this will capture events from keyboard directly connect to the remote machine)


from pynput import keyboard
import time

_VERBOSE = False

def prompt(msg):
    if _VERBOSE:
        print(msg)


class Key():
    def __init__(self):
        self.key = None

        # non-blocking listener
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.listener.start()
        print("Keyboard listener: Started")

    def on_press(self, key):
        try:
            prompt('alphanumeric key {0} pressed'.format(key.char))
            self.key = key.char
        except AttributeError:
            prompt('special key {0} pressed'.format(key))
            self.key = key.name

    def on_release(self, key):
        # print('{0} released'.format(key))
        self.key = None
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    def get_sensor(self):
        return self.key

    def close(self):
        self.listener.stop()
        self.listener.join()
        print("Keyboard listener: Closed")


if __name__ == '__main__':
    ky = Key()
    sen = None
    print("Press 'q' to stop listening")
    while sen != 'q':
        sen = ky.get_sensor()
        if sen is not None:
            print(sen, end=", ", flush=True)
        time.sleep(.01)
        
    ky.close()