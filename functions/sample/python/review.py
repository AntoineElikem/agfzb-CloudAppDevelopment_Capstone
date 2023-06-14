from cloudant.client import Cloudant
from cloudant.error import CloudantException
from datetime import datetime
import requests

def main(param_dict):
    try:
        api_key = param_dict["IAM_API_KEY"]
        couch_url = param_dict["COUCH_URL"]
        review_data = param_dict["review"]  # assuming review data is passed in param_dict
        
        client = Cloudant.iam(None, api_key, url=couch_url, connect=True)
        dbname = 'reviews'
        db = client[dbname]
        
        # Ensure "purchase_date" is a datetime object, not a string
        review_data["purchase_date"] = datetime.strptime(review_data["purchase_date"], '%m/%d/%Y')
        
        # Create the document in the database
        doc = db.create_document(review_data)
        
        # Ensure the document was successfully created
        if doc.exists():
            return {
                "statusCode": 201,
                "headers": { "Content-Type": "application/json" },
                "body": { "message": "Review created successfully" }
            }
        else:
            raise CloudantException('Failed to create document')

    except CloudantException as e:
        return {
            "statusCode": 500,
            "headers": { "Content-Type": "application/json" },
            "body": { "message": "Something went wrong on the server: {}".format(e) }
        }

    finally:
        if client:
            client.disconnect()
