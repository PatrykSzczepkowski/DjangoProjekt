from django.db import models

class Car(models.Model):

    FUEL_CHOICES = (
        ('diesel', 'Diesel'),
        ('petrol', 'Benzyna'),
        ('hybrid', 'Gaz+Benzyna'),
    )

    make = models.CharField(max_length=100)  # Marka
    model = models.CharField(max_length=100)  # Model
    year_of_manufacture = models.IntegerField()  # Rok produkcji
    mileage = models.IntegerField()  # Przebieg
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES) #typ paliwa
    description = models.TextField()  # Opis
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Cena
    date_added = models.DateTimeField(auto_now_add=True)  # Data dodania oferty

    def __str__(self):
        return f"{self.make} {self.model} {self.year_of_manufacture}"

class Owner(models.Model):
    first_name = models.CharField(max_length=100)  # Imię
    last_name = models.CharField(max_length=100)  # Nazwisko
    phone_number = models.CharField(max_length=15)  # Numer telefonu
    cars = models.ForeignKey(Car, on_delete=models.CASCADE)  # Samochody

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class VehicleHistory(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)  # Samochód
    repair_information = models.TextField()  # Informacje o naprawach
    previous_owners = models.IntegerField()  # Ilość poprzednich właścicieli

    def __str__(self):
        return f"Historia {self.car} Ilość właścicieli {self.previous_owners}"

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)  # Samochód
    image = models.ImageField(upload_to='car_images/')  # Zdjęcie
    description = models.CharField(max_length=255)  # Opis zdjęcia
    date_added = models.DateTimeField(auto_now_add=True)  # Data dodania

    def __str__(self):
        return f"Zdjecie {self.car} - {self.description[:50]}" #ogranicza ilosc do 50 znakow w wyswietlaniu