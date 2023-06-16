from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, DealerReview
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
#ibm nlu imports
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Initialize Watson NLU
nlu = NaturalLanguageUnderstandingV1(
    version='2021-03-25',
    authenticator=IAMAuthenticator('TspZ0ytVRoG-WdrpU_6kmsp9AnM5zieCpN1znEbsHjXZ')
)

nlu.set_service_url('https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/5f85e6b0-949f-4daa-a520-a4d4a443c362')

# Create your views here.
def index(request):
    return render(request, 'djangoapp/index.html')

def about(request):
    return render(request, 'djangoapp/about.html')

def contact(request):
    return render(request, 'djangoapp/contact.html')

def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/djangoapp')
        else:
            return render(request, 'djangoapp/login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'djangoapp/login.html')

def logout_request(request):
    logout(request)
    return render(request, "djangoapp/logout.html", {})

def registration_request(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        firstname = request.POST["first_name"]
        lastname = request.POST["last_name"]
        user = User.objects.create_user(username=username, password=password, first_name=firstname, last_name=lastname)
        user.save()
        login(request, user)
        return HttpResponseRedirect('/djangoapp')
    else:
        return render(request, 'djangoapp/registration.html')

def get_mock_dealerships():
    return [
        {"id": 1, "full_name": "Deal Mart Autos", "short_name": "Deal Mart", "city": "San Francisco", "st": "CA", "state": "California", "zip": "94104", "address": "123 Market St", "lat": 37.7941, "long": -122.4016},
        {"id": 2, "full_name": "Auto Pro Center", "short_name": "Auto Pro", "city": "Los Angeles", "st": "CA", "state": "California", "zip": "90013", "address": "456 Spring St", "lat": 34.0473, "long": -118.2462},
        {"id": 3, "full_name": "Car Hub Station", "short_name": "Car Hub", "city": "Seattle", "st": "WA", "state": "Washington", "zip": "98101", "address": "789 Pine St", "lat": 47.6101, "long": -122.3352},
        {"id": 4, "full_name": "Wheel Deal House", "short_name": "Wheel Deal", "city": "Miami", "st": "FL", "state": "Florida", "zip": "33130", "address": "101 Brickell Ave", "lat": 25.7623, "long": -80.1946},
        {"id": 5, "full_name": "Motor House Corp", "short_name": "Motor House", "city": "Chicago", "st": "IL", "state": "Illinois", "zip": "60603", "address": "202 Adams St", "lat": 41.8793, "long": -87.6269},
        {"id": 6, "full_name": "Drive Lane Autos", "short_name": "Drive Lane", "city": "Houston", "st": "TX", "state": "Texas", "zip": "77002", "address": "303 Austin St", "lat": 29.7601, "long": -95.3622},
        {"id": 7, "full_name": "Highway Auto Plaza", "short_name": "Highway Auto", "city": "Phoenix", "st": "AZ", "state": "Arizona", "zip": "85003", "address": "404 Washington St", "lat": 33.4491, "long": -112.0766},
        {"id": 8, "full_name": "Fast Lane Motors", "short_name": "Fast Lane", "city": "San Antonio", "st": "TX", "state": "Texas", "zip": "78205", "address": "505 Commerce St", "lat": 29.4246, "long": -98.4896},
        {"id": 9, "full_name": "Car Spot Dealership", "short_name": "Car Spot", "city": "San Diego", "st": "CA", "state": "California", "zip": "92101", "address": "606 Broadway", "lat": 32.7157, "long": -117.1611},
    ]

def get_dealerships(request):
    if request.method == "GET":
        dealerships = get_mock_dealerships()
        context = {
            'dealerships':dealerships
        }
        return render(request, 'djangoapp/index.html', context)

def get_mock_reviews(dealer_id):
    return [
        {
            "id": 1,
            "name": "John Doe",
            "dealership": dealer_id,
            "review": "This dealership was great! Everyone was very friendly and helpful.",
            "purchase": True,
            "purchase_date": "05/02/2023",
            "car_make": "Audi",
            "car_model": "A6",
            "car_year": 2023,
            "sentiment": "positive"
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "dealership": dealer_id,
            "review": "I had a great experience buying a car here. The staff was friendly and helpful.",
            "purchase": True,
            "purchase_date": "12/01/2023",
            "car_make": "BMW",
            "car_model": "M3",
            "car_year": 2023,
            "sentiment": "positive"
        },
        {
            "id": 3,
            "name": "Bob Johnson",
            "dealership": dealer_id,
            "review": "I had a terrible experience at this dealership. The staff was rude and unhelpful.",
            "purchase": False,
            "purchase_date": "03/15/2023",
            "car_make": "Mercedes",
            "car_model": "C Class",
            "car_year": 2023,
            "sentiment": "negative"
        }
    ]

def get_dealer_details(request, dealer_id):
    # Get dealer reviews from the mock data
    reviews = get_mock_reviews(dealer_id)

    # Analyze sentiment for each review using Watson NLU
    for review in reviews:
        response = nlu.analyze(
            text=review['review'],
            features=Features(sentiment=SentimentOptions())
        ).get_result()

        review['sentiment'] = response['sentiment']['document']['label']

    # Render the template
    return render(request, 'djangoapp/dealer_details.html', {'reviews': reviews})

# def get_dealer_details(request, dealer_id):
#     # Get dealer reviews from the database
#     reviews = DealerReview.objects.filter(dealership=dealer_id)

#     # Analyze sentiment for each review using Watson NLU
#     for review in reviews:
#         response = nlu.analyze(
#             text=review.review,
#             features=Features(sentiment=SentimentOptions())
#         ).get_result()

#         review.sentiment = response['sentiment']['document']['label']

#     # Render the template
#     return render(request, 'dealer_details.html', {'reviews': reviews})
    