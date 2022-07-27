from django.core.management.base import BaseCommand
from FoodJournal.models import Measurements, Foods
import csv

food_description = 0
calories = 1
protein = 2
carbs = 3
total_fat = 4
sat_fat = 5
fiber = 6
MEASUREMENT = 7

decimal_options = {"null": False, "decimal_places": 3, "max_digits": 6}

class Command(BaseCommand):
    help = "Loads the data from a CSV table with food information into Foods."
    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        #get pks for all the measurements in the csv file
        measurement_dict = {}
        with open(options["file_path"], "r") as file:
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
        total_count = 0
        success_count = 0
        with open(options["file_path"], "r") as file:
            data = []
            for row in csv.reader(file):
                total_count += 1
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
                    data.append(food)
                    if len(data) > 50:
                        Foods.objects.bulk_create(data)
                        success_count += 50
                        data = []
                except Exception:
                    continue
            if data:
                success_count += len(data)
                Foods.objects.bulk_create(data)
        self.stdout.write(f"Added {total_count} of {success_count} foods.")