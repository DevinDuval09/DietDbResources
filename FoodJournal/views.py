from django.http.response import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from .DbUtil import *
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
import os
from .forms import InputFoodEaten, NewUserForm
import logging

logger = logging.getLogger(__name__)

def create_user(request, *args, **kwargs):
    form = NewUserForm(request.POST)
    redirect_page = request.POST.get("food_index", "/")
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
        login(request, user)
        return HttpResponseRedirect(redirect_to=redirect_page)
    else:
        return render(request, "new_user.html", {"form": form})

def add_meal(request, *args, **kwargs):
    if request.user.id is None:
        return redirect("/login/")
    form = InputFoodEaten(initial={"user": request.user.id})
    user_name = request.user_name
    if request.method == "POST":
        if form.is_valid():
            form.save()
    redirect(f"/FoodJournal/{user_name}/")



def edit_food_eaten(request, *args, **kwargs):
    pass

def view_food_eaten(request, *args, **kwargs):
    pass

def test_page(request, *args, **kwargs):
    body = "Test Page\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join([f"\t{arg}" for arg in args])
    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join([f"\t{tup}" for tup in kwargs.items()])
    return HttpResponse(body, content_type="text/plain")

def generate_food_journal(request, username, template_name="FoodJournal/FoodJournal.html", *args, **kwargs):
    if request.user.id is None:
        return redirect("/login/")
    if request.method == "GET":
        template_name = "FoodJournal/FoodJournal.html"
        kwargs["user_id"] = get_id(users, users.c.username, username)
        with session.begin() as s:
            query = select(food_eaten.c.date,
                            food_info.c.description,
                            food_eaten.c.qty,
                            food_info.c.calories_unit)\
                        .filter(food_eaten.c.food == food_info.c.id, food_eaten.c.user == kwargs["user_id"])
            results = s.execute(query).all()
            data = []
            for row in results:
                data.append([row[0], row[1], row[2], row[2] * row[3]])
        return render(request, template_name, {"rows": data})
    elif request.method == "POST":
        form = InputFoodEaten(request.POST, initial={"user": request.user.id})
        logger.info("\n\nInvoking form\n\n")
        if form.is_valid():
            form.save(request)
        return redirect(reverse("user_index", args=[username]))

def food_journal_form(request, *args, **kwargs):
    form = InputFoodEaten(request.POST)

def get_food_info_page(request, template_name="FoodJournal/FoodInfo.html", *args, **kwargs):
    with session.begin() as s:
        query = select(food_info.c.description, food_info.c.calories_unit, measurements.c.description).filter(food_info.c.measurement_unit == measurements.c.id)
        results = s.execute(query).all()
        data = []
        for row in results:
            data.append([row[0].title(), row[1], row[2]])
        measurement_query = select(measurements)
        measure_results = s.execute(measurement_query).all()
        measure_rows = []
        for mrow in measure_results:
            measure_rows.append([mrow[0], mrow[1]])
    context = {"rows": data, "m_table": measure_rows}
    if "errors" in kwargs.keys():
        context["errors"] = kwargs["errors"]
    return render(request, template_name, context)

def post_food_info_page(request, template_name="FoodJournal/FoodInfo.html", *args, **kwargs):
    #these should match the input field names on FoodInfo.html
    form_fields = ["food_input",
                    "measurement_input",
                    "calorie_input",
                    "protein_input",
                    "carbs_input",
                    "total_fat_input",
                    "sat_fat_input",
                    "fiber_input"]
    errors = []
    validated_data = {}
    for field in form_fields:
        try:
            if request.POST[field].strip() == '' or request.POST[field] is None:
                raise KeyError
            validated_data[field] = request.POST[field]
        except KeyError:
            errors.append(f"{field} must have a value.")
            continue
    if len(errors) > 0:
        return get_food_info_page(request, template_name, *args, errors=errors)
    with session.begin() as s:
        stmt = insert(food_info).values(description=validated_data["food_input"],
                                        calories_unit=validated_data["calorie_input"],
                                        protein_unit=validated_data["protein_input"],
                                        carbs_unit=validated_data["carbs_input"],
                                        total_fat_unit=validated_data["total_fat_input"],
                                        sat_fat_unit=validated_data["sat_fat_input"],
                                        fiber_unit=validated_data["fiber_input"],
                                        measurement_unit=validated_data["measurement_input"])
        try:
            s.execute(stmt)
            s.commit()
            request.method = "GET"
            message = f"{validated_data['food_input']} has been added."
            return food_info_page(request, template_name, message=message)
        except IntegrityError as err:
            errors.append("Database error: " + repr(err))
            return get_food_info_page(request, template_name, *args, errors=errors)

def food_info_page(request, template_name="FoodJournal/FoodInfo.html", *args, **kwargs):
    if request.method == "GET":
        return get_food_info_page(request, template_name, *args, **kwargs)
    if request.method == "POST":
        return post_food_info_page(request, template_name, *args, **kwargs)

def get_food_json(request, food, *args, **kwargs):
    if request.method == "GET":
        food_name = clean_input(food)
        food_data = get_food_dict(food_name)
        return JsonResponse(food_data)



