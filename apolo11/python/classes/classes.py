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
    """
    _summary_: Take a NASA mission name
    Mission type: class
    """
    def __init__(self) -> None:
        self.name: str = random.choice(missionsConfig)


class DeviceType:
    """"
    This class represents the device type each mission will use
    Attributes: 
    1. device_type (str): It's takes randomly one of the devices 
    2. status (str): Will return the device status randomly
    """
    def __init__(self) -> None:
        self.device_type: str = random.choice(deviceTypeConfig)
        self.status: str = self.generate_status()

    def generate_status(self) -> str:
        return random.choice(deviceStatusConfig)


class Device(DeviceType, Mission):
    """
    _summary_: Generate device hash and file structure
    :param DeviceType: This class is used for take device type and status
    :type DeviceType: class
    :param Mission: This class is used for take a random Mission name
    :type Mission: class
    """
    file_counter: int = 1  # Contador de archivos, inicializado en 1
    
    def __init__(self) -> None:
        DeviceType.__init__(self)
        Mission.__init__(self)
        self.date: str = datetime.now().strftime("%d%m%y%H%M%S")
        self.hash: hashlib = self.generate_hash()
        self.file_number: int = Device.file_counter  # Asignar número de archivo
        Device.file_counter += 1  # Incrementar el contador solo una vez

    def generate_hash(self) -> hashlib:
        '''
        
        '''
        if self.name == "UNKN":
            return ''

        data: str = f"{self.date}{self.name}{self.device_type}{self.status}"
        return hashlib.md5(data.encode()).hexdigest()

    def get_description(self) -> yaml:
        return {
            "date": self.date,
            "mission": self.name,
            "device_type": self.device_type,
            "device_status": self.status,
            "hash": self.hash
        }
