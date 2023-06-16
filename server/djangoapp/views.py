from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed

from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, DealerReview
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
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

#Your mock data
mock_reviews = [
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
        },
        {
            "id": 4,
            "name": "Alice Brown",
            "dealership": dealer_id,
            "review": "The staff here is very knowledgeable and they have a great selection of cars. I am so happy with my new car!",
            "purchase": True,
            "purchase_date": "06/10/2023",
            "car_make": "Lexus",
            "car_model": "IS",
            "car_year": 2023,
            "sentiment": "positive"
        },
        {
            "id": 5,
            "name": "Charlie Davis",
            "dealership": dealer_id,
            "review": "This dealership has been nothing but trouble. They sold me a faulty car and refuse to take responsibility.",
            "purchase": True,
            "purchase_date": "05/15/2023",
            "car_make": "Ford",
            "car_model": "Mustang",
            "car_year": 2023,
            "sentiment": "negative"
        },
        {
            "id": 6,
            "name": "Eve Fisher",
            "dealership": dealer_id,
            "review": "The staff was not very helpful and they seemed uninterested in helping me find a car that fit my needs.",
            "purchase": False,
            "purchase_date": "03/20/2023",
            "car_make": "Toyota",
            "car_model": "Camry",
            "car_year": 2023,
            "sentiment": "neutral"
        }

    ]

def get_mock_reviews(dealer_id):
    return mock_reviews

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

def get_unique_car_combinations():
    reviews = get_mock_reviews(dealer_id=0)  # use a valid dealer_id here
    car_combinations = set()
    
    for review in reviews:
        car_combinations.add((review["car_make"], review["car_model"], review["car_year"]))

    # Format as "make model year"
    car_combinations = [f"{make} {model} {year}" for make, model, year in car_combinations]

    return car_combinations


@login_required
def add_review(request, dealer_id):
    """
    POST a new review or GET the form
    """
    if request.method == 'POST':
        # Prepare the payload
        json_payload = {
            'name': request.POST['name'],
            'dealership': dealer_id,
            'review': request.POST['review'],
            'purchase': request.POST.get('purchase', False),
            'purchase_date': datetime.utcnow().isoformat() if 'purchase_date' in request.POST else None,
            'car_make': request.POST['car_make'],
            'car_model': request.POST['car_model'],
            'car_year': datetime.strptime(request.POST['car_year'], "%Y") if 'car_year' in request.POST else None,
        }
        
        # You can send a post request here with the payload. 
        # I'll just leave it as a comment because it's not in the original code.
        # response = post_request(<url>, json=json_payload)
        
        # If the request was successful, redirect the user to the dealer details page.
        return redirect('djangoapp:dealer', dealer_id=dealer_id)
    elif request.method == 'GET':
        # Get unique car combinations
        car_combinations = get_unique_car_combinations()

        # find dealership from the mock data or database
        dealership = next((dealer for dealer in get_mock_dealerships() if dealer['id'] == dealer_id), None)
        if dealership:
            dealership_name = dealership['full_name']
        else:
            dealership_name = "Not Found"

        context = {
            'dealer_id': dealer_id,
            'dealer_name': dealership_name,
            'car_combinations': car_combinations,
            # add more context data if needed
        }
        return render(request, 'djangoapp/add_review.html', context)
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])



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
    