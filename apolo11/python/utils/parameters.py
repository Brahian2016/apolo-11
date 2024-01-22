import yaml
from apolo11.python.metadata.Directory import PathInputRaw


def load_config() -> None:
    """Load configuration data from a YAML file.

    Args:
        None

    Returns:
        None

    Raises:
        ValueError: If there is an issue loading the YAML file or if the file content is invalid.
            - If the specified file is not found.
            - If there is any other exception during the YAML loading process.

    The function reads the content of the specified YAML configuration file and returns
    a dictionary containing the loaded configuration data. It uses the PyYAML library
    to safely load the YAML content.
    """
    try:
        with open(PathInputRaw.configuration_file, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise ValueError(f"Configuration file '{PathInputRaw.configuration_file}' not found.")
    except Exception as e:
        raise ValueError(f"Error al cargar el archivo YAML: {e}")


def get_parameters() -> dict:
    """Retrieve parameters from a YAML configuration file.

    Returns:
    dict: A dictionary containing the extracted parameters.

    Raises:
    ValueError: If there is an issue loading the YAML file or if the file content is invalid.

    Configuration File Format:
    The configuration file is expected to be in YAML format and contain the following fields:

    - num_loops (int): Number of loops to execute.
    - time_to_create_file (int): Time in seconds to wait before creating a file in each loop.
    - range_for_files (bool): Whether to use a range for creating files (True/False).
    - max_files_per_loop (int): Maximum number of files to create in a single loop.
    - min_files_per_loop (int): Minimum number of files to create in a single loop.
    - infinity_loops (bool): Whether to execute an infinite number of loops (True/False).
    - missionsConfig (list): List of mission configurations.
    - deviceTypeConfig (list): List of device type configurations.
    - deviceStatusConfig (list): List of device status configurations.

    """
    
    # Load configuration data from YAML file
    config_data = load_config()

    # Extract individual parameters from the configuration data
    num_loops: int = config_data.get('num_loops', 0)
    time_to_create_file: int = config_data.get('time_to_create_file', 0)
    range_for_files: bool = config_data.get('range_for_files', 0)
    max_files_per_loop: int = config_data.get('max_files_per_loop', 0)
    min_files_per_loop: int = config_data.get('min_files_per_loop', 0)
    infinity_loops: bool = config_data.get('infinity_loops', 0)
    missionsConfig: list[str] = config_data.get('Missions', [])
    deviceTypeConfig: list[str] = config_data.get('DeviceType', [])
    deviceStatusConfig: list[str] = config_data.get('DeviceStatus', [])
    execute_by_time: bool = config_data.get('execute_by_time', 0)
    time_execution_second: int = config_data.get('time_execution_second', 0)
    
    # Validations for num_loops
    if 'num_loops' not in config_data:
        raise ValueError("Missing 'num_loops' field in the configuration file.")
    if not infinity_loops and not isinstance(infinity_loops, bool):
        raise ValueError("Invalid value for range_for_files. It should be a boolean.")
    if not infinity_loops and not 0 < num_loops:
        raise ValueError("Invalid value for num_loops. It should be greater than 0.")
    
    # Validations for time_to_create_file
    if 'time_to_create_file' not in config_data:
        raise ValueError("Missing 'time_to_create_file' field in the configuration file.")
    if not isinstance(time_to_create_file, int) or time_to_create_file < 0:
        raise ValueError("Invalid value for time_to_create_file. It should be a non-negative integer.")
    
    # Validations for range_for_files
    if 'range_for_files' not in config_data:
        raise ValueError("Missing 'range_for_files' field in the configuration file.")
    if range_for_files and not isinstance(range_for_files, bool):
        raise ValueError("Invalid value for range_for_files. It should be a boolean.")
    
    # Validations for max_files_per_loop
    if 'max_files_per_loop' not in config_data:
        raise ValueError("Missing 'max_files_per_loop' field in the configuration file.")
    if range_for_files and not isinstance(max_files_per_loop, int):
        raise ValueError("Invalid value for max_files_per_loop. It should be integer.")
    if max_files_per_loop < 0:
        raise ValueError("Invalid value for max_files_per_loop. It should be greater than 0.")
    
    # Validations for min_files_per_loop
    if 'min_files_per_loop' not in config_data:
        raise ValueError("Missing 'min_files_per_loop' field in the configuration file.")
    if range_for_files and not isinstance(min_files_per_loop, int):
        raise ValueError("Invalid value for min_files_per_loop. It should be integer.")
    if min_files_per_loop < 0:
        raise ValueError("Invalid value for min_files_per_loop. It should be greater than 0.")
    if min_files_per_loop > max_files_per_loop:
        raise ValueError("Invalid value for min_files_per_loop. It should be less than max_files_per_loop.")
    
    # Validations for infinity_loops
    if 'infinity_loops' not in config_data:
        raise ValueError("Missing 'infinity_loops' field in the configuration file.")
    if not isinstance(infinity_loops, bool):
        raise ValueError("Invalid value for infinity_loops. It should be a boolean.")
    
    # Validations for missionsConfig
    if 'Missions' not in config_data:
        raise ValueError("Missing 'Missions' field in the configuration file.")
    if not isinstance(missionsConfig, list):
        raise ValueError("Invalid value for Missions. It should be a list.")
    
    # Validations for deviceTypeConfig
    if 'DeviceType' not in config_data:
        raise ValueError("Missing 'DeviceType' field in the configuration file.")
    if not isinstance(deviceTypeConfig, list):
        raise ValueError("Invalid value for DeviceType. It should be a list.")
    
    # Validations for deviceStatusConfig
    if 'DeviceStatus' not in config_data:
        raise ValueError("Missing 'deviceStatus' field in the configuration file.")
    if not isinstance(deviceStatusConfig, list):
        raise ValueError("Invalid value for deviceStatus. It should be a list.")
    
    # Validations for execute_by_time
    if 'infinity_loops' not in config_data:
        raise ValueError("Missing 'execute_by_time' field in the configuration file.")
    if not isinstance(execute_by_time, bool):
        raise ValueError("Invalid value for execute_by_time. It should be a boolean.")
    
    # Validations for time_execution_second
    if 'time_execution_second' not in config_data:
        raise ValueError("Missing 'time_execution_second' field in the configuration file.")
    if not isinstance(time_execution_second, int) or time_execution_second < 0:
        raise ValueError("Invalid value for time_execution_second. It should be a non-negative integer.")
    
    # Extra validations
    allowed_fields = {'num_loops', 'time_to_create_file', 'range_for_files', 'max_files_per_loop', 'min_files_per_loop', 'infinity_loops', 'Missions', 'DeviceType', 'DeviceStatus', 'execute_by_time', 'time_execution_second'}
    unknown_fields = set(config_data.keys()) - allowed_fields

    if unknown_fields:
        raise ValueError(f"Unknown field(s) in the configuration file: {', '.join(unknown_fields)}")

    # Create a dictionary with extracted parameters
    parameters_dict = {
        'num_loops': num_loops,
        'time_to_create_file': time_to_create_file,
        'range_for_files': range_for_files,
        'max_files_per_loop': max_files_per_loop,
        'min_files_per_loop': min_files_per_loop,
        'infinity_loops': infinity_loops,
        'missionsConfig': missionsConfig,
        'deviceTypeConfig': deviceTypeConfig,
        'deviceStatusConfig': deviceStatusConfig,
        'execute_by_time': execute_by_time,
        'time_execution_second': time_execution_second
    }

    return parameters_dict
