#!/usr/bin/python3
"""Unittesting for models/engine/file_storage.py.

Unittest classes(2):
    TestFileStorage_instantiation
    TestFileStorage_methods
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_instantiation(unittest.TestCase):
    """Testing instantiation of the FileStorage class."""

    def test_for_FileStorage_instantiation_with_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_for_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_for_FileStorage_file_path_is_private_string(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_for_FileStorage_objects_is_private_dictionary(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_for_storage_initialization(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Testing methods of the FileStorage class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all_method(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_method_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new_method(self):
        bml = BaseModel()
        usr = User()
        ste = State()
        ple = Place()
        cy = City()
        amy = Amenity()
        rvw = Review()
        models.storage.new(bml)
        models.storage.new(usr)
        models.storage.new(ste)
        models.storage.new(ple)
        models.storage.new(cy)
        models.storage.new(amy)
        models.storage.new(rvw)
        self.assertIn("BaseModel." + bml.id, models.storage.all().keys())
        self.assertIn(bml, models.storage.all().values())
        self.assertIn("User." + usr.id, models.storage.all().keys())
        self.assertIn(usr, models.storage.all().values())
        self.assertIn("State." + ste.id, models.storage.all().keys())
        self.assertIn(ste, models.storage.all().values())
        self.assertIn("Place." + ple.id, models.storage.all().keys())
        self.assertIn(ple, models.storage.all().values())
        self.assertIn("City." + cy.id, models.storage.all().keys())
        self.assertIn(cy, models.storage.all().values())
        self.assertIn("Amenity." + amy.id, models.storage.all().keys())
        self.assertIn(amy, models.storage.all().values())
        self.assertIn("Review." + rvw.id, models.storage.all().keys())
        self.assertIn(rvw, models.storage.all().values())

    def test_new_method_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save_method(self):
        bml = BaseModel()
        usr = User()
        ste = State()
        ple = Place()
        cy = City()
        amy = Amenity()
        rvw = Review()
        models.storage.new(bml)
        models.storage.new(usr)
        models.storage.new(ste)
        models.storage.new(ple)
        models.storage.new(cy)
        models.storage.new(amy)
        models.storage.new(rvw)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + bml.id, save_text)
            self.assertIn("User." + usr.id, save_text)
            self.assertIn("State." + ste.id, save_text)
            self.assertIn("Place." + ple.id, save_text)
            self.assertIn("City." + cy.id, save_text)
            self.assertIn("Amenity." + amy.id, save_text)
            self.assertIn("Review." + rvw.id, save_text)

    def test_save_method_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload_method(self):
        bml = BaseModel()
        usr = User()
        ste = State()
        ple = Place()
        cy = City()
        amy = Amenity()
        rvw = Review()
        models.storage.new(bml)
        models.storage.new(usr)
        models.storage.new(ste)
        models.storage.new(ple)
        models.storage.new(cy)
        models.storage.new(amy)
        models.storage.new(rvw)
        models.storage.save()
        models.storage.reload()
        objects = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + bml.id, objects)
        self.assertIn("User." + usr.id, objects)
        self.assertIn("State." + ste.id, objects)
        self.assertIn("Place." + ple.id, objects)
        self.assertIn("City." + cy.id, objects)
        self.assertIn("Amenity." + amy.id, objects)
        self.assertIn("Review." + rvw.id, objects)

    def test_reload_method_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
