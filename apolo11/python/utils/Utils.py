import os
import time
import random
import yaml
import pandas as pd
import shutil
from apolo11.python.classes.classes import *
from apolo11.python.metadata.Directory import *
from apolo11.python.utils.parameters import get_parameters
from datetime import datetime


def run_simulation() -> None:
    """Run a simulation based on parameters obtained from the configuration file.

    Retrieves simulation parameters using the `get_parameters` function and executes a simulation
    process accordingly. The simulation creates files in specified folders and controls the number
    of loops, sleep duration between loops, and file creation options.

    Returns:
    None

    Raises:
    ValueError: If the number of loops specified in the configuration is not greater than 0.
    """
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
    """Create .log files based on device information in the specified output folder.

    Generates log files with unique names for each device, incorporating device information
    such as name, file number, and description, etc.

    Args:
    output_folder (str): The folder where log files will be created.

    Returns:
    None

    Usage:
    create_files(output_folder)
    """
    device = Device()

    file_name = f"APL{device.name}-0000{device.file_number}.log"
    file_path = os.path.join(output_folder, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    print("Intentando crear el archivo en:", file_path)

    with open(file_path, "w") as file:
        yaml.dump(device.get_description(), file, default_flow_style=False)
        
def run_reports() -> None:
    
    datos_concatenados = pd.DataFrame()

    lista_registros = []

    for ruta_carpeta, carpetas, archivos in os.walk(PathOutputRaw.output_files):
        for archivo in archivos:
            ruta_archivo = os.path.join(ruta_carpeta, archivo)
            nombre, extension = os.path.splitext(archivo)
            if os.path.isfile(ruta_archivo) and extension == '.log':
                
                with open(ruta_archivo, 'r') as file:
                    # Almacenar los datos de cada registro -> dict
                    registro: dict = {}
                    
                    # Obtener la carpeta y simulación desde la ruta
                    carpeta, simulacion = os.path.split(ruta_carpeta)
                    
                    # Agregar la información de carpeta y simulación al registro
                    # Utilizar os.path.basename para obtener el nombre de la carpeta sin la ruta completa
                    registro['Carpeta'] = os.path.basename(carpeta)
                    registro['Simulacion'] = simulacion
                    
                    # Iterar sobre las líneas del archivo
                    for linea in file:
                        # Dividir la línea en clave y valor
                        clave, valor = linea.strip().split(': ')
                        registro[clave] = valor
                        
                        # Agregar la fecha de reporte como la fecha actual
                        registro['Fecha de Reporte'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        
                        # Convertir el registro a un DataFrame
                        lista_registros.append(registro)

    # Crear el DataFrame a partir de la lista de registros
    datos_concatenados = pd.DataFrame(lista_registros)
    datos_concatenados.drop_duplicates(inplace=True)
    
    csv_path = os.path.join(PathOutputRaw.output_reports, 'datos_concatenados.csv')
    
    datos_concatenados.to_csv(csv_path, sep=';', index=False)
