from django.http.response import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.views.generic import ListView, CreateView
from .DbUtil import *
from .models import Meals, Foods, Measurements, get_food_model
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
import os
from .forms import InputFoodEaten, NewUserForm
import logging
from datetime import date, timedelta, datetime

logger = logging.getLogger(__name__)

DATE_FORMAT = "%Y-%m-%d"
class IsoStringDateConverter:
    regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]"
    def to_python(self, date_string):
        return datetime.strptime(date_string, DATE_FORMAT)
    def to_url(self, date_val):
        return date_val.strftime(DATE_FORMAT)

def create_user(request, *args, **kwargs):
    form = NewUserForm(request.POST)
    redirect_page = request.POST.get("user_index", "/")
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
        login(request, user)
        return HttpResponseRedirect(redirect_to=redirect_page)
    else:
        return render(request, "new_user.html", {"form": form})

class MealsView(ListView):
    template_name = "FoodJournal/meals_list.html"
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        logger.info(kwargs)
        if not self.kwargs.get("startdate") or not self.kwargs.get("enddate"):
            enddate = date.today()
            delta = timedelta(days=7)
            startdate = enddate - delta
            self.kwargs["startdate"] = startdate
            self.kwargs["enddate"] = enddate
            self.kwargs["startdate_string"] = startdate.strftime(DATE_FORMAT)
            self.kwargs["enddate_string"] = startdate.strftime(DATE_FORMAT)
        else:
            self.kwargs["enddate_string"] = datetime.strftime(self.kwargs["enddate"], DATE_FORMAT)
            self.kwargs["startdate_string"] = datetime.strftime(self.kwargs["startdate"], DATE_FORMAT)
        #logger.info(request.GET)

    def get_queryset(self):
        return Meals.objects.filter(user__username=self.kwargs["username"], cdate__range=(self.kwargs["startdate"], self.kwargs["enddate"])).order_by("cdate")
    def post(self, request, *args, **kwargs):
        logger.info(request.POST)
        form = InputFoodEaten(
            {
                'cdate':    datetime.strptime(request.POST.get("date_input"), '%Y-%m-%d').date(),
                'qty':      float(request.POST.get("qty_input")),
                'food':     int(request.POST.get("food_id")),
                'user':     int(request.user.id)
            }
        )
        if form.is_valid():
            form.save()
        return redirect(reverse("user_meals", args=[self.kwargs["username"]]))


def test_page(request, *args, **kwargs):
    body = "Test Page\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join([f"\t{arg}" for arg in args])
    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join([f"\t{tup}" for tup in kwargs.items()])
    return HttpResponse(body, content_type="text/plain")

class FoodInfo(ListView):
    template_name = "FoodJournal/FoodInfo.html"
    model = Foods
    queryset = Foods.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["m_table"] = Measurements.objects.all()
        return context
    def post(self, request, *args, **kwargs):
        logger.info(request.POST)
        form = AddFood({
            "description":      request.POST.get("food_input"),
            "calories_unit":    request.POST.get("calories_input"),
            "protein_unit":     request.POST.get("protein_input"),
            "carbs_unit":       request.POST.get("carbs_input"),
            "total_fat_unit":   request.POST.get("total_fat_input"),
            "sat_fat_unit":     request.POST.get("sat_fat_input"),
            "fiber_unit":       request.POST.get("fiber_input"),
            "measurement_unit": request.POST.get("measurement_input"),
        })

def get_food_json(request, food, *args, **kwargs):
    logger.info(f"Getting json for {food}...")
    if request.method == "GET":
        food_name = clean_input(food)
        food_data = get_food_model(food_name)
        return JsonResponse(food_data)



