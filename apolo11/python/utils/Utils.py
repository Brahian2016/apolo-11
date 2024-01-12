import os
import time
import random
import yaml
from Apolo11.python.classes.classes import *
from Apolo11.python.metadata.Directory import *
from datetime import datetime

def get_parameters() -> dict:
    with open(PathInputRaw.configuration_file, 'r') as file:
        try:
            config_data = yaml.safe_load(file)
            if config_data is None:
                raise ValueError("Error al cargar el archivo YAML. Asegúrate de que sea válido.")
        except yaml.YAMLError as e:
            raise ValueError(f"Error al cargar el archivo YAML: {e}")

        num_loops: int = config_data.get('num_loops', 0)
        time_to_create_file: int = config_data.get('time_to_create_file', 0)
        range_for_files: bool = config_data.get('range_for_files', 0)
        max_files_per_loop: int = config_data.get('max_files_per_loop', 0)
        min_files_per_loop: int = config_data.get('min_files_per_loop', 0)
        infinity_loops: bool = config_data.get('infinity_loops', 0)
    
        parameters_dict = {
            'num_loops': num_loops,
            'time_to_create_file': time_to_create_file,
            'range_for_files': range_for_files,
            'max_files_per_loop': max_files_per_loop,
            'min_files_per_loop': min_files_per_loop,
            'infinity_loops': infinity_loops
        }

        return parameters_dict


def run_simulation():
    parameters_dict = get_parameters()
    current_date = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    output_folder = os.path.join(PathOutputRaw.output_files, current_date)
    loops_num = 0
    counter_loops = 0

    try:
        if parameters_dict['num_loops'] > 0:
            while loops_num < parameters_dict['num_loops']:
                simulation_folder = os.path.join(output_folder, f"Simulacion_{counter_loops + 1}")

                if parameters_dict['range_for_files']:
                    print("Valor mínimo de archivos por ciclo:", parameters_dict['min_files_per_loop'])
                    print("Valor máximo de archivos por ciclo:", parameters_dict['max_files_per_loop'])
                    for i in range(1, random.randint(parameters_dict['min_files_per_loop'], parameters_dict['max_files_per_loop'] + 1)):
                        create_files(simulation_folder)
                    if loops_num + 1 < parameters_dict['num_loops']:
                        time.sleep(parameters_dict['time_to_create_file'])
                else:
                    for i in range(1, parameters_dict['max_files_per_loop'] + 1):
                        create_files(simulation_folder)
                    if loops_num + 1 < parameters_dict['num_loops']:
                        time.sleep(parameters_dict['time_to_create_file'])
                        
                loops_num += 1
                counter_loops += 1

                if parameters_dict['infinity_loops']:
                    loops_num = 0
        else:
            raise ValueError("La cantidad de loops debe ser mayor a 0")
    except KeyboardInterrupt:
        print("\nProceso interrumpido. Saliendo...")


            
def create_files(output_folder: str) -> None:
    device = Device()

    file_name = f"APL{device.name}-0000{device.file_number}.log"
    file_path = os.path.join(output_folder, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    print("Intentando crear el archivo en:", file_path)

    with open(file_path, "w") as file:
        yaml.dump(device.get_description(), file, default_flow_style=False)