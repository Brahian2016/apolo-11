import random
from datetime import datetime
import hashlib
import yaml
from Apolo11.python.metadata.Directory import PathInputRaw

with open(PathInputRaw.configuration_file, 'r') as file:
    config_data = yaml.safe_load(file)
    if config_data is None:
        raise ValueError("Error al cargar el archivo YAML.")
    missionsConfig: list = config_data.get('Missions', [])
    deviceTypeConfig: list = config_data.get('DeviceType', [])
    deviceStatusConfig: list = config_data.get('DeviceStatus', [])


class Mission:
    def __init__(self):
        self.name: str = random.choice(missionsConfig)


class DeviceType:
    def __init__(self):
        self.device_type: str = random.choice(deviceTypeConfig)
        self.status: str = self.generate_status()

    def generate_status(self) -> str:
        return random.choice(deviceStatusConfig)


class Device(DeviceType, Mission):
    file_counter = 1  # Contador de archivos, inicializado en 1
    
    def __init__(self):
        DeviceType.__init__(self)
        Mission.__init__(self)
        self.date = datetime.now().strftime("%d%m%y%H%M%S")
        self.hash = self.generate_hash()
        self.file_number = Device.file_counter  # Asignar número de archivo
        Device.file_counter += 1  # Incrementar el contador solo una vez

    def generate_hash(self) -> hashlib:
        '''
        
        '''
        if self.name == "UNKN":
            return ''

        data = f"{self.date}{self.name}{self.device_type}{self.status}"
        return hashlib.md5(data.encode()).hexdigest()

    def get_description(self):
        return {
            "date": self.date,
            "mission": self.name,
            "device_type": self.device_type,
            "device_status": self.status,
            "hash": self.hash
        }
