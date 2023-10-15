#!/usr/bin/python3
"""Defines unittests for models/user.py.

Unittest classes:
    TestUser_instantiation
    TestUser_save
    TestUser_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUser_instantiation(unittest.TestCase):
    """testing instantiation of the User class."""

    def test_for_no_args_instantiates(self):
        self.assertEqual(User, type(User()))

    def test_for_new_instance_stored_in_objects(self):
        self.assertIn(User(), models.storage.all().values())

    def test_if_id_is_public_str(self):
        self.assertEqual(str, type(User().id))

    def test_if_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_if_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_if_email_is_public_str(self):
        self.assertEqual(str, type(User.email))

    def test_if_password_is_public_str(self):
        self.assertEqual(str, type(User.password))

    def test_if_first_name_is_public_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_if_last_name_is_public_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_if_two_users_unique_ids(self):
        user_1 = User()
        user_2 = User()
        self.assertNotEqual(user_1.id, user_2.id)

    def test_for_two_users_different_created_at(self):
        user_1 = User()
        sleep(0.05)
        user_2 = User()
        self.assertLess(user_1.created_at, user_2.created_at)

    def test_for_two_users_different_updated_at(self):
        user_1 = User()
        sleep(0.05)
        user_2 = User()
        self.assertLess(user_1.updated_at, user_2.updated_at)

    def test_for_str_representation(self):
        dt = datetime.now()
        dt_repr = repr(dt)
        usr = User()
        usr.id = "123456"
        usr.created_at = usr.updated_at = dt
        usrstr = usr.__str__()
        self.assertIn("[User] (123456)", usrstr)
        self.assertIn("'id': '123456'", usrstr)
        self.assertIn("'created_at': " + dt_repr, usrstr)
        self.assertIn("'updated_at': " + dt_repr, usrstr)

    def test_for_args_unused(self):
        usr = User(None)
        self.assertNotIn(None, usr.__dict__.values())

    def test_for_instantiation_with_kwargs(self):
        dt = datetime.now()
        dt_iso = dt.isoformat()
        usr = User(id="34567", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(usr.id, "34567")
        self.assertEqual(usr.created_at, dt)
        self.assertEqual(usr.updated_at, dt)

    def test_for_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_save(unittest.TestCase):
    """testing save method of the  class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_for_one_save(self):
        usr = User()
        sleep(0.05)
        first_updated_at = usr.updated_at
        usr.save()
        self.assertLess(first_updated_at, usr.updated_at)

    def test_for_two_saves(self):
        usr = User()
        sleep(0.05)
        first_updated_at = usr.updated_at
        usr.save()
        second_updated_at = usr.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        usr.save()
        self.assertLess(second_updated_at, usr.updated_at)

    def test_for_save_with_arg(self):
        usr = User()
        with self.assertRaises(TypeError):
            usr.save(None)

    def test_for_save_updates_file(self):
        usr = User()
        usr.save()
        usrid = "User." + usr.id
        with open("file.json", "r") as f:
            self.assertIn(usrid, f.read())


class TestUser_to_dict(unittest.TestCase):
    """testing to_dict method of the User class."""

    def test_for_to_dict_type(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_if_to_dict_contains_correct_keys(self):
        usr = User()
        self.assertIn("id", usr.to_dict())
        self.assertIn("created_at", usr.to_dict())
        self.assertIn("updated_at", usr.to_dict())
        self.assertIn("__class__", usr.to_dict())

    def test_if_to_dict_contains_added_attributes(self):
        usr = User()
        usr.middle_name = "Holberton"
        usr.my_number = 98
        self.assertEqual("Holberton", usr.middle_name)
        self.assertIn("my_number", usr.to_dict())

    def test_if_to_dict_datetime_attributes_are_strs(self):
        usr = User()
        usr_dict = usr.to_dict()
        self.assertEqual(str, type(usr_dict["id"]))
        self.assertEqual(str, type(usr_dict["created_at"]))
        self.assertEqual(str, type(usr_dict["updated_at"]))

    def test_for_to_dict_output(self):
        dt = datetime.now()
        usr = User()
        usr.id = "123456"
        usr.created_at = usr.updated_at = dt
        set_dict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(usr.to_dict(), set_dict)

    def test_for_contrast_to_dict_dunder_dict(self):
        usr = User()
        self.assertNotEqual(usr.to_dict(), usr.__dict__)

    def test_for_to_dict_with_arg(self):
        usr = User()
        with self.assertRaises(TypeError):
            usr.to_dict(None)


if __name__ == "__main__":
    unittest.main()
