from django.contrib import admin

from .models import Car, Owner, VehicleHistory, CarImage

admin.site.register(Car)
admin.site.register(Owner)
admin.site.register(VehicleHistory)
admin.site.register(CarImage)
