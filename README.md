# Apolo-11: Python Bootcamp final project

Apolo-11 is a simulation project that generates data for NASA devices and generate reports based on the data generated. Project is built using Python and the Tkinter library to create a User Interface to have a better user experience.

## Table of Contents

- [Installation](###Installation)
- [Usage](##usage)
- [Examples](##Examples)



## Installation
In order to install Apolo-11 and all the dependencies, you can user this command:

```python 
pip install apolo-11 
```

## Usage

1. Configure "configuration.yaml" with your values 

2. Go to "main.py" path and execute the file using the Terminal: [python] + [full path]/main.py

## Examples
1. Edit configuration file as desired:

```python
Missions:
  - ORBONE
  - CLNM
  - TMRS
  - GALAXONE
  - UNKN
DeviceType:
  - Satellite
  - Spacecraft
  - Spacesuit
  - Unknown
DeviceStatus:
  - excellent
  - good
  - warning
  - faulty
  - killed
  - unknown
range_for_files: True
min_files_per_loop: 10
max_files_per_loop: 20
infinity_loops: False
num_loops: 2
time_to_create_file: 1
execute_by_time: True
time_execution_second: 5
```
2. Go to Terminal and execute "main.py"
```python
jsern@MHT7VD6W7N apolo-11 % /usr/local/bin/python3 /Users/jsern/apolo-11/main.py
```

3. Select "EXECUTE SIMULATION" and wait until simulation gets:

```python
INFO:root:Ending files creation
```

4. After simulation finish, you should be able to generate data for reporting using "EXECUTE REPORT":

```python
INFO:root:Starting reporting generation...
```

5. Once the reports are generated you will see:

```python
INFO:root:Reports executed.
```
6. User can click on exit and message displayed is:

```python
INFO:root:Aplication closed.
```
7. User will see all the data generated in "Reports" folder




