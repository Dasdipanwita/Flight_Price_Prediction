import streamlit as st
import pandas as pd
import numpy as np
import pickle
from datetime import datetime

st.title("✈️ Flight Price Predictor")
st.write("Powered by a Machine Learning Model")
st.info("Note: This tool predicts prices based on historical data, it does not show live fares.")

# --- Load the trained machine learning model ---
try:
    # Use a relative path to find the model in the same directory
    with open("flight_price_rf.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    
    # Get the exact feature names from the model
    if hasattr(model, 'feature_names_in_'):
        model_features = model.feature_names_in_
        st.write("Model loaded successfully!")
    else:
        st.error("Model doesn't have feature names attribute.")
        st.stop()
    
except FileNotFoundError:
    st.error("❌ Model file 'flight_price_rf.pkl' not found.")
    st.write("Please make sure the model file is in the same directory as this script.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the model: {e}")
    st.stop()


# --- User Inputs ---
col1, col2 = st.columns(2)

with col1:
    origin = st.selectbox("From (Airport Code)", ["DEL", "BOM", "BLR", "MAA", "CCU"], index=0)
    departure_date = st.date_input("Departure Date", datetime.now())

with col2:
    destination = st.selectbox("To (Airport Code)", ["BLR", "DEL", "COK", "HYD"], index=0)
    adults = st.number_input("Number of Adults", min_value=1, max_value=9, value=1)


if st.button("Predict Flight Prices"):
    st.write(f"Predicting prices for flights from {origin} to {destination}...")

    # --- Prepare data for the model ---
    # The model expects specific numerical inputs, so we must convert the user's choices.

    # 1. Date of Journey
    journey_day = departure_date.day
    journey_month = departure_date.month

    # 2. Airline mapping to full names
    # We will predict for a few major airlines to give a range of options.
    airlines = ["IndiGo", "Air India", "SpiceJet", "Vistara", "GoAir"]
    
    # 3. Source and Destination mapping
    source_mapping = {
        'BOM': 'Mumbai', 
        'BLR': 'Bangalore', # Bangalore is the reference category (not in features)
        'DEL': 'Delhi', 
        'CCU': 'Kolkata', 
        'MAA': 'Chennai'
    }
    
    dest_mapping = {
        'COK': 'Cochin', 
        'BLR': 'Bangalore', # Bangalore is the reference category (not in features)
        'DEL': 'Delhi', 
        'HYD': 'Hyderabad'
    }

    source_name = source_mapping.get(origin)
    dest_name = dest_mapping.get(destination)

    if source_name is None or dest_name is None:
        st.error("The selected origin or destination is not supported by this model.")
        st.stop()

    # --- Generate Predictions for Different Airlines ---
    predictions = []
    
    # We'll create some sample times for prediction (same for all airlines)
    dep_hour, dep_min = (9, 30) # Morning
    arrival_hour, arrival_min = (12, 15) # Afternoon
    duration_hours = arrival_hour - dep_hour
    duration_mins = arrival_min - dep_min if arrival_min >= dep_min else (arrival_min + 60 - dep_min)
    
    for airline_name in airlines:
        try:
            # Create a DataFrame with all features initialized to 0
            features_df = pd.DataFrame(0, index=[0], columns=model_features)
            
            # Set the non-categorical features
            features_df['Total_Stops'] = 0  # Assuming non-stop
            features_df['Journey_day'] = journey_day
            features_df['Journey_month'] = journey_month
            features_df['Dep_hour'] = dep_hour
            features_df['Dep_min'] = dep_min
            features_df['Arrival_hour'] = arrival_hour
            features_df['Arrival_min'] = arrival_min
            features_df['Duration_hours'] = duration_hours
            features_df['Duration_mins'] = duration_mins
            
            # Set the airline feature (one-hot encoded)
            airline_col = f'Airline_{airline_name}'
            if airline_col in features_df.columns:
                features_df[airline_col] = 1
            
            # Set the source feature (one-hot encoded)
            # Note: Bangalore is the reference category and doesn't have a column
            if source_name != 'Bangalore':
                source_col = f'Source_{source_name}'
                if source_col in features_df.columns:
                    features_df[source_col] = 1
            
            # Set the destination feature (one-hot encoded)
            # Note: Bangalore is the reference category and doesn't have a column
            if dest_name != 'Bangalore':
                dest_col = f'Destination_{dest_name}'
                if dest_col in features_df.columns:
                    features_df[dest_col] = 1
            
            # Optional: Display the features for debugging
            # st.write(f"Features for {airline_name}:", features_df)

            # Predict the price
            prediction = model.predict(features_df)[0]
            predictions.append({
                "airline": airline_name,
                "price": int(prediction * adults) # Adjust for number of adults
            })
        except Exception as e:
            st.warning(f"Could not generate prediction for {airline_name}. Error: {e}")
            st.write("Error details:", str(e))

    # --- Display Results ---
    if predictions:
        st.success(f"Found {len(predictions)} predicted flight options!")
        
        # Sort by price
        predictions.sort(key=lambda x: x["price"])
        
        for flight in predictions:
            st.markdown("---")
            st.subheader(f"Airline: {flight['airline']}")
            st.write(f"**Predicted Price:** ₹{flight['price']:,} (for {adults} adult(s))")
            st.write("Departure: Morning (Sample)")
            st.write("Arrival: Afternoon (Sample)")
            st.write("Stops: Non-stop (Sample)")

    else:
        st.warning("Could not generate any price predictions for the selected criteria.")