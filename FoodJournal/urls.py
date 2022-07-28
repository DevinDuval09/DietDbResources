
from django.contrib import admin
from django.urls import path, include, re_path, register_converter
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from .views import test_page, MealsView, create_user, get_food_json, FoodInfo, IsoStringDateConverter, SummaryView, MealDetail
from .forms import InputFoodEaten

register_converter(IsoStringDateConverter, "datestring")
urlpatterns = [
    path("", RedirectView.as_view(url="FoodInfo/", permanent=False), name="index"),
    path("FoodInfo/", FoodInfo.as_view(), name="food_index"),
    path("FoodJournal/<str:username>/", MealsView.as_view(), name="user_home"),
    path("FoodJournal/<str:username>/meals/", MealsView.as_view(), name="user_meals"),
    path("FoodJournal/<str:username>/meals/<int:pk>/", MealDetail.as_view(), name="edit_meal"),
    path("FoodJournal/<str:username>/summary/", SummaryView.as_view(), name="user_summary"),
    path("FoodInfo/get_food_json/<str:food>/", get_food_json, name="get_food_json"),
    path("FoodJournal/<str:username>/<datestring:startdate>/<datestring:enddate>/", MealsView.as_view(), name="meals_daterange"),
    path("test/", test_page, name="test_page"),
    path("register/", create_user, name="create_user")
]