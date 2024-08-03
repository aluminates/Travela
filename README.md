# Travela - Your Travel Buddy!

Are you tired of flying out to a destination but realising you don't have a cab to your hotel? Travela's here to sort you out! Now find both flight and transfer offers in the same place.

Travela is a Streamlit-based web application designed to assist users with their travel plans. It integrates flight search, transfer options, and a chat interface powered by a language model to provide a comprehensive travel planning experience.


# Key Components

1. User Interface (main.py): Built with Streamlit for a responsive web interface, it features a sidebar menu with options for Home, Search Flights, Transfer Options, and Chat History. It maintains a session state to store conversation history.
2. Flight Booking (flight_utils.py): It parses user queries for flight searches and integrates with Amadeus API to fetch flight information. After formatting flight data for user-friendly display, it uses a language model to summarize and recommend flight options. Similarly, with transfer_utils.py
3. Amadeus API Integration (amadeus_api.py): It manages connection to Amadeus travel API and provides functions for location code retrieval, flight search, and transfer search.
4. Language Model Integration (llama_api.py): It implements a custom LlamaAgent class for natural language processing and connects to a local LLM server (llama3-8b-instruct) to generate human-like responses for travel recommendations.


# Technical Details

- Language: Python
- Main Framework: Streamlit
- APIs: Amadeus (for travel data), LMStudio running llama3-8b-instruct
- Additional Libraries: streamlit_option_menu, autogen, requests, langchain


# Instructions to Run

1) Download and install LMStudio on your local machine. Install Meta Llama3 or any other open-source LLM of your preference.
2) Run the installed LLM as a server. It should run on port 1234.
3) Set up an account on Amadeus and create an API key.
4) Change the image path in the config.py accordingly.
5) Change the API_KEY and API_SECRET accordingly.
6) Install dependencies by running "pip install -r requirements.txt" in your project directory.
7) Execute the command "streamlit run app.py" to run the application.


# Future Work

Project is still in progress, I will continue to add functionality and features. Reach out to me if you find any code breaks.
