
from django.contrib import admin
from django.urls import path, include, re_path, register_converter
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from .views import test_page, MealsView, create_user, get_food_json, FoodInfo, IsoStringDateConverter
from .forms import InputFoodEaten

register_converter(IsoStringDateConverter, "datestring")
urlpatterns = [
    path("", RedirectView.as_view(url="FoodInfo/", permanent=False), name="index"),
    path("FoodInfo/", FoodInfo.as_view(), name="food_index"),
    path("FoodJournal/<str:username>/", MealsView.as_view(), name="user_home"),
    path("FoodJournal/<str:username>/meals", MealsView.as_view(), name="user_meals"),
    re_path(r"^FoodInfo/get_food_json/(?P<food>[A-Za-z]*|[A-Za-z]* [A-Za-z]*|[0-9]?[0-9]% [A-Za-z]* [A-Za-z]*)/$", get_food_json, name="get_food_json",),
    path("FoodJournal/<str:username>/<datestring:startdate>/<datestring:enddate>/", MealsView.as_view(), name="meals_daterange"),
    path("test/", test_page, name="test_page"),
    path("register/", create_user, name="create_user")
]