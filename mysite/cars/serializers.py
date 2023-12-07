from rest_framework import serializers
from .models import Car, Owner, VehicleHistory, CarImage
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'year_of_manufacture', 'mileage', 'fuel_type', 'description', 'price', 'date_added']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        instance.make = validated_data.get('make', instance.make)
        instance.model = validated_data.get('model', instance.model)
        instance.year_of_manufacture = validated_data.get('year_of_manufacture', instance.year_of_manufacture)
        instance.mileage = validated_data.get('mileage', instance.mileage)
        instance.fuel_type = validated_data.get('fuel_type', instance.fuel_type)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.date_added = validated_data.get('date_added', instance.date_added)
        instance.save()
        return instance

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'cars']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.car = validated_data.get('car', instance.car)

class VehicleHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleHistory
        fields = ['id', 'car', 'repair_information', 'previous_owners']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        instance.car = validated_data.get('car', instance.car)
        instance.repair_information = validated_data.get('repair_information', instance.repair_information)
        instance.previous_owners = validated_data.get('previous_owners', instance.previous_owners)
        instance.save()
        return instance

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'car', 'image', 'description', 'date_added']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        instance.car = validated_data.get('car', instance.car)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.date_added = validated_data.get('date_added', instance.date_added)
        instance.save()
        return instance
