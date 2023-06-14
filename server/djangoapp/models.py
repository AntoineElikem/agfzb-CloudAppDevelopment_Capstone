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

class DealerReview():
    # Assuming a review has an id, dealership, name, purchase, review, and purchase_date
    def __init__(self, id, dealership, name, purchase, review, purchase_date):
        self.id = id
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
