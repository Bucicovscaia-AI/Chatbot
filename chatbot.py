import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key
GEMINI_API_KEY = os.getenv("AIzaSyD8tAm7wuh8xy5wkkUsol0B_YaGTI5oaDY")

# Configure Streamlit page
st.set_page_config(
    page_title="VisionText AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# Page title
st.title("🤖 VisionText AI Assistant")

st.write(
    "Upload an image, type a question, and let Gemini analyse both text and image."
)

# Check API key
if not GEMINI_API_KEY:
    st.error("Gemini API key not found. Please add it to your .env file.")
    st.stop()

# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Sidebar information
st.sidebar.header("About this App")
st.sidebar.write(
    "This chatbot uses Gemini API to analyse text and images. "
    "It is designed for beginner AI students learning multimodal AI."
)

st.sidebar.warning(
    "Do not upload private, confidential, medical, identity, or sensitive images."
)

# User text input
user_prompt = st.text_area(
    "Enter your question:",
    placeholder="Example: Analyse this image and explain what you can see."
)

# Image upload input
uploaded_image = st.file_uploader(
    "Upload an image:",
    type=["png", "jpg", "jpeg"]
)

image = None

# Display uploaded image
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Analyse button
if st.button("Analyse with Gemini"):
    if not user_prompt and image is None:
        st.warning("Please enter a question or upload an image.")

    else:
        with st.spinner("Gemini is analysing your input..."):
            try:
                # Decide what content to send to Gemini
                if image is not None and user_prompt:
                    contents = [user_prompt, image]

                elif image is not None:
                    contents = [
                        "Describe and analyse this image in detail. "
                        "Mention visible objects, possible context, and any uncertainty.",
                        image
                    ]

                else:
                    contents = user_prompt

                # Send request to Gemini
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents
                )

                # Display response
                st.subheader("AI Response")
                st.write(response.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")