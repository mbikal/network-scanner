from datetime import date


class Device:
    def __init__(self, mac, ip, name, devices_data, model_name="Unknown", date_added=None):
        self.mac = mac
        self.ip = ip
        self.name = name
        self.model_name = model_name
        self.date_added = date_added or str(date.today())

        # Load additional details from devices.json if the device exists
        device_info = devices_data.get(self.mac, {})
        self.type = device_info.get('type', 'Unknown')
        self.owner = device_info.get('owner', 'Unknown')
        self.location = device_info.get('location', 'Unknown')
        self.allowed = device_info.get('allowed', False)

    def to_list(self):
        """Returns device details as a list for table representation."""
        return [
            self.mac, self.ip, self.name, self.model_name, self.date_added,
            self.type, self.owner, self.location, self.allowed
        ]

    def to_string(self):
        """Returns device details as a formatted string for logging."""
        return (
            f"MAC: {self.mac}, IP: {self.ip}, Name: {self.name}, Model: {self.model_name}, "
            f"Date Added: {self.date_added}, Type: {self.type}, Owner: {self.owner}, "
            f"Location: {self.location}, Allowed: {self.allowed}"
        )
