from pathlib import Path

class CurrentDirectory:
    '''Una clase que representa el directorio de trabajo actual.'''
    current_directory: Path = Path.cwd()
    
class PathDataRaw:
    '''Una clase que representa el directorio data.'''
    data_directory: Path = CurrentDirectory.current_directory / 'data'

class PathInputRaw:
    '''Una clase que representa el directorio input.'''
    input_directory: Path = CurrentDirectory.current_directory / 'input'
    
class PathOutputRaw:
    '''Una clase que representa el directorio output.'''
    output_directory: Path = CurrentDirectory.current_directory / 'output'

