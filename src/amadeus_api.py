from amadeus import Client, ResponseError

amadeus = Client(
    client_id='ENTER_API_KEY_HERE',
    client_secret='ENTER_API_SECRET_HERE'
)

def get_location_code(keyword, subType='CITY'):
    try:
        response = amadeus.reference_data.locations.get(
            keyword=keyword,
            subType=subType
        )
        
        if response.data:
            return response.data[0]['iataCode']
        else:
            return None
    except ResponseError as error:
        print(f"An error occurred: {error}")
        return None

def search_flights(origin, destination, date):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=date,
            adults=1,
            max=3
        )
        return response.data
    except ResponseError as error:
        return f"An error occurred: {error}"

def search_transfer(start_location, end_location, start_date, passengers=2):
    try:
        response = amadeus.shopping.transfer_offers.post(
            body={
                "startLocationCode": start_location,
                "endAddressLine": "City Center",
                "endCityName": end_location,
                "startDateTime": f"{start_date}T10:00:00",
                "passengers": passengers,
                "transferType": "PRIVATE"
            }
        )
        return response.data
    except ResponseError as error:
        print(f"An error occurred: {error}")
        return f"An error occurred: {error}"
