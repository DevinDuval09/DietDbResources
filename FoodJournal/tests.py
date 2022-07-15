from .DbUtil import *
from .views import get_food_json, create_user
from django.test import TestCase, TransactionTestCase, LiveServerTestCase
from django.http.request import HttpRequest
from django.contrib.auth.models import User
from importlib import import_module
from django.conf import settings
from sqlalchemy import Date, Table, Column, MetaData, Integer, Identity, Text, Numeric, ForeignKey
from sqlalchemy import create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError as bad_brew
import os
import sqlite3
import json
from datetime import date

class DatabaseTests(TestCase):
    fixtures = ["users_fixtures.json"]
    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.csv_file = os.path.dirname(__file__) + '\csv\RawFoodData.csv'
        self.engine = create_test_engine(db_name="test_db.sqlite3", log_to_console=False)
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
        user_count = 0
        with self.engine.connect() as conn:
            results = conn.execute(food_info.select())
            #print("\n\n")
            #print(food_info.bind)
            for _ in results:
                food_count += 1
        with self.engine.connect() as conn:
            results2 = conn.execute(measurements.select())
            for _ in results2:
                measurement_count += 1
        with self.engine.connect() as conn:
            results = conn.execute(users.select())
            for _ in results:
                print(_)
                user_count += 1
        #print('\n\n')
        #print(self.user.id)
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

    def test_generate_food_journal(self):
        curr_user = User.objects.create(username="user")
        curr_user.set_password("12345")
        curr_user.save()
        login = self.client.login(username="user", password="12345")
        self.assertTrue(login)
        food = {"qty_input": 2, "food_id": 1, "date_input": date.today()}
        post = self.client.post(f"/FoodJournal/user/", data=food, follow=True)
        with self.engine.connect() as conn:
            stmt = food_eaten.select()
            results = conn.execute(stmt)
            for row in results:
                print(row)
    
        self.assertEquals(post.status_code, 200)




