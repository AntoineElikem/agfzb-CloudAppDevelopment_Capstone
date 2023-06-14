from django.contrib import admin
from .models import CarMake, CarModel

# Define the admin class
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 0  # how many rows to show

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]  # This makes CarModelInline part of CarMakeAdmin
    list_display = ('name', 'description')  # which fields to display
    search_fields = ['name']  # which fields to search

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'dealer_id', 'car_type', 'year')
    list_filter = ('car_make', 'car_type')
    search_fields = ['name']

# Register your models here.
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
