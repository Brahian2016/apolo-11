import random
from datetime import datetime
import hashlib
import yaml
from apolo11.python.metadata.Directory import PathInputRaw

with open(PathInputRaw.configuration_file, 'r') as file:
    config_data = yaml.safe_load(file)
    if config_data is None:
        raise ValueError("Error al cargar el archivo YAML.")
    missionsConfig: list = config_data.get('Missions', [])
    deviceTypeConfig: list = config_data.get('DeviceType', [])
    deviceStatusConfig: list = config_data.get('DeviceStatus', [])


class Mission:
    """Class to obtain a random mission name
    """
    def __init__(self) -> None:
        """Constructor method that generate the ramdom mission
        """
        self.name: str = random.choice(missionsConfig)


class DeviceType:
    """"Class that define device type and device status
    """
    def __init__(self) -> None:
        self.device_type: str = random.choice(deviceTypeConfig)
        self.status: str = self.generate_status()

    def generate_status(self) -> str:
        return random.choice(deviceStatusConfig)


class Device(DeviceType, Mission):
    """Generate device hash and file structure
    
    :param DeviceType: Used for take the device type
    :type DeviceType: class
    :param Mission: Used for take a random Mission name
    :type Mission: class
    """
    file_counter: int = 1  # Contador de archivos, inicializado en 1
    
    def __init__(self) -> None:
        """Constructor method that inicialize Date, hash, file number and counter values
        """
        DeviceType.__init__(self)
        Mission.__init__(self)
        self.date: str = datetime.now().strftime("%d%m%y%H%M%S")
        self.hash: hashlib = self.generate_hash()
        self.file_number: int = Device.file_counter  # Asignar número de archivo
        Device.file_counter += 1  # Incrementar el contador solo una vez

    def generate_hash(self) -> hashlib:
        """Generate hash identifier

        :return: hash object
        :rtype: hashlib
        """
        if self.name == "UNKN":
            return ''

        data: str = f"{self.date}{self.name}{self.device_type}{self.status}"
        return hashlib.md5(data.encode()).hexdigest()

    def get_description(self) -> yaml:
        """Get a description of the object.

        Returns:
        dict: A dictionary containing the following information:
        - "date": The date associated with the object.
        - "mission": The name of the mission.
        - "device_type": The type of device.
        - "device_status": The status of the device.
        - "hash": The hash associated with the object.
        """
        return {
            "date": self.date,
            "mission": self.name,
            "device_type": self.device_type,
            "device_status": self.status,
            "hash": self.hash
        }
