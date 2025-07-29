import streamlit as st
import requests
from bs4 import BeautifulSoup
from together import Together
from dotenv import load_dotenv
import os

# Load environment variables from key.env file
load_dotenv('key.env')

# Get API key from environment variable
API_KEY = os.getenv('API_KEY')

# Validate API key is loaded
if not API_KEY:
    st.error("API key not found! Please check your key.env file.")
    st.stop()

def fetch_data_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except Exception as e:
        st.error(f"Error fetching the URL: {e}")
        return None

def ask_question(text, question):
    client = Together(api_key=API_KEY)

    messages = [
        {
            "role": "user",
            "content": f"{question} {text}"
        }
    ]

    try:
        response = client.chat.completions.create(
            model="lgai/exaone-3-5-32b-instruct",
            messages=messages
        )
        
        # Return the full answer without limiting sentences
        return response.choices[0].message.content

    except Exception as e:
        st.error(f"Error calling the AI model: {e}")
        return None

def main():
    st.title("Link-based QA App")

    url = st.text_input("Enter a URL:")

    if url:
        text = fetch_data_from_url(url)
        if text:
            st.success("Data fetched successfully!")

            question = st.text_input("Enter your question:")
            if question:
                answer = ask_question(text, question)
                st.write(f"Answer: {answer}")

if __name__ == "__main__":
    main()