from django.http.response import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.views.generic import ListView, CreateView
from django.db.models import Sum, FloatField, F
from .DbUtil import *
from .models import Meals, Foods, Measurements, get_food_model
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
import os
from .forms import InputFoodEaten, NewUserForm, AddFood
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

class SummaryView(ListView):
    template_name = "FoodJournal/FoodJournal.html"


    def dispatch(self, request, *args, **kwargs):
        if request.user.id is None:
            return redirect("/login/")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        #need to find a way to pass args to search
        logger.info(self.request.GET)
        default_end = datetime.strftime(date.today(), DATE_FORMAT)
        default_start = datetime.strftime(date.today() - timedelta(days=7), DATE_FORMAT)
        self.enddate = datetime.strptime(self.request.GET.get("end_date_input", default_end), DATE_FORMAT)
        self.startdate = datetime.strptime(self.request.GET.get("start_date_input", default_start), DATE_FORMAT)
        q = Meals.objects.filter(user__username=self.kwargs["username"],
                                    cdate__range=(self.startdate,
                                    self.enddate))\
                        .select_related("food")\
                        .values("cdate")\
                        .annotate(total_calories =  Sum(F('food__calories_unit') * F('qty')))\
                        .annotate(total_protein =   Sum(F('food__protein_unit') * F('qty')))\
                        .annotate(total_carbs =     Sum(F('food__carbs_unit') * F('qty')))\
                        .annotate(total_total_fat = Sum(F('food__total_fat_unit') * F('qty')))\
                        .annotate(total_sat_fat =   Sum(F('food__sat_fat_unit') * F('qty')))\
                        .annotate(total_fiber =     Sum(F('food__fiber_unit') * F('qty'))\
                                )\
                        .order_by()
        return q
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["startdate_string"] = datetime.strftime(self.startdate, DATE_FORMAT)
        ctx["enddate_string"] = datetime.strftime(self.enddate, DATE_FORMAT)
        return ctx
class MealsView(ListView):
    template_name = "FoodJournal/meals_list.html"
    def setup(self, request, *args, **kwargs):
        if (request.user.id is None):
            redirect("/login/")
        super().setup(request, *args, **kwargs)
        logger.info(kwargs)
        if not self.kwargs.get("startdate") or not self.kwargs.get("enddate"):
            enddate = date.today()
            delta = timedelta(days=7)
            startdate = enddate - delta
            self.kwargs["startdate"] = startdate
            self.kwargs["enddate"] = enddate
            self.kwargs["startdate_string"] = startdate.strftime(DATE_FORMAT)
            self.kwargs["enddate_string"] = enddate.strftime(DATE_FORMAT)
        else:
            self.kwargs["enddate_string"] = datetime.strftime(self.kwargs["enddate"], DATE_FORMAT)
            self.kwargs["startdate_string"] = datetime.strftime(self.kwargs["startdate"], DATE_FORMAT)
        #logger.info(request.GET)

    def dispatch(self, request, *args, **kwargs):
        if request.user.id is None:
            return redirect("/login/")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Meals.objects.filter(user__username=self.kwargs["username"],
                                    cdate__range=(self.kwargs["startdate"],
                                    self.kwargs["enddate"])).order_by("cdate")

    def post(self, request, *args, **kwargs):
        if (request.user.id is None):
            redirect("/login/")
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

    def dispatch(self, request, *args, **kwargs):
        if request.user.id is None:
            return redirect("/login/")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logger.info(f"{request.user.id}")
        logger.info(request.POST)
        if (request.user.id is None):
            redirect("/login/")
        errors = None
        divisor = float(request.POST.get("measurement_qty_input", None))
        if divisor and divisor > 0:
            calories_unit = float(request.POST.get("calorie_input")) / divisor
            protein_unit =  float(request.POST.get("protein_input")) / divisor
            carbs_unit =    float(request.POST.get("carbs_input")) / divisor
            total_fat_unit =float(request.POST.get("total_fat_input")) / divisor
            sat_fat_unit =  float(request.POST.get("sat_fat_input")) / divisor
            fiber_unit =    float(request.POST.get("fiber_input")) / divisor
            form = AddFood({
                "description":      request.POST.get("food_input"),
                "calories_unit":    calories_unit,
                "protein_unit":     protein_unit,
                "carbs_unit":       carbs_unit,
                "total_fat_unit":   total_fat_unit,
                "sat_fat_unit":     sat_fat_unit,
                "fiber_unit":       fiber_unit,
                "measurement_unit": request.POST.get("measurement_input"),
            })
            if form.is_valid():
                form.save()
        else:
            errors = ["Measurement quantity must be above 0."]
        if errors:
            self.object_list = self.queryset
            ctx = self.get_context_data(**kwargs)
            ctx["errors"] = errors
            return render(request, "FoodJournal/FoodInfo.html", context=ctx)
        return redirect(reverse("food_index"))

def get_food_json(request, food, *args, **kwargs):
    logger.info(f"Getting json for {food}...")
    if request.method == "GET":
        food_name = clean_input(food)
        food_data = get_food_model(food_name)
        return JsonResponse(food_data)



