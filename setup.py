import django
django.setup()
from FoodJournal.models import csv_to_model, file_path
if __name__ == "__main__":
    csv_to_model(file_path)