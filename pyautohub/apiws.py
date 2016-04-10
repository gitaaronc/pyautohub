from urllib.parse import urlencode
import json
import sys
import requests
import time
import collections

class APIErrorWS(Exception):
    """API Error Response

    Attributes:
        msg -- the error message
        code -- the error code
    """
    def __init__(self, data):
        self.data = data

class AutohubResourceWS(object):
    def __init__(self, api, data=None):
        for data_key in self._properties:
            setattr(self, "_" + data_key, None)
        self._resource_id = None
        self._api_iface = api
        if data:
            self._update_details(data)
        else:
            self.reload_details

        self.func_map_ = collections.defaultdict(list)

    def on_device_update(self, callback):
        self.func_map_["OnUpdate"].append(callback)

    def OnUpdate(self):
        for callback in self.func_map_.get("OnUpdate",()):
            callback()

    def __getattr__(self, name):
        if name in self._properties:
            return getattr(self, "_"+name)
        else:
            raise AttributeError

    def __setattr__(self, name, value):
        if name in self._properties:
            if name in self._settables:
                self.__dict__["_"+name] = value
            else:
                raise "Property not settable"
        else:
            self.__dict__[name] = value

    def _update_details(self, data):
        #Intakes dict of details, and sets necessary properties in device
        for api_name in self._properties:
            if api_name in data:
                setattr(self, "_" + api_name, data[api_name])

    def reload_details(self):
        return

    def save(self):
        return

    @property
    def json(self):
        json_data = {}
        for attribute in self._properties:
            print(getattr(self, "_" + attribute))
            json_data[attribute] = getattr(self, "_" + attribute)
        return json.dumps(json_data)

class AutohubCommandableWS(AutohubResourceWS):
    def send_command(self, command, level=None):
        data = {
            'event' : 'device',
            'device_id': getattr(self, "device_address_"),
            'command': command
        }
        if level:
            data['command_two'] = level

        self._api_iface._ws.send(json.dumps(data))


