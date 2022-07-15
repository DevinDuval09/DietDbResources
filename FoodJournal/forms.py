from django.db.models.base import Model
from django.forms import Form, ModelForm, TextInput, Textarea, DateInput, NumberInput, ChoiceField, Select
from django.contrib.auth.forms import UserCreationForm
from .DbUtil import FOOD_CHOICES, food_eaten, DATABASE_NAME, create_test_engine
from sqlalchemy.orm.session import sessionmaker, Session
from sqlalchemy import select, insert
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)
engine = create_test_engine()
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
    def save(self, request):
        if self.is_valid():
            session = sessionmaker(engine)
            logger.info("Post request and data transformation:")
            logger.info(request.POST)
            data = {}
            data["date"] = datetime.strptime(request.POST["date_input"], '%Y-%m-%d')
            data["food"] = request.POST["food_id"]
            data["qty"] = request.POST["qty_input"]
            data["user"] = request.user.id
            logger.info(data)
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
        logger.error("InputFoodEaten form is not valid.")

