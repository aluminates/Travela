import streamlit as st
st.set_page_config(page_title="Travela: Your Travel Buddy", page_icon=":airplane:")
from streamlit_option_menu import option_menu
from config import set_background
from flight_utils import handle_flight_booking
from transfer_utils import handle_transfer_booking

def main():
    st.title("Travela: Your Travel Buddy!")
    set_background()

    with st.sidebar:
        selected = option_menu(
            "Menu",
            ["Home", "Search Flights", "Transfer Options", "Chat History"],
            icons=["house", "search", "truck", "clock"],
            menu_icon="cast",
            default_index=0,
        )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if selected == "Home":
        st.write("Hi, I'm Travela! How can I assist you with your travel plans today?")

    elif selected == "Search Flights":
        user_input = st.text_input("Enter your flight details: (e.g., 'Flight from NYC to LAX on 2024-08-01')")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            response = handle_flight_booking(user_input)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write("Travela:", response)

    elif selected == "Transfer Options":
        user_input = st.text_input("Enter your transfer details: (e.g., 'Transfer from Paris to London on 2024-08-01 for 2 passengers')")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            response = handle_transfer_booking(user_input)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write("Travela:", response)

    elif selected == "Chat History":
        st.write("Chat History:")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

if __name__ == "__main__":
    main()