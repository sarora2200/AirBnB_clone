#!/usr/bin/python3
"""Module creates a User class"""
from models.base_model import BaseModel


class User(BaseModel):
    """class to manage user objects"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
