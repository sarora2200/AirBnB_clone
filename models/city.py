#!/usr/bin/python3
"""Model creates City class """

from models.base_model import BaseModel


class City(BaseModel):
    """class to manage state objects"""

    state_id = ""
    name = ""
