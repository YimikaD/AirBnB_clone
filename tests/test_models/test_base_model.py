#!/usr/bin/python3
"""Defines unittests for models/base_model.py.

Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """For testing instantiation of the BaseModel class."""

    def test_for_no_args_instantiation(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    #def test_new_instance_stored_in_objects(self):
        #self.assertIn(BaseModel(), models.storage.all().values())

    def test_if_id_is_string(self):
        self.assertEqual(str, type(BaseModel().id))

    def tes_if_created_at_is_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_if_updated_at_is_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_for_two_instance_unique_ids(self):
        sample1 = BaseModel()
        sample2 = BaseModel()
        self.assertNotEqual(sample1.id, sample2.id)

    def test_for_two_instance_created_at(self):
        sample1 = BaseModel()
        sleep(0.05)
        sample2 = BaseModel()
        self.assertLess(sample1.created_at, sample2.created_at)

    def test_for_two_instance_updated_at(self):
        sample1 = BaseModel()
        sleep(0.05)
        sample2 = BaseModel()
        self.assertLess(sample1.updated_at, sample2.updated_at)

    def test_for_string_representation(self):
        dt = datetime.now()
        dt_repr = repr(dt)
        sample = BaseModel()
        sample.id = "6789"
        sample.created_at = sample.updated_at = dt
        sample_str = sample.__str__()
        self.assertIn("[BaseModel] (6789)", sample_str)
        self.assertIn("'id': '6789'", sample_str)
        self.assertIn("'created_at': " + dt_repr, sample_str)
        self.assertIn("'updated_at': " + dt_repr, sample_str)

    def test_for_args_unused(self):
        sample = BaseModel(None)
        self.assertNotIn(None, sample.__dict__.values())

    def test_for_instantiation_with_kwargs(self):
        dt = datetime.now()
        dt_iso = dt.isoformat()
        sample = BaseModel(id="12345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(sample.id, "12345")
        self.assertEqual(sample.created_at, dt)
        self.assertEqual(sample.updated_at, dt)

    def test_for_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_for_instantiation_with_args_and_kwargs(self):
        dt = datetime.now()
        dt_iso = dt.isoformat()
        sample = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(sample.id, "345")
        self.assertEqual(sample.created_at, dt)
        self.assertEqual(sample.updated_at, dt)


class TestBaseModel_save(unittest.TestCase):
    """For testing save method of the BaseModel class."""

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

    def test_one_save(self):
        sample = BaseModel()
        sleep(0.05)
        one_updated_at = sample.updated_at
        sample.save()
        self.assertLess(one_updated_at, sample.updated_at)

    def test_two_saves(self):
        sample = BaseModel()
        sleep(0.05)
        one_updated_at = sample.updated_at
        sample.save()
        two_updated_at = sample.updated_at
        self.assertLess(one_updated_at, two_updated_at)
        sleep(0.05)
        sample.save()
        self.assertLess(second_updated_at, sample.updated_at)

    def test_for_save_with_arg(self):
        sample = BaseModel()
        with self.assertRaises(TypeError):
            sample.save(None)

    def test_for_save_updates_file(self):
        sample = BaseModel()
        sample.save()
        sample_id = "BaseModel." + sample.id
        with open("file.json", "r") as f:
            self.assertIn(sample_id, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """For testing to_dict method of the BaseModel class."""

    def test_for_to_dict_type(self):
        sample = BaseModel()
        self.assertTrue(dict, type(sample.to_dict()))

    def test_for_to_dict_containing_correct_keys(self):
        sample = BaseModel()
        self.assertIn("id", sample.to_dict())
        self.assertIn("created_at", sample.to_dict())
        self.assertIn("updated_at", sample.to_dict())
        self.assertIn("__class__", sample.to_dict())

    def test_for_to_dict_containing_added_attributes(self):
        sample = BaseModel()
        sample.name = "Holberton"
        sample.my_number = 98
        self.assertIn("name", sample.to_dict())
        self.assertIn("my_number", sample.to_dict())

    def test_for_to_dict_datetime_attributes_are_strings(self):
        sample = BaseModel()
        sample_dict = sample.to_dict()
        self.assertEqual(str, type(sample_dict["created_at"]))
        self.assertEqual(str, type(sample_dict["updated_at"]))

    def test_for_to_dict_output(self):
        dt = datetime.now()
        sample = BaseModel()
        sample.id = "6789"
        sample.created_at = sample.updated_at = dt
        retun_dict = {
            'id': '6789',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(sample.to_dict(), return_dict)

    def test_for_contrasting_to_dict_attributes(self):
        sample = BaseModel()
        self.assertNotEqual(sample.to_dict(), sample.__dict__)

    def test_for_to_dict_with_arg(self):
        sample = BaseModel()
        with self.assertRaises(TypeError):
            sample.to_dict(None)


if __name__ == "__main__":
    unittest.main()
