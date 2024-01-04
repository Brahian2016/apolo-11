import os
import random
from datetime import datetime
import hashlib
import time

class Mission:
    def __init__(self):
        self.name = random.choice(["ORBONE", "CLNM", "TMRS", "GALAXONE", "UNKN"])
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)

    def generate_report(self):
        for device in self.devices:
            print(device.get_description())

class DeviceType:
    def __init__(self):
        self.device_type = random.choice(["Satellite", "Spacecraft", "Spacesuit", "Unknown"])
        self.status = self.generate_status()

    def generate_status(self):
        return random.choice(["excellent", "good", "warning", "faulty", "killed", "unknown"])

class Device(DeviceType, Mission):
    def __init__(self):
        DeviceType.__init__(self)
        Mission.__init__(self)
        self.date = datetime.now().strftime("%d%m%y%H%M%S")
        self.hash = self.generate_hash()

    def generate_hash(self):
        if self.name == "UNKN":
            return None

        data = f"{self.date}{self.name}{self.device_type}{self.status}"
        return hashlib.md5(data.encode()).hexdigest()

    def get_description(self):
        return f"date: {self.date}\nmission: {self.name}\ndevice_type: {self.device_type}\ndevice_status: {self.status}\nhash: {self.hash}"

def run_simulation(output_folder, num_missions):
    while True:
        missions = []

        for _ in range(num_missions):
            mission = Mission()
            missions.append(mission)

            num_files = random.randint(1, 100)

            for i in range(1, num_files + 1):
                device = Device()
                mission.add_device(device)

                # Reemplazar corchetes y barras verticales en el nombre del archivo
                file_name = f"APL{device.name}0000{i}.log"
                file_path = os.path.join(output_folder, "devices", file_name)

                # Comprobar y crear la carpeta si no existe
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                print("Intentando crear el archivo en:", file_path)  # Agregado para depuración

                with open(file_path, "w") as file:
                    file.write(device.get_description())

                time.sleep(2)  # Esperar 2 segundos

        for mission in missions:
            mission.generate_report()

if __name__ == "__main__":
    output_folder = "C:\\Users\\anjim\\OneDrive\\Documentos\\apolo-11\\apolo-11\\Archivos"
    num_missions = int(input("Ingrese la cantidad de misiones a crear: "))
    run_simulation(output_folder, num_missions)
