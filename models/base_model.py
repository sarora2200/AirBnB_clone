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
        """return string representation of of basemodel instance"""
       className = self.__class__.__name__
        return "[{}] ({}) {}".format(className, self.id, self.__dict__)


