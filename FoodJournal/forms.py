from django.db.models.base import Model
from django.forms import Form, ModelForm, TextInput, Textarea, DateInput, NumberInput, ChoiceField, Select
from django.contrib.auth.forms import UserCreationForm
import logging
from datetime import datetime
from .models import Meals, Foods, Measurements

logger = logging.getLogger(__name__)
#MEASUREMENT_CHOICES = Measurements.objects.all()
#FOOD_CHOICES = Foods.objects.all()
class NewUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
        labels = {"email": ("Email address:")}


class InputFoodEaten(ModelForm):
    class Meta:
        model = Meals
        fields = ["cdate", "food", "qty", "user"]
        widgets = {
            "cdate"      : DateInput(attrs={"class":"datepicker"}),
            "food"      : NumberInput(attrs={"required":True}),#ChoiceField(choices = FOOD_CHOICES, required=True),
            "qty"       : NumberInput(attrs={"required": True}),
            "user"      : NumberInput(attrs={"required": True})
        }
        labels = {"cdate": "Date:", "food": "Food:", "qty": "Quantity:"}

class AddFood(Form):
    class Meta:
        model = Foods
        fields =    ["description",
                    "calories_unit",
                    "protein_unit",
                    "carbs_unit",
                    "total_fat_unit",
                    "sat_fat_unit",
                    "fiber_unit",
                    "measurement_unit"]
        widgets = {
            "description":      TextInput(attrs={"required": True}),
            "calories_unit":    NumberInput(attrs={"required": True}),
            "protein_unit":    NumberInput(attrs={"required": True}),
            "carbs_unit":    NumberInput(attrs={"required": True}),
            "total_fat_unit":    NumberInput(attrs={"required": True}),
            "sat_fat_unit":    NumberInput(attrs={"required": True}),
            "fiber_unit":    NumberInput(attrs={"required": True}),
            "measurement_unit":    TextInput(attrs={"required": True}),
        }
        labels = {
            "description": "Description",
            "calories_unit": "Calories",
            "protein_unit": "Protein",
            "carbs_unit": "Carbs",
            "total_fat_unit": "Total Fat",
            "sat_fat_unit": "Saturated Fat",
            "fiber_unit": "Fiber",
            "measurement_unit": "Measurements"
        }

