from .DbUtil import *
from .models import *
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
from .models import csv_to_model, Foods, Measurements, Meals

class DatabaseTests(TestCase):
    fixtures = ["users_fixtures.json"]
    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.csv_file = os.path.dirname(__file__) + '\csv\RawFoodData.csv'
        try:
            csv_to_model(self.csv_file)
        except sqlite3.IntegrityError or bad_brew:
            print("failed to load csv")

    def tearDown(self):
        pass
    def test_setup(self):
        food_count = 0
        measurement_count = 0
        user_count = 0
        for _ in Foods.objects.all():
            food_count += 1
        for _ in Measurements.objects.all():
            measurement_count += 1
        self.assertTrue(food_count > 0)
        self.assertTrue(measurement_count > 0)

    '''def test_get_id(self):
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
        self.assertTrue(id > 0)'''

    def test_get_food_model(self):
        test = "pork shoulder"
        test_dict = get_food_model(test)
        self.assertEquals(test, test_dict["description"])

    def test_get_food_json(self):
        test1 = "tofu"
        test2 = "90% ground beef"
        test3 = "pinto beans"
        tests = [test1, test2, test3]
        for test in tests:
            food = Foods.create(test, 1, 1, 1, 1, 1, 1, Measurements.objects.get(id=1))
            food.save()
            request = HttpRequest()
            request.method = "GET"
            request.path = "FoodJournal/get_food_json/" + test
            js = get_food_json(request, test)
            data = json.loads(js.getvalue().decode())
            self.assertEquals(test, data["description"])

    def test_get_food_json_not_found(self):
        test1 = "plastic"
        test2 = "90% not food"
        test3 = "mercedes benz"
        tests = [test1, test2, test3]
        for test in tests:
            request = HttpRequest()
            request.method = "GET"
            request.path = "FoodJournal/get_food_json/" + test
            js = get_food_json(request, test)
            data = json.loads(js.getvalue().decode())
            self.assertTrue(test in data["error"])

    def test_generate_food_journal(self):
        curr_user = User.objects.create(username="user")
        curr_user.set_password("12345")
        curr_user.save()
        login = self.client.login(username="user", password="12345")
        self.assertTrue(login)
        food = {"qty_input": 2, "food_id": 1, "date_input": date.today()}
        post = self.client.post(f"/FoodJournal/user/", data=food, follow=True)
        self.assertEquals(post.status_code, 200)

    def test_add_food_form(self):
        pass




