from apolo11.python.classes.classes import *
from apolo11.python.metadata.Directory import *
import time

with open(PathInputRaw.configuration_file, 'r') as file:
    config_data = yaml.safe_load(file)
    if config_data is None:
        raise ValueError("Error al cargar el archivo YAML. Asegúrate de que sea válido.")
    
    num_loops = config_data.get('num_loops', 0)
    num_files_per_loop = config_data.get('num_files_per_loop', 0)
    time_to_create_file = config_data.get('time_to_create_file', 0)


def run_simulation():
    
    for _ in range(num_loops):
        
        for i in range(1, num_files_per_loop + 1):  # Cambiar según la cantidad de archivos por misión
            device = Device()

            file_name = f"APL{device.name}0000{device.file_number}.log"  # Cambiar la extensión a .yaml
            file_path = os.path.join(PathOutputRaw.output_files, "devices", file_name)

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            print("Intentando crear el archivo en:", file_path)

            with open(file_path, "w") as file:
                yaml.dump(device.get_description(), file, default_flow_style=False)

        time.sleep(time_to_create_file)