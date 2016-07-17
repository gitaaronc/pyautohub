from .apiws import AutohubResourceWS, AutohubCommandableWS

class HouseWS(AutohubResourceWS):
    resource_name="houses"
    _settables = (
        'AutohubHubID', 'HouseName', 'City', 'DHCP', 'DaylightSavings'
    )
    _properties = (
        'AutohubHubID','HouseName','City','DHCP','DaylightSavings',
        'HubType','HubUsername','HubPassword','IP','Port','Gateway',
        'Mask','Mac','BinVer','PLMVer','FirmwareVer','HouseID','IconID'
    )

class AccountWS(AutohubResourceWS):
    resource_name="accounts"
    #TODO add DefaultAddress
    _settables = (
        'Username', 'Email', 'FirstName', 'LastName', 'Suffix',
        'Phone'
    )
    _properties = (
        'AccountID', 'Username', 'Email', 'FirstName', 'LastName',
        'Suffix', 'Phone'
    )

class ContactWS(AutohubResourceWS):
    resource_name="contacts"
    _settables = (
        'ContactName', 'NotifyTo', 'ContactType', 'Prefered'
    )
    _properties = (
        'ContactName', 'NotifyTo', 'ContactType', 'Prefered'
    )

class DeviceWS(AutohubCommandableWS):
    resource_name="devices"
    _settables = (
        'device_name_', 'button_on_level', 'button_on_ramp_rate', 'enable_blink_on_traffic',
		'enable_led', 'enable_load_sense', 'enable_programming_lock', 'enable_resume_dim', 
		'x10_house_code', 'x10_unit_code'
    )
    _properties = (
        'device_address_', 'device_name_', 'properties_'
    )

    @property
    def DeviceCategory(self):
        import yaml
        import os
        try:
            file_dir = os.path.dirname(os.path.realpath(__file__))
            with open(file_dir+"/categories.yml", encoding='utf-8') as categories_file:
                categories = yaml.load(categories_file) or {}
        except yaml.YAMLError:
            return "No Category"
        return categories.get('dev_cat', {}).get(self._properties_["device_category"], "No Category")
