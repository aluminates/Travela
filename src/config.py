import streamlit as st
import base64

def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def set_background():
    background_image = get_base64_of_image(r"D:\Travela\images\airport.jpg")
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{background_image}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )