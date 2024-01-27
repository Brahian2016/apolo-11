# Apolo-11: Python Bootcamp final project

Apolo-11 is a simulation project that generates data for NASA devices and generate reports based on the data generated. Project is built using Python and the Tkinter library to create a User Interface to have a better user experience.

## Table of Contents

- [Installation](##Installation)
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

1. Edit [Configuration file](input/configuration.yaml) file as desired:

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
```

There are three different ways to run the program:

```python
#---------------------------------------------------------------------------

# This part is shared among the three ways to run the program:
#range_for_files defines the quantity of files that will be generated during the execution
# If range_for_files is TRUE, an aleatory number will be generated between min_files_per_loop and max_files_per_loop.
# If range_for_files is FALSE, the number of files generated will be equal to max_files_per_loop.

range_for_files: True
min_files_per_loop: 10
max_files_per_loop: 20

#---------------------------------------------------------------------------

# First way to execute program: When you want to execute the program for an specific time:
# infinity_loops must be FALSE
# time_execution_second must be greater than 0

execute_by_time: True
time_execution_second: 5

#---------------------------------------------------------------------------

# Second way to run the program: When you want to have inifity loops, and you want the system to create files indefinitely.
# execute_by_time must be FALSE

infinity_loops: False

#---------------------------------------------------------------------------
# Third way to run the program: When you want to run the program by a number of designated loops
# infinity_loops must be FALSE
# execute_by_time must be FALSE
# num_loop must be greater than 0

num_loops: 2
time_to_create_file: 1

#---------------------------------------------------------------------------

```

2. Go to Terminal and execute "main.py"

```python
jsern@MHT7VD6W7N apolo-11 % /usr/local/bin/python3 /Users/jsern/apolo-11/main.py
```

3. Select "EXECUTE SIMULATION" and wait until simulation gets:

```python
INFO:root:Ending files creation
```

![Alt text](media/image-1.png)

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

![Alt text](media/image-2.png)

## Test plan

In this section we will describe the different types of testing we will perform for the application in order to meet all the requirements specified on the project description file.

### Devices scope

- The program is built to be executed in any laptop using Windows, MacOS and Linux.
- This program is not attempt to be run on mobile devices.

### Testing scope

Testing will be divided in two main categories:

1. Functional testing: On this section we will perform the Boundaries technique to design and execute some test cases about the Inputs and Outputs NASA expects about the system.

2. Unit testing: We will perfom Unit test on the project with some paramaters as coverage around XX%.

### Funtional testing

- We will perform Boundaries technique to design test cases
- All the parameters mentioned below, are listed on the [Configuration file](input/configuration.yaml) where you can update it accordinly.

#### Using execute_by_time

| Scenario             | time_to_create_file | range_for_files | min_files_per_loop | max_files_per_loop | Expected result                                                                                                                                                                                                                              |
| -------------------- | ------------------- | --------------- | ------------------ | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| execute_by_time = 3  | 8                   | TRUE            | 10                 | 20                 | The program will be run for 3 seconds successfully. The quantity of files per each folder will be defined by a random number between 10 and 20, and the quantity of folders created will be the number that the system can reach during that time. `time_to_create_file` will be defined as the time sleep between the creation of each. |
| execute_by_time = 20 | 2                   | FALSE           | N/A                | 16                 | The program will be run for 20 seconds successfully. The quantity of files per each folder will be defined by 16, and the quantity of folders created will be the number that the system can reach during that time. `time_to_create_file` will be defined as the time sleep between the creation of each.                                |
| execute_by_time = 40 | 7                   | TRUE            | 30                 | 55                 | The program will be run for 40 seconds successfully. The quantity of files per each folder will be defined by a random number between 30 and 55, and the quantity of folders created will be the number that the system can reach during that time. `time_to_create_file` will be defined as the time sleep between the creation of each.|


#### Using infinity_loops

| Scenario               | time_to_create_file | range_for_files | min_files_per_loop | max_files_per_loop | Expected result                                                                                                                                                                                                                            |
| ---------------------- | ------------------- | --------------- | ------------------ | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| infinity_loops = True   | 9                   | TRUE            | 15                 | 25                 | The program will be run indefinitely. The quantity of files per each folder will be defined by a random number between 15 and 25, and the quantity of folders created will be the number that the system can reach during the time it is executing. `time_to_create_file` will be defined as the time sleep between the creation of each.|
| infinity_loops = True   | 3                   | FALSE           | N/A                | 54                 | The program will be run indefinitely. The quantity of files per each folder will be defined by 54, and the quantity of folders created will be the number that the system can reach during the time it is executing. `time_to_create_file` will be defined as the time sleep between the creation of each.                                |
| infinity_loops = True   | 6                   | TRUE            | 35                 | 60                 | The program will be run indefinitely. The quantity of files per each folder will be defined by a random number between 35 and 60, and the quantity of folders created will be the number that the system can reach during the time it is executing. `time_to_create_file` will be defined as the time sleep between the creation of each.|


#### Using num_loops

| Scenario       | time_to_create_file | range_for_files | min_files_per_loop | max_files_per_loop | Expected result                                                                                                                                                                                                                       |
| -------------- | ------------------- | --------------- | ------------------ | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| num_loops = 2  | 10                  | TRUE            | 15                 | 25                 | 2 folders were created during the execution. The quantity of files per each folder will be define by a random number between 15 and 25. time_to_create_file will be define the time sleep between the creation of each folder.|
| num_loops = 10 | 5                   | FALSE           | N/A                | 90                | 10 folders were created during the execution. The quantity of files per each folder will be define by 90. time_to_create_file will be define the time sleep between the creation of each folder.                                                                                                                                                                                                                                  |
| num_loops = 20 | 1                   | TRUE            | 35                 | 60                 | 20 folders were created during the execution. The quantity of files per each folder will be define by a random number between 35 and 60. time_to_create_file will be define the time sleep between the creation of each. folder.                                                                                                                                                                                                                                  |
