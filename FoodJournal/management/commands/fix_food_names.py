
from django.core.management.base import BaseCommand
from FoodJournal.models import Measurements, Foods

class Command(BaseCommand):
    help = "Changes uppercase letters in Food.description to lowercase."
    def add_arguments(self, parser):
        parser.add_argument("food_names", type=str, nargs="?", default=None)

    def handle(self, *args, **options):
        foods = options.get("food_names", None)
        if foods:
            for food in foods:
                try:
                    obj = Foods.objects.get(description=food)
                    obj.description = obj.description.lower()
                    obj.save()
                except Foods.DoesNotExist:
                    self.stdout.write(f"Couldn't locate {food} in database.")
        else:
            foods = Foods.objects.all()
            for food in foods:
                food.description = food.description.lower()
                food.save()
