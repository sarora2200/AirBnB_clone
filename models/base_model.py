#!/usr/bin/python3
"""the base model script"""

import uuid
import models
from datetime import datetime


class BaseModel:

    """class that defines all common attributes/methods for other classes"""

    def __init__(self, *args, **kwargs):
        """initialization of base model
        Args:
            -*args: arguments
            -**kwargs: dictionary of key-values arguments
        """

        if kwargs:
            datetime_format = "%Y-%m-%dT%H:%M:%S.%f"
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                elif key == 'created_at':
                    self.created_at = datetime.strptime(
                        kwargs['created_at'], datetime_format)
                elif key == 'updated_at':
                    self.updated_at = datetime.strptime(
                        kwargs['updated_at'], datetime_format)
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """return string representation of basemodel instance"""

        clsName = self.__class__.__name__
        return "[{}] ({}) {}".format(clsName, self.id, self.__dict__)

    def save(self):
        """Updates the attribute updated_at with the current datetime"""

        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values
        of __dict__ of the instance"""

        My_dict = self.__dict__.copy()
        My_dict['updated_at'] = self.updated_at.isoformat()
        My_dict['created_at'] = self.created_at.isoformat()
        My_dict['__class__'] = self.__class__.__name__
        # My_dict = dict()
        # My_dict['__class__'] = self.__class__.__name__
        # for key, value in self.__dict__.items():
        #    if key in ('created_at', 'updated_at'):
        #        My_dict[key] = value.isoformat()
        #    else:
        #        My_dict[key] = value
        return My_dict
        # My_dict = dict()
        # My_dict['__class__'] = self.__class__.__name__
        # for key, value in self.__dict__.items():
        #    if type(value) is datetime:
        #        My_dict[key] = value.isoformat()
        #    else:
        #        My_dict[key] = value
        # return My_dict
