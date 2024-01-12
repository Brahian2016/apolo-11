import os


class CurrentDirectory:
    '''Una clase que representa el directorio de trabajo actual.'''
    current_directory: os = os.getcwd()
    
class PathDataRaw:
    '''Una clase que representa el directorio data.'''
    data_directory: os = os.path.join(CurrentDirectory.current_directory, 'data')

class PathInputRaw:
    '''Una clase que representa el directorio input.'''
    input_directory: os = os.path.join(CurrentDirectory.current_directory, 'input')
    configuration_file: os = os.path.join(input_directory, 'configuration.yaml')
    
class PathOutputRaw:
    '''Una clase que representa el directorio output.'''
    output_directory: os = os.path.join(CurrentDirectory.current_directory, 'output')
    output_files: os = os.path.join(output_directory, 'devices')

