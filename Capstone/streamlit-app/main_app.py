import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
import pickle
import base64
import os

# Ensure your AWS credentials are set in your environment or in ~/.aws/credentials

local_image_path = '/app/files/pickled_image.pkl'  # Path inside Docker

def s3_download(s3_bucket, s3_file_key, local_file_path):
    try:
        s3 = boto3.client("s3")
        # Ensure directory exists
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        s3.download_file(s3_bucket, s3_file_key, local_file_path)
        st.success("File downloaded successfully.")
    except Exception as e:
        st.error(f"Failed to download file: {e}")

def load_and_display_image(image_path):
    with open(image_path, "rb") as file:
        image_data = pickle.load(file)
        print(f"Type of loaded data: {type(image_data)}")  # Debugging line
        st.image(image_data, caption="Loaded Image", use_column_width=True)


# Example usage
s3_bucket_name = "capstone-houseprice-prediction"
s3_file_key = "files/pickled_image.pkl"
s3_download(s3_bucket_name, s3_file_key, local_image_path)

# Load and display the deserialized image
load_and_display_image(local_image_path)

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def add_bg_from_local(image_file):
    bin_str = get_image_base64(image_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .overlayBg {{
        background-color: rgba(255, 255, 255, 0.6); /* Transparency */
        border-radius: 10px;
        padding: 10px;
        color: black; /* Default text color */
    }}
    .overlayBg h1, .overlayBg h2 {{
        color: black !important; /* Ensuring that <h1> and <h2> are black */
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

add_bg_from_local(local_image_path)  # Adjust the path to the image

# Additional Streamlit app content
st.set_page_config(page_title="Welcome to the World of Homes", layout="wide")
st.markdown("""
<div>
    <h1>Welcome to the World of Homes</h1>
    <h2>Unlock the Door to Real Estate Mastery</h2>
    <p>Welcome to our Real Estate Analysis Platform—where data meets strategy.</p>
    ...
</div>
""", unsafe_allow_html=True)
