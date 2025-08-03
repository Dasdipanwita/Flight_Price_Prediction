---
description: Repository Information Overview
alwaysApply: true
---

# Flight Price Finder Information

## Summary
A Streamlit web application that uses the Amadeus API to search for real-time flight prices between airports. The app allows users to select origin and destination airports, departure dates, number of passengers, and preferred currency.

## Structure
- `app.py`: Main Streamlit application file
- `.env`: Environment file containing Amadeus API credentials
- `flight_price.py`: Machine learning model training script for flight price prediction
- `flight_price_rf.pkl`: Trained Random Forest model for flight price prediction
- `requirements.txt`: List of Python dependencies
- `README.md`: Project documentation

## Language & Runtime
**Language**: Python 3.x
**Framework**: Streamlit
**API**: Amadeus Flight Offers Search API
**Package Manager**: pip

## Dependencies
**Main Dependencies**:
- streamlit: Web application framework
- amadeus: Official Amadeus API client
- python-dotenv: Environment variable management
- pandas: Data manipulation
- numpy: Numerical operations
- scikit-learn: Machine learning (for the prediction model)

## Build & Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Usage
The application provides a user interface for searching flight prices:
1. Select origin and destination airports
2. Choose departure date
3. Specify number of passengers and currency
4. View real-time flight prices and details

## API Configuration
The application requires Amadeus API credentials to be set in the `.env` file:
```
AMADEUS_API_KEY=your_api_key
AMADEUS_API_SECRET=your_api_secret
```

## Machine Learning Model
The repository includes a trained Random Forest model (`flight_price_rf.pkl`) for flight price prediction as a fallback when the API is not available. The model was trained on historical flight data using the script in `flight_price.py`.