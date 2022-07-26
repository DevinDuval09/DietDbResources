from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.contrib.auth.models import User
import csv
from sqlite3 import IntegrityError

file_path = './csv/RawFoodData.csv'
food_description = 0
calories = 1
protein = 2
carbs = 3
total_fat = 4
sat_fat = 5
fiber = 6
MEASUREMENT = 7

decimal_options = {"null": False, "decimal_places": 3, "max_digits": 6}
def csv_to_model(path:str)->None:
    #get pks for all the measurements in the csv file
    measurement_dict = {}
    with open(path, "r") as file:
        for row in csv.reader(file):
            measure_string = row[MEASUREMENT].lower().strip()
            if measure_string == 'measurement':
                continue
            id = Measurements.objects.filter(description=measure_string)
            if id:
                measurement_dict[measure_string] = id
            else:
                new_measure = Measurements.create(description=measure_string)
                new_measure.save()
                id = Measurements.objects.get(description=measure_string)
                measurement_dict[measure_string] = id
    #load all data from csv file
    with open(path, "r") as file:
        for row in csv.reader(file):
            data_dict = {}
            try:
                # data dict keys have to be the same as the food_info table column names
                data_dict['description'] = row[food_description].lower().strip()
                data_dict['calories_unit'] = float(row[calories])
                data_dict['protein_unit'] = float(row[protein])
                data_dict['carbs_unit'] = float(row[carbs])
                data_dict['total_fat_unit'] = float(row[total_fat])
                data_dict['sat_fat_unit'] = float(row[sat_fat])
                data_dict['fiber_unit'] = float(row[fiber])
                data_dict['measurement_unit'] = measurement_dict[row[MEASUREMENT].lower().strip()]
                food = Foods(**data_dict)
                food.save()
            except (ValueError, IntegrityError) as error:
                continue

class Measurements(models.Model):
    class Meta:
        db_table = "Measurements"
    id = models.IntegerField(primary_key=True, auto_created=True)
    description = models.CharField(unique=True, null=False, max_length=100)
    @classmethod
    def create(clss, description:str):
        return clss(description=description)


class Foods(models.Model):
    class Meta:
        db_table = "Foods"
    id = models.IntegerField(primary_key=True, auto_created=True)
    description = models.CharField(unique=True, null=False, max_length=100)
    calories_unit = models.DecimalField(**decimal_options)
    protein_unit = models.DecimalField(**decimal_options)
    carbs_unit = models.DecimalField(**decimal_options)
    total_fat_unit = models.DecimalField(**decimal_options)
    sat_fat_unit = models.DecimalField(**decimal_options)
    fiber_unit = models.DecimalField(**decimal_options)
    measurement_unit = models.ForeignKey("Measurements", null=False, on_delete=CASCADE, db_column="measurement_unit")
    @classmethod
    def create(clss, description:str, calories:float, protein:float, carbs:float, tot_fat:float, sat_fat:float, fiber: float, measurement:int):
        return clss(description=description,
                    calories_unit=calories,
                    protein_unit=protein,
                    carbs_unit=carbs,
                    total_fat_unit=tot_fat,
                    sat_fat_unit=sat_fat,
                    fiber_unit=fiber,
                    measurement_unit=measurement)

class Meals(models.Model):
    class Meta:
        db_table = "Meals"
    id = models.IntegerField(primary_key=True, auto_created=True)
    food = models.ForeignKey("Foods", null=False, on_delete=CASCADE, db_column="food")
    qty = models.DecimalField(**decimal_options)
    cdate = models.DateField(null=False, db_column="date")
    user = models.ForeignKey(User, on_delete=CASCADE, db_column="user")
    @classmethod
    def create(clss, food:Foods, qty:float, date, user:User):
        return clss(food=food, qty=qty, cdate=date, user=user)

def get_food_model(food:str)->dict:
    try:
        instance = Foods.objects.get(description=food)
        food_dict = {
            "id":               instance.id,
            "description":      instance.description,
            "calories_unit":    float(instance.calories_unit),
            "protein_unit":     float(instance.protein_unit),
            "carbs_unit":       float(instance.carbs_unit),
            "total_fat_unit":   float(instance.total_fat_unit),
            "sat_fat_unit":     float(instance.sat_fat_unit),
            "fiber_unit":       float(instance.fiber_unit),
            "measurement_id":   instance.measurement_unit.id,
            "measurement_desc": instance.measurement_unit.description
            }
        return food_dict
    except Foods.DoesNotExist:
        error_dict = {"error": f"{food} is not in database."}
        return error_dict