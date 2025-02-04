import os
import json
import sys
from datetime import date
from getmac import get_mac_address
from prettytable import PrettyTable
from device import Device
from network import Network


class NetworkScanner:
    def __init__(self, data_path='data'):
        self.data_path = data_path
        self.devices_json_path = os.path.join(self.data_path, "devices.json")
        self.devices_data = self.load_devices_json()

    def load_devices_json(self):
        """Load devices.json or create an empty one if not found."""
        if not os.path.exists(self.devices_json_path):
            os.makedirs(self.data_path, exist_ok=True)
            default_data = {}
            with open(self.devices_json_path, "w") as write_file:
                json.dump(default_data, write_file, indent=4)
            return default_data
        with open(self.devices_json_path, "r") as read_file:
            return json.load(read_file)

    def scan_network(self):
        """Scan the network for devices."""
        network = Network()  # Ensure this class is properly implemented in `network.py`
        try:
            devices = network.get_devices()
        except KeyboardInterrupt:
            print(
                "You stopped scanning. Scanning may take a while. If it takes too long, there may be a problem with the connection. Did you specify the correct network?"
            )
            sys.exit()

        # Retrieve MAC addresses for each device
        for host, info in devices:
            info['mac'] = get_mac_address(ip=host) or "UNKNOWN_MAC"
            info['model_name'] = "Unknown"  # Placeholder for model name
        return devices

    def create_device_list(self, devices):
        """Categorize devices into known and unknown."""
        known_devices = []
        unknown_devices = []

        for host, info in devices:
            mac = info.get('mac', 'UNKNOWN_MAC')
            hostnames = info.get('hostnames', [{}])
            name = hostnames[0].get('name', 'UNKNOWN_HOST') if hostnames else 'UNKNOWN_HOST'
            model_name = info.get('model_name', 'Unknown')

            # Instantiate the device
            device = Device(mac, host, name, self.devices_data, model_name=model_name)

            # Categorize the device
            if device.name and device.name != 'UNKNOWN_HOST':
                known_devices.append(device)
            else:
                unknown_devices.append(device)

        return {'known': known_devices, 'unknown': unknown_devices}

    def log_devices(self, data):
        """Log devices to a file."""
        log_text = ''

        # Known devices
        table = PrettyTable()
        table.field_names = ["MAC ADDRESS", "IP", "NAME IN NETWORK", "MODEL", "DATE ADDED", "TYPE", "OWNER", "LOCATION", "ALLOWED"]
        for device in data['known']:
            table.add_row(device.to_list())
            log_text += f"{device.to_string()}\n"

        print('Known Devices\n{}'.format(table))

        # Unknown devices
        table = PrettyTable()
        table.field_names = ["MAC ADDRESS", "IP", "NAME IN NETWORK", "MODEL", "DATE ADDED"]
        for device in data['unknown']:
            table.add_row(device.to_list()[:5])  # Only include available details
            log_text += f"{device.to_string()}\n"

        print('Unknown Devices\n{}'.format(table))

        # Ensure log directory exists
        if not os.path.isdir(self.data_path):
            os.mkdir(self.data_path)

        # Write log file
        log_file_path = os.path.join(self.data_path, f"{date.today()}.log")
        with open(log_file_path, "a") as log_file:
            log_file.write(log_text)
            print(f'You can find a log file with all devices in "{log_file_path}"')

    def run(self):
        """Run the network scanner."""
        devices = self.scan_network()
        device_list = self.create_device_list(devices)
        self.log_devices(device_list)


if __name__ == '__main__':
    scanner = NetworkScanner()
    scanner.run()
