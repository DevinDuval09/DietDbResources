from django.db.models.base import Model
from django.forms import Form, ModelForm, TextInput, Textarea, DateInput, NumberInput, ChoiceField, Select
from django.contrib.auth.forms import UserCreationForm
from .DbUtil import FOOD_CHOICES, session, food_eaten
from sqlalchemy import select

class NewUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
        labels = {"email": ("Email address:")}


class InputFoodEaten(Form):
    class Meta:
        fields = ["date", "food", "qty", "calories"]
        widgets = {
            "date"      : DateInput(attrs={"class":"datepicker"}),
            "food"      : ChoiceField(choices = FOOD_CHOICES, required=True),
            "qty"       : NumberInput(attrs={"required": True}),
            "calories"  : NumberInput({"readonly":True})
        }
        labels = {"date": "Date:", "food": "Food:", "qty": "Quantity:", "calories": "Total Calories:"}
    def save(self):
        if self.is_valid():
            data = {}
            data["date"] = request.POST["date"]
            data["food"] = request.POST["food"]
            data["qty"] = request.POST["qty"]
            data["user"] = request.user.id
            with session.begin() as s:
                stmt = insert(food_eaten).values(
                                                date=data["date"],
                                                food=data["food"],
                                                qty=data["qty"],
                                                user=data["user"]
                                                )
                s.execute(stmt)
                s.commit()
                return
        print("InputFoodEaten form is not valid.")
        return



