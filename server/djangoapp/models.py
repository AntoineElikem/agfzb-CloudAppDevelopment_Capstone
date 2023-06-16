from django.db import models

class CarMake(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class CarModel(models.Model):
    SEDAN = 'SD'
    SUV = 'SV'
    WAGON = 'WG'
    CAR_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
    ]
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=255)
    car_type = models.CharField(
        max_length=2,
        choices=CAR_CHOICES,
        default=SEDAN,
    )
    year = models.DateField()

    def __str__(self):
        return self.name

class CarDealer():
    # Assuming a dealer has an id, name, and city
    def __init__(self, id, name, city):
        self.id = id
        self.name = name
        self.city = city

class DealerReview(models.Model):
    dealership = models.IntegerField()
    name = models.CharField(max_length=255)
    purchase = models.BooleanField()
    review = models.TextField()
    purchase_date = models.DateField()
    car_make = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)
    car_year = models.IntegerField()
    sentiment = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.name}'s review of dealer {self.dealership}"

class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name
