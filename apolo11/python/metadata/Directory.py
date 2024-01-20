import os


class CurrentDirectory:
    """Class that represents the "actual" work directory
    """
    current_directory: str = os.getcwd()

    
class PathDataRaw:
    """Class that represents the "data" work directory
    """
    data_directory: str = os.path.join(CurrentDirectory.current_directory, 'data')
    data_backups: str = os.path.join(data_directory, 'backups')


class PathInputRaw:
    """Class that represents the "input" work directory
    """
    input_directory: str = os.path.join(CurrentDirectory.current_directory, 'input')
    configuration_file: str = os.path.join(input_directory, 'configuration.yaml')


class PathOutputRaw:
    """Class that represents the "output" work directory
    """
    output_directory: str = os.path.join(CurrentDirectory.current_directory, 'output')
    output_files: str = os.path.join(output_directory, 'devices')
    output_reports: str = os.path.join(output_directory, 'reports')
    output_consolidated: str = os.path.join(output_reports, 'consolidado_final')
