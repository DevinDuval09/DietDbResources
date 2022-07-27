import django
django.setup()
from FoodJournal.models import csv_to_model
if __name__ == "__main__":
    file_path = "./FoodJournal/csv/RawFoodData.csv"
    csv_to_model(file_path)