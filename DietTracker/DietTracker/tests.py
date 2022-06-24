from .DbUtil import *
from django.test import TestCase, TransactionTestCase, LiveServerTestCase
from sqlalchemy import Date, Table, Column, MetaData, Integer, Identity, Text, Numeric, ForeignKey
from sqlalchemy import create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError as bad_brew
import os
import sqlite3

class DatabaseTests(TestCase):
    def setUp(self):
        self.csv_file = os.path.dirname(__file__) + '\csv\RawFoodData.csv'
        self.engine = create_test_engine(log_to_console=False)
        create_database(self.engine)
        try:
            load_foodinfo_csv(self.csv_file, self.engine)
        except sqlite3.IntegrityError or bad_brew:
            print("failed to load csv")

    def test_setup(self):
        food_count = 0
        with self.engine.connect() as conn:
            results = conn.execute(food_info.select())
            for _ in results:
                food_count += 1
        self.assertTrue(food_count > 0)

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
        id = get_id(self.engine, measurements, measurements.c.description, test)
        self.assertEquals(correct, id)

    def test_get_id_not_found(self):
        invalid = "invalid"
        id = get_id(self.engine, measurements, measurements.c.description, invalid)
        self.assertEquals(id, 0)

    def test_add_measurement(self):
        test = "test"
        with self.engine.connect() as conn:
            add_measurement(test, conn)
        id = get_id(self.engine, measurements, measurements.c.description, test)
        self.assertTrue(id > 0)


