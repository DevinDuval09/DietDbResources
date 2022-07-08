from .DbUtil import *
from .views import get_food_json
from django.test import TestCase, TransactionTestCase, LiveServerTestCase
from django.http.request import HttpRequest
from sqlalchemy import Date, Table, Column, MetaData, Integer, Identity, Text, Numeric, ForeignKey
from sqlalchemy import create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError as bad_brew
import os
import sqlite3
import json

class DatabaseTests(TestCase):
    def setUp(self):
        self.csv_file = os.path.dirname(__file__) + '\csv\RawFoodData.csv'
        self.engine = create_engine("sqlite:///file:test_db?mode=memory&cache=shared&uri=true", future=True)
        create_database(self.engine)
        try:
            load_foodinfo_csv(self.csv_file, self.engine)
        except sqlite3.IntegrityError or bad_brew:
            print("failed to load csv")

    def tearDown(self):
        reset_db(engine=self.engine, load_csv=True)

    def test_setup(self):
        food_count = 0
        measurement_count = 0
        with self.engine.connect() as conn:
            results = conn.execute(food_info.select())
            for _ in results:
                food_count += 1
        with self.engine.connect() as conn:
            results2 = conn.execute(measurements.select())
            for _ in results2:
                measurement_count += 1
        self.assertTrue(food_count > 0)
        self.assertTrue(measurement_count > 0)

    def test_get_id(self):
        test = "test"
        correct = 0
        s = select(measurements)
        with self.engine.connect() as conn:
            conn.execute(measurements.insert().values(description=test))
            conn.commit()
            results = conn.execute(s)
            for row in results:
                correct += 1
        id = get_id(measurements, measurements.c.description, test, self.engine)
        self.assertEquals(correct, id)

    def test_get_id_not_found(self):
        invalid = "invalid"
        id = get_id(measurements, measurements.c.description, invalid, self.engine)
        self.assertEquals(id, 0)

    def test_add_measurement(self):
        test = "test"
        with self.engine.connect() as conn:
            add_measurement(test, conn)
        id = get_id(measurements, measurements.c.description, test, self.engine)
        self.assertTrue(id > 0)

    def test_get_food_dict(self):
        test = "tofu"
        tofu_dict = get_food_dict(test, self.engine)
        self.assertEquals(test, tofu_dict['description'])

    def test_get_food_json(self):
        test = "tofu"
        request = HttpRequest()
        request.method = "GET"
        request.path = "FoodJournal/get_food_json/" + test
        js = get_food_json(request, test)
        data = json.loads(js.getvalue().decode())
        self.assertEquals(test, data["description"])


