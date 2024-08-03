import re
from amadeus_api import get_location_code, search_transfer
from llama_api import llama_chat
from langchain.prompts import ChatPromptTemplate

def format_transfer_info(transfers):
    formatted_transfers = []
    for transfer in transfers:
        price = transfer['price']['total']
        currency = transfer['price']['currency']
        vehicle = transfer['vehicle']
        
        formatted_transfer = f"Transfer Option:\n"
        formatted_transfer += f"Price: {price} {currency}\n"
        formatted_transfer += f"Vehicle: {vehicle['name']} (Capacity: {vehicle['maxPassengers']})\n"
        formatted_transfer += f"Category: {vehicle['category']}\n"
        
        formatted_transfers.append(formatted_transfer)
    
    return "\n\n".join(formatted_transfers)

def handle_transfer_booking(query):
    try:
        match = re.search(r'from (\w+) to (\w+) on (\d{4}-\d{2}-\d{2})(?: for (\d+) passengers)?', query, re.IGNORECASE)
        if not match:
            return "Invalid query format. Please use the format: Transfer from [START] to [END] on [DATE] for [PASSENGERS] passengers"

        start_location = get_location_code(match.group(1))
        end_location = get_location_code(match.group(2))
        date = match.group(3)
        passengers = int(match.group(4)) if match.group(4) else 2

        if not start_location or not end_location:
            return "Could not find location codes for the specified cities."

        transfers = search_transfer(start_location, end_location, date, passengers)
        
        if isinstance(transfers, str): 
            return transfers
        
        formatted_transfers = format_transfer_info(transfers)
        
        prompt = ChatPromptTemplate.from_template("""
        You are a helpful travel assistant. Based on the following transfer information taken from JSON Amadeus API calls, provide a summary of the best options for the user (include briefly the prices, vehicle types, and any other relevant details). 
        Transfer Information:
        {transfers}

        Please provide a concise summary and recommendation.
        """)
        
        formatted_prompt = prompt.format(transfers=formatted_transfers)
        
        llm_response = llama_chat([
            {"role": "system", "content": "You are a helpful travel assistant."},
            {"role": "user", "content": formatted_prompt}
        ])
        
        return llm_response
    except ValueError as e:
        return str(e)