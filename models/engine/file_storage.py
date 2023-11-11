#!/usr/bin/python3
"""FileStorage ModelAndclass."""

import json
import os
from json.decoder import JSONDecodeError
from models.base_model import BaseModel
from datetime import datetime


class FileStorage:

    """ Private variables"""
    __file_path = "file.json"
    __objects = {}

    def __init__(self):
        """OurConstructor"""
        pass

    def all(self):
        """Dictionary __objects AndReturn all instances stored"""
        return FileStorage.__objects

    def new(self, obj):
        """setOURobjects"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """ JSONFile Creation As fs_f and dy_d """
        with open(FileStorage.__file_path, "w", encoding="utf-8") as fs:
            dy = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
            json.dump(dy, fs)

    def classes(self):
        """References"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes

    def reload(self):
        """ReloadStoredObjects as fs_f and obj_dicst is obj_dict"""
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as fs:
            obj_dicst = json.load(fs)
            obj_dicst = {k: self.classes()[v["__class__"]](**v)
                         for k, v in obj_dicst.items()}
            FileStorage.__objects = obj_dicst

    def Attributes(self):
        """AttributesTypes"""
        Attributes = {
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
        return Attributes
