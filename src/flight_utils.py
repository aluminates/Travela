import re
from datetime import datetime, timedelta
from amadeus_api import get_location_code, search_flights
from llama_api import llama_chat
from langchain.prompts import ChatPromptTemplate

def parse_flight_query(response):
    response = response.lower()
    origin = None
    destination = None
    date = None

    origin_match = re.search(r'from\s+(\w+)', response)
    destination_match = re.search(r'to\s+(\w+)', response)

    if origin_match:
        origin_keyword = origin_match.group(1)
        origin = get_location_code(origin_keyword)

    if destination_match:
        destination_keyword = destination_match.group(1)
        destination = get_location_code(destination_keyword)

    date_patterns = [
        r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
        r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
        r'\d{1,2}\s(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s\d{4}',  # 15 Jan 2024
        r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s\d{1,2},?\s\d{4}',  # January 15, 2024
        r'(?:tomorrow|next week|next month)'  # relative dates
    ]

    for pattern in date_patterns:
        match = re.search(pattern, response)
        if match:
            date_str = match.group()
            try:
                if date_str == 'tomorrow':
                    date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
                elif date_str == 'next week':
                    date = (datetime.now() + timedelta(weeks=1)).strftime('%Y-%m-%d')
                elif date_str == 'next month':
                    date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
                else:
                    date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                try:
                    date = datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
                except ValueError:
                    try:
                        date = datetime.strptime(date_str, '%d %b %Y').strftime('%Y-%m-%d')
                    except ValueError:
                        try:
                            date = datetime.strptime(date_str, '%B %d, %Y').strftime('%Y-%m-%d')
                        except ValueError:
                            date = None

    if date is None:
        date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    if origin is None and destination is None:
        raise ValueError("Could not extract origin and destination from the query.")
    elif origin is None:
        raise ValueError("Could not extract origin from the query.")
    elif destination is None:
        raise ValueError("Could not extract destination from the query.")
    
    if origin == destination:
        raise ValueError("Origin and destination cannot be the same.")

    return origin, destination, date

def format_flight_info(flights):
    formatted_flights = []
    for flight in flights:
        price = flight['price']['total']
        currency = flight['price']['currency']
        itineraries = flight['itineraries'][0]
        segments = itineraries['segments']
        
        departure = segments[0]['departure']
        arrival = segments[-1]['arrival']
        
        formatted_flight = f"Flight from {departure['iataCode']} to {arrival['iataCode']}:\n"
        formatted_flight += f"Departure: {departure['at']}\n"
        formatted_flight += f"Arrival: {arrival['at']}\n"
        formatted_flight += f"Price: {price} {currency}\n"
        formatted_flight += "Segments:\n"
        
        for segment in segments:
            formatted_flight += f"  {segment['departure']['iataCode']} to {segment['arrival']['iataCode']} - "
            formatted_flight += f"Carrier: {segment['carrierCode']}, Flight: {segment['number']}\n"
        
        formatted_flights.append(formatted_flight)
    
    return "\n\n".join(formatted_flights)

def handle_flight_booking(query):
    try:
        origin, destination, date = parse_flight_query(query)
        flights = search_flights(origin, destination, date)
        
        if isinstance(flights, str): 
            return flights
        
        formatted_flights = format_flight_info(flights)
        
        prompt = ChatPromptTemplate.from_template("""
        You are a helpful travel assistant. Based on the following flight information taken from JSON Amadeus API calls, provide a summary of the best options for the user (include briefly the important times, prices and layovers). 
        JSON Information:
        {flights}

        Please provide a concise summary and recommendation.
        """)
        
        formatted_prompt = prompt.format(flights=formatted_flights)
        
        llm_response = llama_chat([
            {"role": "system", "content": "You are a helpful travel assistant."},
            {"role": "user", "content": formatted_prompt}
        ])
        
        return llm_response
    except ValueError as e:
        return str(e)