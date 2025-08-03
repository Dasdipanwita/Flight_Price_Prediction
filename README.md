# Flight Price Finder

A real-time flight price search application powered by the Amadeus API.

## Features

- Search for flights between major airports
- View real-time pricing information
- Filter by date, number of passengers, and currency
- View detailed flight information including stops and segments
- Simple and intuitive user interface

## Technologies Used

- Python
- Streamlit for the web interface
- Amadeus API for flight data
- Python-dotenv for environment variable management

## Setup Instructions

1. Clone this repository
2. Install the required packages:
   ```
   pip install streamlit amadeus python-dotenv
   ```
3. Create a `.env` file in the project root with your Amadeus API credentials:
   ```
   AMADEUS_API_KEY=your_api_key
   AMADEUS_API_SECRET=your_api_secret
   ```
4. Run the application:
   ```
   streamlit run app.py
   ```

## How to Use

1. Select your origin and destination airports
2. Choose your departure date
3. Specify the number of passengers
4. Select your preferred currency
5. Click "Search for Flights" to see available options
6. Expand flight details to see more information about each segment

## Notes

- This application requires a valid Amadeus API key and secret
- The application is for demonstration purposes only
- No actual bookings are made through this interface

## Future Enhancements

- Add return flight search capability
- Implement more filtering options (airlines, time of day, etc.)
- Add fare class selection
- Integrate with a booking system
- Add user accounts and saved searches

## License

This project is licensed under the MIT License - see the LICENSE file for details.