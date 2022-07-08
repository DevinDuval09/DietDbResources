
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.views import LoginView, LogoutView
from .views import generate_food_journal, test_page, food_info_page, add_meal, create_user, get_food_json
from .forms import InputFoodEaten

urlpatterns = [
    path("", food_info_page, name="index"),
    path("FoodInfo/", food_info_page, name="food_index"),
    path("FoodJournal/<str:username>/", generate_food_journal, name="user_index"),
    path("FoodJournal/<str:username>/add_meal", add_meal, name="add_meal"),
    re_path(r"^FoodInfo/get_food_json/(?P<food>[A-Za-z]*)/$", get_food_json, name="get_food_json",),
    path("test/", test_page, name="test_page"),
    path("register/", create_user, name="create_user")
]