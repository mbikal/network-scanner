from nmap import PortScanner

class Network(object):
    def __init__(self):
        self.ip_default = '192.168.1.1'
        self.ip = input('Please input network IP (press return for ' + self.ip_default + '):\n')

    def get_devices(self):
        '''Return a list of devices with additional details'''
        
        if len(self.ip) >= 1:
            network_to_scan = self.ip + '/16'
        else:
            network_to_scan = self.ip_default + '/24'

        p_scanner = PortScanner()
        print('Scanning {}...'.format(network_to_scan))
        
        # Perform OS detection using -O (OS detection)
        p_scanner.scan(hosts=network_to_scan, arguments='-A -O -T5')  # -O for OS detection, -T4 for faster execution
        
        device_list = []
        for device in p_scanner.all_hosts():
            info = p_scanner[device]
            
            # Try to fetch MAC, model name, OS information, etc.
            device_data = {
                'host': device,
                'mac': info.get('addresses', {}).get('mac', 'UNKNOWN_MAC'),
                'model_name': info.get('osmatch', [{'name': 'Unknown'}])[0].get('name', 'Unknown') if info.get('osmatch') else 'Unknown',
                'os': info.get('osmatch', [{'osclass': 'Unknown'}])[0].get('osclass', 'Unknown') if info.get('osmatch') else 'Unknown',  # OS class info
                'hostnames': info.get('hostnames', [{}]),
                'version': info.get('osmatch', [{'osfamily': 'Unknown'}])[0].get('osfamily', 'Unknown') if info.get('osmatch') else 'Unknown',  # Version or family info
            }
            device_list.append((device, device_data))
        
        return device_list
