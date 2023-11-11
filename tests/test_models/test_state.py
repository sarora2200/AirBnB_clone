#!/usr/bin/python3
"""It Defines unittests for models/state.py.
Unittest classes:
    TestState_instantiation
    TestState_save
    TestState_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestStateInstantiation(unittest.TestCase):
    """Its Unittests for testing instantiation of the State class."""

    def test_No_Args_Instantiates(self):
        self.assertEqual(State, type(State()))

    def test_New_Instance_Stored_In_Objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_Id_Is_Public_Str(self):
        self.assertEqual(str, type(State().id))

    def test_Created_At_Is_Public_Datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_Updated_At_Is_Public_Datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_Name_Is_Public_Class_Attribute(self):
        St = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(St))
        self.assertNotIn("name", St.__dict__)

    def test_Two_States_Unique_Ids(self):
        St1 = State()
        St2 = State()
        self.assertNotEqual(St1.id, St2.id)

    def test_Two_States_Different_Created_At(self):
        St1 = State()
        sleep(0.05)
        St2 = State()
        self.assertLess(St1.created_at, St2.created_at)

    def test_Two_States_Different_Updated_At(self):
        St1 = State()
        sleep(0.05)
        St2 = State()
        self.assertLess(St1.updated_at, St2.updated_at)

    def test_Str_Representation(self):
        Dt = datetime.today()
        Dt_repr = repr(Dt)
        St = State()
        St.id = "123456"
        St.created_at = St.updated_at = Dt
        Ststr = St.__str__()
        self.assertIn("[State] (123456)", Ststr)
        self.assertIn("'id': '123456'", Ststr)
        self.assertIn("'created_at': " + Dt_repr, Ststr)
        self.assertIn("'updated_at': " + Dt_repr, Ststr)

    def test_Args_Unused(self):
        St = State(None)
        self.assertNotIn(None, St.__dict__.values())

    def test_Instantiation_With_Kwargs(self):
        Dt = datetime.today()
        Dt_iso = Dt.isoformat()
        St = State(id="345", created_at=Dt_iso, updated_at=Dt_iso)
        self.assertEqual(St.id, "345")
        self.assertEqual(St.created_at, Dt)
        self.assertEqual(St.updated_at, Dt)

    def test_Instantiation_With_None_Kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_Save(unittest.TestCase):
    """it Unittests for testing save method of the State class."""

    @classmethod
    def SetUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def TearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_One_Save(self):
        St = State()
        sleep(0.05)
        First_updated_at = St.updated_at
        St.save()
        self.assertLess(First_updated_at, St.updated_at)

    def test_Two_Saves(self):
        St = State()
        sleep(0.05)
        First_updated_at = St.updated_at
        St.save()
        Second_updated_at = St.updated_at
        self.assertLess(First_updated_at, Second_updated_at)
        sleep(0.05)
        St.save()
        self.assertLess(Second_updated_at, St.updated_at)

    def test_Save_With_Arg(self):
        St = State()
        with self.assertRaises(TypeError):
            St.save(None)

    def test_Save_Updates_File(self):
        St = State()
        St.save()
        Stid = "State." + St.id
        with open("file.json", "r") as f:
            self.assertIn(Stid, f.read())


class TestState_To_Dict(unittest.TestCase):
    """it Unittests for testing to_dict method of the State class."""

    def test_To_Dict_Type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_To_Dict_Contains_Correct_Keys(self):
        St = State()
        self.assertIn("id", St.to_dict())
        self.assertIn("created_at", St.to_dict())
        self.assertIn("updated_at", St.to_dict())
        self.assertIn("__class__", St.to_dict())

    def test_To_Dict_Contains_Added_Attributes(self):
        St = State()
        St.middle_name = "Holberton"
        St.my_number = 98
        self.assertEqual("Holberton", St.middle_name)
        self.assertIn("my_number", St.to_dict())

    def test_To_Dict_Datetime_Attributes_Are_Strs(self):
        St = State()
        St_dict = St.to_dict()
        self.assertEqual(str, type(St_dict["id"]))
        self.assertEqual(str, type(St_dict["created_at"]))
        self.assertEqual(str, type(St_dict["updated_at"]))

    def test_To_Dict_Output(self):
        Dt = datetime.today()
        St = State()
        St.id = "123456"
        St.created_at = St.updated_at = Dt
        Tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': Dt.isoformat(),
            'updated_at': Dt.isoformat(),
        }
        self.assertDictEqual(St.to_dict(), Tdict)

    def test_contrast_To_Dict_Dunder_Dict(self):
        St = State()
        self.assertNotEqual(St.to_dict(), St.__dict__)

    def test_To_Dict_With_Arg(self):
        St = State()
        with self.assertRaises(TypeError):
            St.to_dict(None)


if __name__ == "__main__":
    unittest.main()
