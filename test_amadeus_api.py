import os
from dotenv import load_dotenv
from amadeus import Client, ResponseError
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Get API credentials
api_key = os.getenv("AMADEUS_API_KEY")
api_secret = os.getenv("AMADEUS_API_SECRET")

if not api_key or not api_secret or api_secret == "YOUR_AMADEUS_API_SECRET":
    print("Error: API credentials not found or not properly configured in .env file")
    print("Make sure you have both AMADEUS_API_KEY and AMADEUS_API_SECRET in your .env file")
    print("Your current API key:", api_key)
    print("Your current API secret:", "Not set correctly" if not api_secret or api_secret == "YOUR_AMADEUS_API_SECRET" else "Set (hidden)")
    exit(1)

print(f"Testing Amadeus API with key: {api_key[:4]}{'*' * (len(api_key) - 8)}{api_key[-4:]}")

# Initialize Amadeus client
try:
    amadeus = Client(
        client_id=api_key,
        client_secret=api_secret
    )
    
    # Calculate tomorrow's date
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")
    
    print(f"Searching for flights from DEL to BLR on {tomorrow_str}")
    
    # Call Flight Offers Search API
    flight_offers = amadeus.shopping.flight_offers_search.get(
        originLocationCode="DEL",
        destinationLocationCode="BLR",
        departureDate=tomorrow_str,
        adults=1,
        currencyCode="INR",
        max=1
    )
    
    # Process results
    if flight_offers.data:
        offer = flight_offers.data[0]
        price = offer['price']['total']
        currency = offer['price']['currency']
        
        # Get carrier code
        carrier_code = offer['itineraries'][0]['segments'][0]['carrierCode']
        
        print(f"\nAPI TEST SUCCESSFUL!")
        print(f"Found flight for {currency} {price} with {carrier_code}")
    else:
        print("\nAPI TEST SUCCESSFUL, but no flights found for the selected criteria.")
        
except ResponseError as error:
    print(f"\nAPI TEST FAILED with Amadeus error: {error}")
except Exception as e:
    print(f"\nAPI TEST FAILED with error: {str(e)}")