from .DbUtil import *
from .models import *
from .views import get_food_json, create_user
from django.test import TestCase, TransactionTestCase, LiveServerTestCase
from django.http.request import HttpRequest
from django.contrib.auth.models import User
from importlib import import_module
from django.conf import settings
from django.db import transaction
from sqlalchemy import Date, Table, Column, MetaData, Integer, Identity, Text, Numeric, ForeignKey
from sqlalchemy import create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError as bad_brew
import os
import sqlite3
import json
from datetime import date, timedelta
from .models import csv_to_model, Foods, Measurements, Meals

class FoodJournalTests(TestCase):
    fixtures = ["users_fixtures.json"]
    def setUp(self):
        food_int = 100
        self.user = User.objects.get(pk=1)
        self.csv_file = os.path.dirname(__file__) + '\csv\RawFoodData.csv'
        try:
            csv_to_model(self.csv_file)
        except sqlite3.IntegrityError or bad_brew:
            print("failed to load csv")
        with transaction.atomic():
            test_food = Foods.create("test_food", food_int, food_int, food_int, food_int, food_int, food_int, Measurements.objects.get(pk=1))
            test_food.save()
        self.test_food = Foods.objects.get(description="test_food")
        self.food_int = food_int

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

    def test_Mealsview_post(self):
        curr_user = User.objects.create(username="user")
        curr_user.set_password("12345")
        curr_user.save()
        login = self.client.login(username="user", password="12345")
        self.assertTrue(login)
        food = {"qty_input": 2, "food_id": 1, "date_input": date.today()}
        post = self.client.post(f"/FoodJournal/user/", data=food, follow=True)
        self.assertEquals(post.status_code, 200)

    def test_Mealsview(self):
        DEFAULT_DAYS_BACK = 7
        curr_user = User.objects.create(username="user")
        curr_user.set_password("12345")
        curr_user.save()
        login = self.client.login(username="user", password="12345")
        self.assertTrue(login)
        dt = date(2022, 7, 1)
        dt_strings = []
        food = Foods.objects.get(pk=1)
        for num in range(DEFAULT_DAYS_BACK):
            delta = timedelta(days=num)
            test_date = dt - delta
            meal = Meals.create(food, num + 1, test_date, curr_user)
            meal.save()
            dt_strings.append(test_date.strftime('%B %d, %Y').replace(" 0", " "))
        response = self.client.get(f"/FoodJournal/user/2022-06-25/2022-07-01/")
        self.assertEquals(response.status_code, 200)
        for date_string in dt_strings:
            self.assertIn(date_string, response.content.decode())
        meal = Meals.objects.get(cdate=dt)
        self.assertTrue(meal)

    def test_summaryview(self):
        DEFAULT_DAYS_BACK = 7
        food_int = 100
        username = "user"
        curr_user = User.objects.create(username=username)
        curr_user.set_password("12345")
        curr_user.save()
        login = self.client.login(username=username, password="12345")
        self.assertTrue(login)
        end_dt = date(2022, 7, 3)
        start_dt = end_dt - timedelta(DEFAULT_DAYS_BACK)
        dt_strings = []
        url_default = f"/FoodJournal/{username}/summary/"
        url = f"/FoodJournal/{username}/summary/?start_date_input={start_dt.isoformat()}&end_date_input={end_dt.isoformat()}"
        for num in range(DEFAULT_DAYS_BACK):
            delta = timedelta(days=num)
            test_date = end_dt - delta
            meal = Meals.create(self.test_food, 1, test_date, curr_user)
            meal.save()
            dt_strings.append(test_date.strftime('%B %d, %Y').replace(" 0", " "))
        response = self.client.get(url_default)
        self.assertEquals(response.status_code, 200)
        self.assertNotIn(str(food_int), response.content.decode())
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        for date_string in dt_strings:
            self.assertIn(date_string, response.content.decode())
        self.assertIn(str(self.food_int), response.content.decode())

    def test_AddFood_valid(self):
        curr_user = User.objects.create(username="user")
        curr_user.set_password("12345")
        curr_user.save()
        login = self.client.login(username="user", password="12345")
        self.assertTrue(login)
        food = {
                "food_input":      "test",
                "calories_input":    1,
                "protein_input":     1,
                "carbs_input":       1,
                "total_fat_input":   1,
                "sat_fat_input":     1,
                "fiber_input":       1,
                "measurement_input": 1,
                "measurement_qty_input": 1
            }
        post = self.client.post(f"/FoodInfo/", food, follow=True)
        self.assertEquals(post.status_code, 200)
        food = Foods.objects.get(description="test")
        self.assertTrue(food)

    def test_AddFood_invalid(self):
        message = "FOOD FAILED TO LOAD"
        curr_user = User.objects.create(username="user")
        curr_user.set_password("12345")
        curr_user.save()
        login = self.client.login(username="user", password="12345")
        self.assertTrue(login)
        food = {
                "food_input":      "test",
                "calories_input":    1,
                "protein_input":     1,
                "carbs_input":       1,
                "total_fat_input":   1,
                "sat_fat_input":     1,
                "fiber_input":       1,
                "measurement_input": 1,
                "measurement_qty_input": 0
            }
        post = self.client.post(f"/FoodInfo/", food, follow=True)
        self.assertEquals(post.status_code, 200)
        self.assertIn(message, post.content.decode())
        self.assertRaises(Foods.DoesNotExist, Foods.objects.get, description="test")

    def test_add_food_not_logged_in(self):
        message = "FOOD FAILED TO LOAD"
        food = {
                "food_input":      "test",
                "calories_input":    1,
                "protein_input":     1,
                "carbs_input":       1,
                "total_fat_input":   1,
                "sat_fat_input":     1,
                "fiber_input":       1,
                "measurement_input": 1,
                "measurement_qty_input": 0
            }
        post = self.client.post(f"/FoodInfo/", food, follow=True)
        self.assertEquals(post.status_code, 200)
        self.assertIn(message, post.content.decode())
        self.assertRaises(Foods.DoesNotExist, Foods.objects.get, description="test")




