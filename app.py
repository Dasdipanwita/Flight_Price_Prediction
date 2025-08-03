import streamlit as st
import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from amadeus import Client, ResponseError

st.title("✈️ Real-Time Flight Price Finder")
st.write("Powered by Amadeus API")

# --- Load Amadeus API credentials ---
try:
    load_dotenv()
    amadeus_api_key = os.getenv("AMADEUS_API_KEY")
    amadeus_api_secret = os.getenv("AMADEUS_API_SECRET")
    
    # Check if credentials are available
    if not amadeus_api_key or not amadeus_api_secret:
        st.error("❌ Amadeus API credentials not properly configured. Please check your .env file.")
        st.info("You need both AMADEUS_API_KEY and AMADEUS_API_SECRET in your .env file.")
        amadeus = None
    else:
        # Initialize Amadeus client
        amadeus = Client(
            client_id=amadeus_api_key,
            client_secret=amadeus_api_secret
        )
        st.success("✅ Connected to Amadeus API")
except ImportError:
    st.error("❌ Required packages not installed. Please run: pip install python-dotenv amadeus")
    amadeus = None


# --- User Inputs ---
col1, col2 = st.columns(2)

with col1:
    origin = st.selectbox("From (Airport Code)", ["DEL", "BOM", "BLR", "MAA", "CCU"], index=0)
    departure_date = st.date_input("Departure Date", datetime.now() + timedelta(days=7))  # Default to 1 week from now

with col2:
    destination = st.selectbox("To (Airport Code)", ["BLR", "DEL", "COK", "HYD"], index=0)
    adults = st.number_input("Number of Adults", min_value=1, max_value=9, value=1)

# Add currency selection
currency = st.selectbox("Currency", options=["INR", "USD", "EUR", "GBP"], index=0)

if st.button("Search for Flights"):
    if amadeus is None:
        st.error("❌ Amadeus client not initialized. Please check your API credentials.")
    else:
        st.write(f"Searching for flights from {origin} to {destination} on {departure_date.strftime('%Y-%m-%d')}...")
        
        try:
            # Format date as YYYY-MM-DD for Amadeus API
            formatted_date = departure_date.strftime("%Y-%m-%d")
            
            # Call Amadeus Flight Offers Search API
            flight_offers = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=formatted_date,
                adults=adults,
                currencyCode=currency,
                max=5  # Limit to 5 results
            )
            
            # Process and display results
            if flight_offers.data:
                st.success(f"Found {len(flight_offers.data)} flights!")
                
                for offer in flight_offers.data:
                    # Extract price
                    price = offer['price']['total']
                    currency_code = offer['price']['currency']
                    
                    # Extract itinerary details
                    itinerary = offer['itineraries'][0]  # First itinerary (outbound)
                    segments = itinerary['segments']
                    
                    # Get first and last segment for departure and arrival times
                    first_segment = segments[0]
                    last_segment = segments[-1]
                    
                    # Extract carrier code
                    carrier_code = first_segment['carrierCode']
                    
                    # Format departure and arrival times
                    departure_time = datetime.strptime(
                        first_segment['departure']['at'], 
                        "%Y-%m-%dT%H:%M:%S"
                    ).strftime('%I:%M %p')
                    
                    arrival_time = datetime.strptime(
                        last_segment['arrival']['at'], 
                        "%Y-%m-%dT%H:%M:%S"
                    ).strftime('%I:%M %p')
                    
                    # Number of stops
                    stops = len(segments) - 1
                    stop_text = "non-stop" if stops == 0 else f"{stops} stop{'s' if stops > 1 else ''}"
                    
                    # Display flight information
                    st.markdown("---")
                    st.subheader(f"Price: {currency_code} {price}")
                    st.write(f"**Airline:** {carrier_code}")
                    st.write(f"**Departure:** {departure_time} from {first_segment['departure']['iataCode']}")
                    st.write(f"**Arrival:** {arrival_time} at {last_segment['arrival']['iataCode']}")
                    st.write(f"**Stops:** {stop_text}")
                    
                    # Display flight details in an expander
                    with st.expander("View Flight Details"):
                        for i, segment in enumerate(segments):
                            st.write(f"**Segment {i+1}:**")
                            st.write(f"From: {segment['departure']['iataCode']} at {datetime.strptime(segment['departure']['at'], '%Y-%m-%dT%H:%M:%S').strftime('%I:%M %p')}")
                            st.write(f"To: {segment['arrival']['iataCode']} at {datetime.strptime(segment['arrival']['at'], '%Y-%m-%dT%H:%M:%S').strftime('%I:%M %p')}")
                            st.write(f"Flight: {segment['carrierCode']} {segment['number']}")
                            st.write(f"Duration: {segment['duration']}")
                            if i < len(segments) - 1:
                                st.write("---")
                    
                    # Add a booking button (simulated)
                    if st.button(f"Book this flight for {currency_code} {price}", key=f"book_{flight_offers.data.index(offer)}"):
                        st.success("Booking simulation successful! (This is a demo)")
            else:
                st.warning("No flights found for the selected criteria.")
                
        except ResponseError as error:
            st.error(f"Amadeus API Error: {error}")
        except Exception as e:
            st.error(f"Error: {str(e)}")