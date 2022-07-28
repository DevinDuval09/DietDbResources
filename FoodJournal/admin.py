from django.contrib import admin
from .models import Measurements, Foods, Meals

class MeasurementsInline(admin.TabularInline):
    model = Measurements

class MeasurementsAdmin(admin.ModelAdmin):
    list_display = ["id", "description"]
    ordering = ["description"]

class FoodsInline(admin.TabularInline):
    model = Foods

class FoodsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "description",
        "calories_unit",
        "protein_unit",
        "carbs_unit",
        "total_fat_unit",
        "sat_fat_unit",
        "measurement_unit"
        ]
    ordering = ["description"]

class MealsAdmin(admin.ModelAdmin):
    list_display = ["food", "qty", "cdate", "user"]
    ordering = ["user", "cdate"]


admin.site.register(Measurements, MeasurementsAdmin)
admin.site.register(Foods, FoodsAdmin)
admin.site.register(Meals, MealsAdmin)