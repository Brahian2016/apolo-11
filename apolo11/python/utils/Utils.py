import os
import time
import random
import yaml
import pandas as pd
import shutil
import logging
from pydantic import ValidationError
from zipfile import ZipFile
from apolo11.python.classes.classes import *
from apolo11.python.metadata.Directory import *
from apolo11.python.utils.parameters import get_parameters
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def run_simulation() -> None:
    """
    Run a simulation process based on specified parameters.

    This function initializes a simulation process, creating folders and files according
    to the specified parameters.
    
    Raises:
    - ValueError: If the number of loops specified in the parameters is not greater than 0.

    Note:
    - The simulation can be interrupted using a KeyboardInterrupt (Ctrl+C).
    """
    logging.info('Starting simulation process...')

    try:
        parameters_dict = get_parameters()
        current_date = datetime.now().strftime("%Y_%m_%d_%H%M%S")
        output_folder = os.path.join(PathOutputRaw.output_files, current_date)
        loops_num = 0
        counter_loops = 0

        start_time = time.time()

        if parameters_dict['num_loops'] > 0:
            while True:
                simulation_folder = os.path.join(output_folder, f"Simulation_{counter_loops + 1}")

                if parameters_dict['execute_by_time']:
                    if time.time() - start_time >= parameters_dict['time_execution_second']:
                        logging.info(f"Exceeded execution time ({parameters_dict['time_execution_second']} seconds). Ending simulation.")
                        break
                    else:
                        if parameters_dict['range_for_files']:                        
                            for i in range(1, random.randint(parameters_dict['min_files_per_loop'], parameters_dict['max_files_per_loop'] + 1)):
                                create_files(simulation_folder)
                            counter_loops += 1
                        else:
                            for i in range(1, parameters_dict['max_files_per_loop'] + 1):
                                create_files(simulation_folder)
                            counter_loops += 1   
                else:
                    if parameters_dict['range_for_files']:                        
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
            raise ValueError("The number of loops must be greater than 0.")
    except KeyboardInterrupt:
        logging.info("\nInterrupted process. Exit...")

def create_files(output_folder: str) -> None:
    """
    Create files in the specified output folder.

    This method generates a log file for a simulated device and saves it to the specified output folder.
    The log file contains device information in YAML format.

    Parameters:
    - output_folder (str): The path to the folder where the log file will be created.

    Raises:
    - ValidationError: If there is a Pydantic validation error during device creation.
    - Exception: If an unknown error occurs during device creation.

    Note:
    - The log file is named in the format "APL{device_name}-0000{file_number}.log".
    - Device information is obtained using the Device class and saved in YAML format.
    """
    
    try:
        logging.info('Starting files creation.')
        
        device = Device()

        file_name = f"APL{device.name}-0000{device.file_number}.log"
        file_path = os.path.join(output_folder, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(device.get_description(), file, default_flow_style=False)
            
        logging.info('Ending files creation')
        
    except ValidationError as e:
        logging.error(f"Pydantic validation error when creating device: {e}")
    except Exception as e:
        # Capturar otras excepciones
        logging.error(f"Unknown error when creating device: {e}")
    
    
def run_reports() -> bool:
    """
    Generate reports based on log files in the specified output folder.

    This method searches for log files in the output folder, extracts information, and creates
    a consolidated CSV report. The CSV report is saved in the 'output_reports' folder and includes data
    from different simulations.

    Returns:
    - bool: True if the report is generated successfully, False if no data is found.

    Note:
    - Log files in the '.log' format are processed.
    - Extracted information includes simulation folder, report date.
    - The consolidated CSV report is named 'concatenated_data_{report_date}.csv'.
    - The report is saved in the 'output_reports' folder.
    - If the report is generated successfully, files are moved to backup and CSV files are consolidated.
    """
    logging.info('Starting reporting generation...')

    datos_concatenados = pd.DataFrame()
    lista_registros = []
    fecha_reporte = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

    for ruta_carpeta, carpetas, archivos in os.walk(PathOutputRaw.output_files):
        for archivo in archivos:
            ruta_archivo = os.path.join(ruta_carpeta, archivo)
            nombre, extension = os.path.splitext(archivo)

            if os.path.isfile(ruta_archivo) and extension == '.log':
                with open(ruta_archivo, 'r') as file:
                    registro: dict = {}
                    carpeta, simulacion = os.path.split(ruta_carpeta)
                    registro['Carpeta'] = os.path.basename(carpeta)
                    registro['Simulacion'] = simulacion
                    registro['Fecha de Reporte'] = fecha_reporte

                    for linea in file:
                        clave, valor = linea.strip().split(': ')
                        registro[clave] = valor

                    lista_registros.append(registro)

    datos_concatenados = pd.DataFrame(lista_registros)
    datos_concatenados.drop_duplicates(inplace=True)

    file_name = 'concatenated_data_' + fecha_reporte + '.csv'
    csv_path = os.path.join(PathOutputRaw.output_reports, file_name)

    if not datos_concatenados.empty:
        datos_concatenados.to_csv(csv_path, sep=';', index=False)
        logging.info(f'CSV report generated: {file_name}')
        move_files_to_backup()
        consolidate_csv_files()
        return True
    else:
        logging.warning('No data were found to generate the report.')
        return False

    
def move_files_to_backup() -> None:
    """
    Move files to the backup folder after compressing them into zip archives.

    This method compresses each subfolder in the 'output_files' directory into a zip archive and then
    moves the zip file to the 'data_backups' folder.

    Note:
    - The 'data_backups' folder is created if it doesn't exist.
    - Each subfolder in 'output_files' is compressed into a separate zip archive.
    - The compressed zip file is moved to the 'data_backups' folder.
    - The original subfolder is deleted after a successful compression and move operation.
    - Any errors during the process are logged using "logging" library. 
    """
    logging.info('Starting backup process (Moving files to backup folder.)')

    # Verificar si la carpeta de destino existe, si no, crearla
    if not os.path.exists(PathDataRaw.data_backups):
        os.makedirs(PathDataRaw.data_backups)

    for carpeta in os.listdir(PathOutputRaw.output_files):
        # Crear la ruta completa de la carpeta de origen y destino
        ruta_origen = os.path.join(PathOutputRaw.output_files, carpeta)
        ruta_destino_zip = os.path.join(PathDataRaw.data_backups, carpeta + '.zip')

        try:
            # Comprimir la carpeta en un archivo zip
            with ZipFile(ruta_destino_zip, 'w') as zipf:
                for carpeta_raiz, _, archivos in os.walk(ruta_origen):
                    for archivo in archivos:
                        ruta_archivo_completa = os.path.join(carpeta_raiz, archivo)
                        ruta_relativa = os.path.relpath(ruta_archivo_completa, ruta_origen)
                        zipf.write(ruta_archivo_completa, arcname=ruta_relativa)

            # Mover el archivo zip a la ubicación de destino
            shutil.move(ruta_destino_zip, os.path.join(PathDataRaw.data_backups, carpeta + '.zip'))

            shutil.rmtree(ruta_origen)
            logging.info(f'Folder {carpeta} was compressed and moved to backup folder')
            
        except Exception as e:
            logging.error(f"Error when attempt to compress and move the folder {carpeta}: {str(e)}")

def consolidate_csv_files():
    """This function performs the following steps:

    1. Checks for output directory: Ensures the output directory exists, creating it if necessary.
    2. Reads CSV files: Iterates through CSV files in a specified input directory (PathOutputRaw.output_reports), reads their contents into DataFrames using Pandas, and appends them to a list.
    3. Concatenates DataFrames: Combines all DataFrames in the list into a single, consolidated DataFrame using Pandas' concat function.
    4. Saves merged CSV: Saves the consolidated DataFrame to a new CSV file named "merged.csv" in a specified output directory (PathOutputRaw.output_consolidated).
    5. Logs completion: Logs a message indicating successful completion and the location of the merged file.

    """
    logging.info('Starting CSV files consolidation.')

    # Verificar si la carpeta de destino existe, si no, crearla
    if not os.path.exists(os.path.dirname(PathOutputRaw.output_consolidated)):
        os.makedirs(os.path.dirname(PathOutputRaw.output_consolidated))

    # Lista para almacenar todos los marcos de datos (DataFrames) de los archivos CSV
    dataframes = []

    for file_name in os.listdir(PathOutputRaw.output_reports):
        if file_name.endswith(".csv"):
            file_path = os.path.join(PathOutputRaw.output_reports, file_name)
            
            df = pd.read_csv(file_path, dtype=str)
            dataframes.append(df)

    # Concatenar todos los DataFrames en uno solo
    consolidated_df = pd.concat(dataframes, ignore_index=True)

    # Guardar el DataFrame consolidado en un nuevo archivo CSV
    consolidated_file_name = os.path.join(PathOutputRaw.output_consolidated, 'merged.csv')
    consolidated_df.to_csv(consolidated_file_name, index=False)

    logging.info(f'CSV compilation was completed and succeed. Records are already saved on {consolidated_file_name}.')
