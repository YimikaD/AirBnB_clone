#!/usr/bin/python3
"""Defines the BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """This represents the BaseModel(super class) of the AirBnB project."""

    def __init__(self, *args, **kwargs):
        """To initialize a new BaseModel instance.

        Args:
            *args (any): Not to be used.
            **kwargs (dict): Dictionary of Key/value pairs of attributes.
        """
        Time_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if len(kwargs) != 0:
            for key1, key2 in kwargs.items():
                if key1 == "created_at" or key1 == "updated_at":
                    self.__dict__[key1] = datetime.strptime(key2, Time_format)
                else:
                    self.__dict__[key1] = key2
        else:
            models.storage.new(self)

    def save(self):
        """To update public instance updated_at with the current datetime."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """To return the dictionary of the BaseModel instances which
        includes the key/value pair of __dict__
        """
        return_dict = self.__dict__.copy()
        #return_dict["__class__"] = self.__class__.__name__
        return_dict["created_at"] = self.created_at.isoformat()
        return_dict["updated_at"] = self.updated_at.isoformat()
        return_dict["__class__"] = self.__class__.__name__
        return return_dict

    def __str__(self):
        """To return  the string representation of the BaseModel instance."""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)
