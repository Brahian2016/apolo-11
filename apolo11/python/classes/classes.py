from pydantic import BaseModel, Field, root_validator
from typing import ClassVar
import hashlib
import random
from apolo11.python.utils.parameters import get_parameters
from datetime import datetime

diccionary = get_parameters()


class Mission(BaseModel):
    """Class to obtain a random mission name
    """
    name: str = Field(default_factory=lambda: random.choice(diccionary['missionsConfig']))


class DeviceType(BaseModel):
    """Class that defines device type and device status
    """
    device_type: str = Field(default_factory=lambda: random.choice(diccionary['deviceTypeConfig']))
    status: str = Field(default_factory=lambda: random.choice(diccionary['deviceStatusConfig']))


class Device(Mission, DeviceType):
    """Generate device hash and file structure

    :param DeviceType: Used for taking the device type
    :type DeviceType: class
    :param Mission: Used for taking a random Mission name
    :type Mission: class
    """
    file_counter: ClassVar[int] = 1  # Class variable for the counter

    _date: str
    _hash: str
    _file_number: int

    __annotations__ = {"hash": str, "file_counter": ClassVar[int], "file_number": int, "date": str}

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self, value):
        self._hash = value

    @property
    def file_number(self):
        return self._file_number

    @file_number.setter
    def file_number(self, value):
        self._file_number = value

    @root_validator(pre=True)
    def calculate_hash(cls, values):
        """Calculate hash during validation"""
        date = datetime.now().strftime("%d%m%y%H%M%S")
        name = values.get("name", "")
        device_type = values.get("device_type", "")
        status = values.get("status", "")

        if name == "UNKN":
            values["hash"] = ''
        else:
            data: str = f"{date}{name}{device_type}{status}"
            values["hash"] = hashlib.md5(data.encode()).hexdigest()

        values["file_number"] = cls.file_counter  # Assign file number
        values["date"] = date  # Initialize date
        cls.file_counter += 1  # Increment the counter only once

        return values

    def get_description(self):
        """Get a description of the object.

        Returns:
        dict: A dictionary containing the following information:
        - "date": The date associated with the object.
        - "mission": The name of the mission.
        - "device_type": The type of device.
        - "device_status": The status of the device.
        - "hash": The hash associated with the object.
        - "file_number": The file number associated with the object.
        """
        return {
            "date": self.date,
            "mission": self.name,
            "device_type": self.device_type,
            "device_status": self.status,
            "hash": self.hash,
            "file_number": self.file_number
        }
