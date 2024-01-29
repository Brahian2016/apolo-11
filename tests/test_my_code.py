import os
import pytest
from apolo11.python.utils.Utils import create_files
from apolo11.python.metadata.Directory import PathOutputRaw
from apolo11.python.utils.parameters import load_config, get_parameters
from apolo11.python.utils.Utils import run_reports


@pytest.fixture
def cleanup_generated_files():
    # Fixture para limpiar archivos generados durante las pruebas
    if os.path.exists(PathOutputRaw.output_files):
        for filename in os.listdir(PathOutputRaw.output_files):
            file_path = os.path.join(PathOutputRaw.output_files, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error al borrar archivos de prueba: {e}")


def test_create_files(cleanup_generated_files):
    # Prueba para la función create_files
    output_folder = "test_output_folder"
    create_files(output_folder)

    # Verificar si se ha creado el archivo esperado
    files_created = os.listdir(output_folder)
    assert files_created[0].startswith("APL")
    assert files_created[0].endswith(".log")


def test_reports(cleanup_generated_files):
    # Prueba para el proceso de generación de informes
    run_reports()

    # Verificar si se ha creado el informe esperado
    report_files = os.listdir(PathOutputRaw.output_reports)
    assert report_files[0].startswith("APLSTATS_REPORT")
    assert report_files[0].endswith(".log")


def test_load_config():
    # Prueba para la función load_config
    config_data = load_config()

    # Verificar que se haya cargado la configuración correctamente
    assert "Missions" in config_data
    assert "DeviceType" in config_data
    assert "DeviceStatus" in config_data


def test_get_parameters():
    # Prueba para la función get_parameters
    parameters_dict = get_parameters()

    # Verificar que se hayan extraído los parámetros correctamente
    assert "num_loops" in parameters_dict
    assert "time_to_create_file" in parameters_dict
    assert "range_for_files" in parameters_dict
    assert "max_files_per_loop" in parameters_dict
    assert "min_files_per_loop" in parameters_dict
    assert "infinity_loops" in parameters_dict
    assert "missionsConfig" in parameters_dict
    assert "deviceTypeConfig" in parameters_dict
    assert "deviceStatusConfig" in parameters_dict
    assert "execute_by_time" in parameters_dict
    assert "time_execution_second" in parameters_dict
