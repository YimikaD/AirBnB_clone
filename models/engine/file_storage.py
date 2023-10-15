#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """For storing and retrieving data

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        set_obj = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[set_obj] = obj

    def save(self):
        """Serialize __objects to the JSON file (__file_path)"""
        objectdict = FileStorage.__objects
        objdict = {obj: objectdict[obj].to_dict() for obj in objectdict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objdict, f)

    def reload(self):
        """Deserialize the JSON file (__file_path) to __objects"""
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for obj in objdict.values():
                    clas_name = obj["__class__"]
                    del obj["__class__"]
                    self.new(eval(clas_name)(**obj))
        except FileNotFoundError:
            return
    
    def attributes(self):
        """Returns the valid attributes and their types for classname"""
        attributes = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
            {"place_id": str,
                         "user_id": str,
                         "text": str}
        }
        return attributes

    def classes(self):
        """Returns a dictionary of valid classes and their references"""

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes


