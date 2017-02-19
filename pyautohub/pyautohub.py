import websocket
import threading
import logging
import time
import json
import collections

from .apiws import APIErrorWS
from .resourcesws import DeviceWS

LOG = logging.getLogger(__name__)

class AutohubWS(object):


  def __init__(self, ip_addr, port):
    self._ws = None
    self._host = "ws://" + str(ip_addr) + ":" + str(port)
    self._ws_thread = None
    self.devices = {}
    self.func_map_ = collections.defaultdict(list)

  def start(self):
    self._ws_thread = threading.Thread(target=self.run_ws_loop,
                                       name='AutohubWS Events Loop')
    self._ws_thread.daemon = True
    self._ws_thread.start()

  def stop(self):
    self._ws.close()
    self.join()
    LOG.info("AutohubWS Threads terminated")

  def on_device_added(self, callback):
      self.func_map_["OnDeviceAdded"].append(callback)

  def getDeviceFromAddress(self, device_address):
      return self.devices[device_address]
	  
  def on_message(self, ws, message):
      LOG.info("AutohubWS - incoming\r\n %s" ,message)
      list = json.loads(message)
      if list['event'] == 'deviceList':
        self.on_deviceList(list)
      elif list['event'] == 'deviceUpdate':
        self.on_deviceUpdate(list)

  def on_deviceUpdate(self, data):
      device = DeviceWS(self, data)
      if device.device_address_ not in self.devices:
        self.devices[device.device_address_] = device
        self.OnDeviceAdded(device)
      else:
        self.devices[device.device_address_]._properties_ = device._properties_
        self.devices[device.device_address_].OnUpdate()

  def on_deviceList(self, list):
      for data in list['devices']:
        device = DeviceWS(self,data)
        if device.device_address_ not in self.devices:
          self.devices[device.device_address_] = device
          self.OnDeviceAdded(device)

  def on_error(self, ws, error):
      LOG.info("AutohubWS error: %s", error)

  def on_close(self, ws):
      LOG.info("AutohubWS connection closed")

  def on_open(self, args):
    self._ws.send('{\r\n"event" : "getDeviceList"\r\n}\r\n')
    LOG.info("AuothubWS - connected to server")

  def join(self):
      self._ws_thread.join()

  def OnDeviceAdded(self, device):
      for callback in self.func_map_.get("OnDeviceAdded",()):
          callback(device)

  def run_ws_loop(self):
    self._ws = websocket.WebSocketApp(self._host,
                                on_message = self.on_message,
                                on_error = self.on_error,
                                on_close = self.on_close)

    self._ws.on_open = self.on_open
    self._ws.run_forever()
    LOG.info("run_ws_loop")
