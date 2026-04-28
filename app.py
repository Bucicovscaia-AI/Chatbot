import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from google import genai


# Load environment variables from .env file
load_dotenv()

# Read Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Configure Streamlit page
st.set_page_config(
    page_title="VisionText AI Assistant",
    page_icon="🤖",
    layout="centered"
)


st.title("VisionText AI Assistant")

st.write(
    "This AI chatbot can analyse text, images, or both using Google Gemini."
)


# Check if API key exists
if not GEMINI_API_KEY:
    st.error("Gemini API key not found. Please add it to your .env file.")
    st.stop()


# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


# Sidebar
st.sidebar.header("About")
st.sidebar.write(
    "This app uses Streamlit for the frontend and Gemini API for AI analysis."
)

st.sidebar.warning(
    "Do not upload private, confidential, medical, financial, or sensitive images."
)


# User inputs
user_prompt = st.text_area(
    "Enter your question or instruction:",
    placeholder="Example: Analyse this image and explain what you can see."
)

uploaded_image = st.file_uploader(
    "Upload an image:",
    type=["png", "jpg", "jpeg"]
)


image = None

if uploaded_image is not None:
    image = Image.open(uploaded_image)

    # Convert image to RGB to avoid image mode errors
    image = image.convert("RGB")

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )


# Analyse button
if st.button("Submit"):

    if not user_prompt.strip() and image is None:
        st.warning("Please type a question, upload an image, or do both.")

    else:
        with st.spinner("Gemini is analysing your input..."):
            try:
                # Text + image
                if user_prompt.strip() and image is not None:
                    contents = [
                        user_prompt,
                        image
                    ]

                # Image only
                elif image is not None:
                    contents = [
                        "Describe and analyse this image in detail. "
                        "Identify visible objects, possible context, and any uncertainty.",
                        image
                    ]

                # Text only
                else:
                    contents = user_prompt

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents
                )

                st.subheader("AI Response")

                if response.text:
                    st.write(response.text)
                else:
                    st.warning("Gemini returned an empty response.")

            except Exception as e:
                st.error("Something went wrong while contacting Gemini.")
                st.write(str(e))