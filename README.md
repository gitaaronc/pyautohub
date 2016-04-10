pyAutohub
======
Lightweight Python 3 module to communication with Autohub Server.

Dependencies
------------
pyWeMo depends on Python package requests.
    - json
    - websocket-client
    
How to use
----------

    >> import pyautohub
    >> autohub = pyautohub.AutohubWS()
    >> autohub.start()
    This will make the initial connection to the Authub server and rerieve a list of devices.
    >> for k, v in autohub.devices.items():
    >>   print(v.device_address_)
    A list of device addresses will be printed to the screen. From this list you can use
    the addresses to call functions within the device object.
    >> autohub.devices[2547435].send_command('on',255)
    Replace "2547435" with one of your device addresses!
    The previous command will turn on the device to full power.
    >> autohub.devices[2547435].send_command('off')
    The previous command will turn off the device.
    
License
-------
  Written and copyright Aaron Coombs. Do with it what you like. Please share/commit your changes.
  Inspired by other people working on Home-Assistant.io
  
