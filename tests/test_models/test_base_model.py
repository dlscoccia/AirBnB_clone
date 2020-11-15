#!/usr/bin/python3
"""Base Model Class Test Module"""
import unittest
from datetime import timedelta  # for isoformat and fromisoformat
from datetime import datetime  # for strftime
from datetime import date
from time import sleep
import uuid
from models import storage
from models.base_model import BaseModel


class BaseModelTest(unittest.TestCase):
    '''Class to test the BaseModel Class'''

    def test_0_id(self):
        '''If the id of the an instance is correct'''

        my_model_0 = BaseModel()
        my_model_1 = BaseModel()
        my_model_2 = BaseModel()

        # 1) check if id len is 36 including '-'
        self.assertEqual(len(my_model_0.id), 36)
        self.assertEqual(len(my_model_1.id), 36)
        self.assertEqual(len(my_model_2.id), 36)

        # 2) check if the type of the id is str
        self.assertEqual(type(my_model_0.id), str)
        self.assertEqual(type(my_model_1.id), str)
        self.assertEqual(type(my_model_2.id), str)

        # 3) check if all id's are different
        self.assertNotEqual(my_model_0.id, my_model_1.id)
        self.assertNotEqual(my_model_0.id, my_model_2.id)
        self.assertNotEqual(my_model_1.id, my_model_2.id)

    def test_1_created_at(self):
        '''If the date of creation of the instance is correct'''

        my_model_0 = BaseModel()
        my_model_1 = BaseModel()
        my_model_2 = BaseModel()

        # 1) Checks if the creation date is a datetime object
        self.assertEqual(type(my_model_0.created_at), datetime)
        self.assertEqual(type(my_model_1.created_at), datetime)
        self.assertEqual(type(my_model_2.created_at), datetime)

        # 2) Checks if when an instance is created, created_at == updated_at
        self.assertEqual(my_model_0.created_at, my_model_0.updated_at)
        self.assertEqual(my_model_1.created_at, my_model_1.updated_at)
        self.assertEqual(my_model_2.created_at, my_model_2.updated_at)

        # 3) Checks if creation date is set with the creation of the instance
        actual_date = datetime.now()
        time_spread = timedelta(seconds=1)

        self.assertTrue(actual_date - my_model_0.created_at < time_spread)
        self.assertTrue(actual_date - my_model_1.created_at < time_spread)
        self.assertTrue(actual_date - my_model_2.created_at < time_spread)

    def test_2_save(self):
        '''If updated_at works when save() is called'''

        b1 = BaseModel()
        crtime = b1.created_at
        uptime = b1.updated_at
        sleep(0.1)
        b1.save()
        self.assertTrue(crtime == b1.created_at)
        self.assertFalse(uptime == crtime)
        self.assertFalse(uptime == b1.updated_at)

    def test_3_str(self):
        '''If str method work as expected'''

        my_model_0 = BaseModel()
        my_model_1 = BaseModel()
        my_model_2 = BaseModel()

        str_model_0 = "[" + str(type(my_model_0).__name__) + "] (" + \
                      str(my_model_0.id) + ") " + str(my_model_0.__dict__)
        str_model_1 = "[" + str(type(my_model_1).__name__) + "] (" + \
                      str(my_model_1.id) + ") " + str(my_model_1.__dict__)
        str_model_2 = "[" + str(type(my_model_2).__name__) + "] (" + \
                      str(my_model_2.id) + ") " + str(my_model_2.__dict__)

        self.assertEqual(str(my_model_0), str_model_0)
        self.assertEqual(my_model_1.__str__(), str_model_1)
        self.assertEqual(my_model_2.__str__(), str_model_2)

    def test_4_to_dict(self):
        '''If to_dict method work correctly'''

        my_model_0 = BaseModel()
        my_model_1 = BaseModel()
        my_model_2 = BaseModel()

        dict_0 = my_model_0.to_dict()
        dict_1 = my_model_1.to_dict()
        dict_2 = my_model_2.to_dict()

        # 1) Checks if is a dictionary
        self.assertEqual(type(dict_0), dict)
        self.assertEqual(type(dict_1), dict)
        self.assertEqual(type(dict_2), dict)

        # 2) Checks if the creation date is in ISO 8601 format
        date_0 = my_model_0.created_at
        date_1 = my_model_1.created_at
        date_2 = my_model_2.created_at

        str_date_0 = date_0.strftime("%Y-%m-%dT%H:%M:%S.%f")
        str_date_1 = date_1.strftime("%Y-%m-%dT%H:%M:%S.%f")
        str_date_2 = date_2.strftime("%Y-%m-%dT%H:%M:%S.%f")

        self.assertEqual(dict_0['created_at'], str_date_0)
        self.assertEqual(dict_1['created_at'], str_date_1)
        self.assertEqual(dict_2['created_at'], str_date_2)

        # 3) Checks if the update date is in ISO 8601 format
        date_0 = my_model_0.updated_at
        date_1 = my_model_1.updated_at
        date_2 = my_model_2.updated_at

        str_date_0 = date_0.strftime("%Y-%m-%dT%H:%M:%S.%f")
        str_date_1 = date_1.strftime("%Y-%m-%dT%H:%M:%S.%f")
        str_date_2 = date_2.strftime("%Y-%m-%dT%H:%M:%S.%f")

        self.assertEqual(dict_0['created_at'], str_date_0)
        self.assertEqual(dict_1['created_at'], str_date_1)
        self.assertEqual(dict_2['created_at'], str_date_2)

        # 4) Checks if the __class__ is in dict

        class_0 = type(my_model_0).__name__
        class_1 = type(my_model_1).__name__
        class_2 = type(my_model_2).__name__

        self.assertEqual(dict_0['__class__'], class_0)
        self.assertEqual(dict_1['__class__'], class_1)
        self.assertEqual(dict_2['__class__'], class_2)

    def test_5_kwargs(self):
        '''If object is correctly created with kwargs'''

        my_id = str(uuid.uuid4())
        actual_date = datetime.now().isoformat()
        Mod1 = BaseModel(id=my_id, created_at=actual_date,
                         updated_at=actual_date, __class__='BaseModel',
                         test='my_test')
        self.assertTrue(isinstance(Mod1, BaseModel))
        self.assertEqual(str, type(Mod1.id))
        self.assertEqual(datetime, type(Mod1.created_at))
        self.assertEqual(datetime, type(Mod1.updated_at))

        # Check that __class__ atribute is not created
        self.assertFalse('__class__' in Mod1.__dict__)

        # Check if a custom atribute is created
        self.assertTrue('test' in Mod1.__dict__)
        self.assertTrue('my_test' in Mod1.__dict__.values())

    def test_6_BaseModel_type_args(self):
        '''If object args are of the correct type'''

        my_model_0 = BaseModel()

        attbs = storage.class_attributes()['BaseModel']

        for key, value in attbs.items():
            attr = getattr(my_model_0, key)
            self.assertEqual(type(attr), value)
