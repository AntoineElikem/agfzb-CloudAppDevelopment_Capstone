import requests
import json
# import related models here
from .models import CarDealer, CarMake, CarModel, DealerReview
from requests.auth import HTTPBasicAuth

from .models import CarDealer
from requests.auth import HTTPBasicAuth
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


#get dealer reviews from cloud function and database

def get_dealer_reviews_from_cf(dealer_id):
    # Define the endpoint
    url = 'https://us-south.functions.appdomain.cloud/api/v1/web/fa20c694-da60-4e79-966f-cd17de8cc10f/dealership-package/review'
    
    # Define the query parameters
    params = {
        'dealerId': dealer_id
    }
    
    # Make the GET request
    response = requests.get(url, params=params)
    
    # Get the JSON data from the response
    json_data = response.json()

    # Define a list to hold the DealerReview objects
    dealer_reviews = []
    
    # Loop through the data and create a DealerReview object for each
    for review in json_data:
        dealer_review = DealerReview(
            dealership=review['dealership'],
            name=review['name'],
            purchase=review['purchase'],
            review=review['review'],
            purchase_date=review['purchase_date'],
            car_make=review['car_make'],
            car_model=review['car_model'],
            car_year=review['car_year'],
            sentiment='',  # We will fill this in later
            id=review['id']
        )
        
        # Add the DealerReview object to the list
        dealer_reviews.append(dealer_review)
        
    # Return the list of DealerReview objects
    return dealer_reviews



def post_request(url, json_payload, **kwargs):
    """
    POST method to send data to a specified URL
    """
    response = requests.post(url, params=kwargs, json=json_payload)

    # Check the status of the response
    status = response.status_code
    if status != 200 and status != 201:
        raise Exception(f"Post request failed with status code {status}")
    else:
        return response.json()


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



