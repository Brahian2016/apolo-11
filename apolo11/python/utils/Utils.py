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
    logging.info('Iniciando proceso de simulación!!!')

    try:
        parameters_dict = get_parameters()
        current_date = datetime.now().strftime("%Y_%m_%d_%H%M%S")
        output_folder = os.path.join(PathOutputRaw.output_files, current_date)
        loops_num = 0
        counter_loops = 0

        start_time = time.time()

        if parameters_dict['num_loops'] > 0:
            while True:
                simulation_folder = os.path.join(output_folder, f"Simulacion_{counter_loops + 1}")

                if parameters_dict['execute_by_time']:
                    if time.time() - start_time >= parameters_dict['time_execution_second']:
                        logging.info(f"Se ha alcanzado el tiempo de ejecución definido ({parameters_dict['time_execution_second']} segundos). Finalizando simulación.")
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
            raise ValueError("La cantidad de loops debe ser mayor a 0")
    except KeyboardInterrupt:
        logging.info("\nProceso interrumpido. Saliendo...")

def create_files(output_folder: str) -> None:
    try:
        logging.info('Iniciando creación de archivos.')
        
        device = Device()

        file_name = f"APL{device.name}-0000{device.file_number}.log"
        file_path = os.path.join(output_folder, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(device.get_description(), file, default_flow_style=False)
            
        logging.info('Finalización de creación de archivos')
        
    except ValidationError as e:
        logging.error(f"Error de validación Pydantic al crear el Device: {e}")
    except Exception as e:
        # Capturar otras excepciones
        logging.error(f"Error desconocido al crear el Device: {e}")
    
    
def run_reports() -> bool:
    logging.info('Iniciando proceso de generación de reportes!!!')

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

    file_name = 'datos_concatenados_' + fecha_reporte + '.csv'
    csv_path = os.path.join(PathOutputRaw.output_reports, file_name)

    if not datos_concatenados.empty:
        datos_concatenados.to_csv(csv_path, sep=';', index=False)
        logging.info(f'Se generó el informe CSV: {file_name}')
        move_files_to_backup()
        consolidate_csv_files()
        return True
    else:
        logging.warning('No se encontraron datos para generar el informe.')
        return False

    
def move_files_to_backup() -> None:
    logging.info('Iniciando proceso de movimiento de archivos a la carpeta de respaldo.')

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
            logging.info(f'La carpeta {carpeta} fue comprimida y movida a la carpeta de respaldo.')
            
        except Exception as e:
            logging.error(f"Error al comprimir y mover la carpeta {carpeta}: {str(e)}")

def consolidate_csv_files():
    logging.info('Iniciando proceso de consolidación de archivos CSV.')

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
    consolidated_file_name = os.path.join(PathOutputRaw.output_consolidated, 'consolidado.csv')
    consolidated_df.to_csv(consolidated_file_name, index=False)

    logging.info(f'La consolidación de archivos CSV fue exitosa. Resultado guardado en {consolidated_file_name}.')
