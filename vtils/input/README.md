# Device configuration info

## Gamepad

### Linux

**Dependencies**

```bash
pip install inputs
```

Supported gamepads are:

- Logitech Gamepad F710
- Microsoft X-Box 360 pad

## Spacemouse

### macOS
To set up a new SpaceMouse controller:
1. Install hidapi library through pip (make sure you run uninstall hid first if it is installed).
2. Make sure SpaceMouse is connected before running the script
3. (Optional) Based on the model of SpaceMouse, you might need to change the vendor id and product id that correspond to the device.\n

### Linux

For Linux support, you can find open-source Linux drivers and SDKs online at http://spacenav.sourceforge.net/

**Dependencies**

Install `hidapi` on Linux to enable access to the spacemouse device using the `hid` API in Python.

```bash
pip install hidapi
```

Install and configure the open-source spacenav daemon `spnavd`:
```bash
# Installs spacenavd binary and service (open source)
git clone https://github.com/FreeSpacenav/spacenavd.git
cd spacenavd
./configure
make
sudo make install # Installs it to /usr/local/bin, so either softlink to your own bin, or add it to your PATH The required libraries and drivers forenv variable
```

Next, install the spacenav driver `libspnav`:
```bash
git clone https://github.com/FreeSpacenav/libspnav.git
cd libspnav
./configure
make
sudo make install # Installs it to /usr/local/bin, so either softlink to your own bin, or add it to your PATH env variable
```

Setup up udev rules to be able to access the spacenav daemon without requiring root permission:
```bash
# Created udev config file as follows:
## /etc/udev/rules.d/90-spacemouse.rules
SUBSYSTEM=="usb", ATTRS{idVendor}=="256f", ATTRS{idProduct}=="c635", MODE="0666"
KERNEL=="hidraw*",ATTRS{busnum}=="1", ATTRS{idVendor}=="256f", ATTRS{idProduct}=="c635", MODE="0666"
```
The above example uses the default Spacenav's Spacemouse _Vendor_ and _Product_ ID in hexadecimal, but make sure to double check that your spacemouse's vendor and product id match the content of the udev rules file with `lsusb` for example.

Make udev load the new rules (might require sudo permission):
```bash
udevadm control --reload-rules && udevadm trigger
```

Either manually start the `spnavd` daemon:
```bash
spnavd -v -d
```
or setup a service file:
```bash
### /etc/systemd/system/spacenavd.service
[Unit]
Description=Userspace Daemon of the spacenav driver.

[Service]
Type=forking
PIDFile=/var/run/spnavd.pid
Environment=XAUTHORITY=/run/user/1000/gdm/Xauthority
ExecStart=/usr/local/bin/spacenavd

[Install]
WantedBy=multi-user.target
```
then start / enable it with:
```bash
systemctl daemon-reload
systemctl enable --now spacenavd.service
```

Optionally, install the `spnavcfg` tool to check that the spacenav daemon and driver are properly working.
It is also useful to setup sensitivity and deadzone, although the settings do not seem to persist once the spacemouse is unplugged.
```bash
sudo apt-get install qt5-default # in case you get a qt5 dependency error
git clone https://github.com/FreeSpacenav/spnavcfg.git
cd spnavcfg
./configure
make
sudo make install # Installs it to /usr/local/bin, so either softlink to your own bin, or add it to your PATH env variable
```
With the spacemouse plugged in, execute `spnavcfg` to make sure that the device is properly detected.

It should now be possible to run Robohive's tele-operation tutorials with the spacemouse using:
```bash
python ee_teleop_multi.py --input_device spacemouse
```
