# import streamlit as st
# import base64
# import boto3
# import sys
# import pickle
# sys.path.append("/Users/siddhant/housepriceproject")

# from botocore.exceptions import NoCredentialsError

# image_path = '/app/files/image.pkl'
# s3_image = 'files/image.pkl'



# bucket_name = "capstone-houseprice-prediction"

# def s3_download(s3_bucket, s3_file_path, local_file):
#     s3 = boto3.client("s3")

#     s3.download_file(s3_bucket, s3_file_path, local_file)



# s3_download(bucket_name, s3_image, image_path)

# with open(image_path, 'rb') as file:
#     image = pickle.load(file)
# # Set page configuration
# st.set_page_config(page_title="Welcome to the World of Homes", layout="wide")

# # Function to get base64 of the image file
# def get_image_base64(image_path):
#     with open(image_path, "rb") as img_file:
#         return base64.b64encode(img_file.read()).decode()

# # Custom CSS to inject into the Streamlit app
# # Custom CSS to inject into the Streamlit app
# def add_bg_from_local(image_file):
#     bin_str = get_image_base64(image_file)
#     page_bg_img = f'''
#     <style>
#     .stApp {{
#         background-image: url("data:image/jpeg;base64,{bin_str}");
#         background-size: cover;
#         background-repeat: no-repeat;
#         background-attachment: fixed;
#     }}
#     .overlayBg {{
#         background-color: rgba(255, 255, 255, 0.6); /* Transparency */
#         border-radius: 10px;
#         padding: 10px;
#         color: black; /* Default text color */
#     }}
#     .overlayBg h1, .overlayBg h2 {{
#         color: black !important; /* Ensuring that <h1> and <h2> are black */
#     }}
#     </style>
#     '''
#     st.markdown(page_bg_img, unsafe_allow_html=True)

# add_bg_from_local(image)  # Adjust the path to the image

# st.markdown("""
# <div class="overlayBg">
#     <h1>Welcome to the World of Homes</h1>
#     <h2>Unlock the Door to Real Estate Mastery</h2>
#     <p>Welcome to our Real Estate Analysis Platform—where data meets strategy.</p>
#     <ul>
#         <li><b>Tailored Insights:</b> Whether you're a first-time homebuyer or a seasoned investor, our platform offers tailored insights that cater to your needs. Explore interactive charts, maps, and analytics designed to empower your decision-making process.</li>
#         <li><b>Comprehensive Coverage:</b> From bustling city centers to serene suburbs, navigate through an extensive database of properties, market trends, and price comparisons at your fingertips.</li>
#     </ul>
#     <p><i>Begin your journey with us today and see where data can take you. Your dream property awaits!</i></p>
# </div>
# """, unsafe_allow_html=True)

import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
import pickle
import base64
import os

# Ensure your AWS credentials are set in your environment or in ~/.aws/credentials

local_image_path = '/app/files/image.pkl'  # Path inside Docker

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
        st.image(image_data, caption="Loaded Image", use_column_width=True)

# Example usage
s3_bucket_name = "capstone-houseprice-prediction"
s3_file_key = "files/image.pkl"
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
