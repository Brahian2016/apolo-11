import os
import random
from datetime import datetime
import hashlib
import time
import yaml

class Mission:
    def __init__(self):
        self.name = random.choice(["ORBONE", "CLNM", "TMRS", "GALAXONE", "UNKN"])


class DeviceType:
    def __init__(self):
        self.device_type = random.choice(["Satellite", "Spacecraft", "Spacesuit", "Unknown"])
        self.status = self.generate_status()

    def generate_status(self) -> str:
        return random.choice(["excellent", "good", "warning", "faulty", "killed", "unknown"])

class Device(DeviceType, Mission):
    file_counter = 1  # Contador de archivos, inicializado en 1

    def __init__(self):
        DeviceType.__init__(self)
        Mission.__init__(self)
        self.date = datetime.now().strftime("%d%m%y%H%M%S")
        self.hash = self.generate_hash()
        self.file_number = Device.file_counter  # Asignar número de archivo
        Device.file_counter += 1  # Incrementar el contador solo una vez

    def generate_hash(self):
        if self.name == "UNKN":
            return None

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

def run_simulation(output_folder):
    num_loops = int(input("Ingrese la cantidad de bucles a crear: "))
    num_files_per_loop = int(input("Ingrese la cantidad de archivos por bucle: "))

    for _ in range(num_loops):
        
        for i in range(1, num_files_per_loop + 1):  # Cambiar según la cantidad de archivos por misión
            device = Device()

            file_name = f"APL{device.name}0000{device.file_number}.yaml"  # Cambiar la extensión a .yaml
            file_path = os.path.join(output_folder, "devices", file_name)

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            print("Intentando crear el archivo en:", file_path)

            with open(file_path, "w") as file:
                yaml.dump(device.get_description(), file, default_flow_style=False)

        time.sleep(2)  # Esperar 2 segundos después de crear el par de archivos


if __name__ == "__main__":
    output_folder = "C:\\Users\\Brahian Álvarez\\Documents\\apolo-11\\apolo-11\\Archivos"
    run_simulation(output_folder)