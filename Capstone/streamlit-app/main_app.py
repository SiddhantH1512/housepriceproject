import streamlit as st
import base64
import boto3
import sys
import pickle
sys.path.append("/Users/siddhant/housepriceproject")
from Capstone.logger import logging
from botocore.exceptions import NoCredentialsError

image_path = '/app/files/image.pkl'
s3_image = 'files/image.pkl'



bucket_name = "capstone-houseprice-prediction"

def s3_download(s3_bucket, s3_file_path, local_file):
    s3 = boto3.client("s3")
    try:
        logging.info(f"Downloading file {local_file} residing in S3 bucket {s3_bucket} at {s3_file_path}")
        s3.download_file(s3_bucket, s3_file_path, local_file)
        logging.info(f"Downloaded file {local_file} residing in S3 bucket {s3_bucket} at {s3_file_path}")
    except FileNotFoundError:
        logging.exception(f"The file {local_file} was not found.")
    except NoCredentialsError:
        logging.exception("Credentials not available.")
    except Exception as e:
        logging.exception(f"An error occurred while downloading {local_file}: {e}")


s3_download(bucket_name, s3_image, image_path)

with open(image_path, 'rb') as file:
    image = pickle.load(file)
# Set page configuration
st.set_page_config(page_title="Welcome to the World of Homes", layout="wide")

# Function to get base64 of the image file
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Custom CSS to inject into the Streamlit app
# Custom CSS to inject into the Streamlit app
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



# Apply the background image from a local file
add_bg_from_local(image)  # Adjust the path to the image

# # Sidebar for navigation
# st.sidebar.title("Navigation")
# navigation_options = ["Home", "Price Analysis", "Sector Insights", "Property Finder"]
# selection = st.sidebar.selectbox("Go to", navigation_options)

# Main body of the app with an overlay background for text
st.markdown("""
<div class="overlayBg">
    <h1>Welcome to the World of Homes</h1>
    <h2>Unlock the Door to Real Estate Mastery</h2>
    <p>Welcome to our Real Estate Analysis Platform—where data meets strategy.</p>
    <ul>
        <li><b>Tailored Insights:</b> Whether you're a first-time homebuyer or a seasoned investor, our platform offers tailored insights that cater to your needs. Explore interactive charts, maps, and analytics designed to empower your decision-making process.</li>
        <li><b>Comprehensive Coverage:</b> From bustling city centers to serene suburbs, navigate through an extensive database of properties, market trends, and price comparisons at your fingertips.</li>
    </ul>
    <p><i>Begin your journey with us today and see where data can take you. Your dream property awaits!</i></p>
</div>
""", unsafe_allow_html=True)

# Rest of your Streamlit app code












# import streamlit as st 
# import pandas as pd 
# import plotly.express as px
# import matplotlib.pyplot as plt 
# from wordcloud import WordCloud
# import pickle
# import ast
# import numpy as np 
# import boto3
# import sys
# sys.path.append("/Users/siddhant/housepriceproject")
# from Capstone.logger import logging
# from botocore.exceptions import NoCredentialsError


# def run_page2():
#     st.title("Page 2")
#     model_path1 = '/app/models/cosinse_sim.pkl'
#     model_path2 = '/app/models/cosinse_sim2.pkl'
#     model_path3 = '/app/models/cosinse_sim3.pkl'
#     wordcloud = '/app/models/wordcloud_data.pkl'
#     df_path = '/app/models/locationdf.pkl'

#     s3_path1 = 'models/cosinse_sim.pkl'
#     s3_path2 = 'models/cosinse_sim2.pkl'
#     s3_path3 = 'models/cosinse_sim3.pkl'
#     s3_path_df_4 = 'files/locationdf.pkl'
#     s3_path_wordcloud_5 = 'files/wordcloud_data.pkl'



#     bucket_name = "capstone-houseprice-prediction"

#     def s3_download(s3_bucket, s3_file_path, local_file):
#         s3 = boto3.client("s3")
#         try:
#             logging.info(f"Downloading file {local_file} residing in S3 bucket {s3_bucket} at {s3_file_path}")
#             s3.download_file(s3_bucket, s3_file_path, local_file)
#             logging.info(f"Downloaded file {local_file} residing in S3 bucket {s3_bucket} at {s3_file_path}")
#         except FileNotFoundError:
#             logging.exception(f"The file {local_file} was not found.")
#         except NoCredentialsError:
#             logging.exception("Credentials not available.")
#         except Exception as e:
#             logging.exception(f"An error occurred while downloading {local_file}: {e}")

#     # Upload each file
#     s3_download(bucket_name, s3_path1, model_path1)
#     s3_download(bucket_name, s3_path2, model_path2)
#     s3_download(bucket_name, s3_path3, model_path3)
#     s3_download(bucket_name, s3_path_df_4, df_path)
#     s3_download(bucket_name, s3_path_wordcloud_5, wordcloud)


#     with open(model_path1, 'rb') as file:
#         cosine_sim1 = pickle.load(file)

#     with open(model_path2, 'rb') as file:
#         cosine_sim2 = pickle.load(file)
        
#     with open(model_path3, 'rb') as file:
#         cosine_sim3 = pickle.load(file)
        
#     with open(df_path, 'rb') as file:
#         locationdf = pickle.load(file)
        
#     with open(wordcloud, 'rb') as file:
#         wordcloud_data = pickle.load(file)
        

#     st.title("Page 2")

#     # STREAMLIT LAYOUT
#     st.header("Sector wise price per sqft map")

#     # PREPARING DATA FOR GEOMAP
#     new_df = pd.read_csv("/Users/siddhant/housepriceproject/Capstone/datasets/data_viz1.csv")
#     groupdf = new_df.groupby("sector")[['price','price_per_sqft','built_up_area','latitude','longitude']].mean()

#     # GEOMAP
#     fig = px.scatter_mapbox(groupdf, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
#                     color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
#                     mapbox_style="open-street-map", width=1200, height=700, hover_name=groupdf.index)
#     st.plotly_chart(fig, use_container_width=True)





#     # STREAMLIT LAYOUT
#     st.header("Sector-specific Wordcloud")
#     # FUNCTION TO PLOT SECTOR WISE WORDCLOUD
#     def generate_wordcloud(sector):
#         # Extracting features for the selected sector
#         features = wordcloud_data[wordcloud_data['sector'] == sector]['features']
#         main = []
#         for feature_list in features.dropna():
#             main.extend(ast.literal_eval(feature_list))
#         text = ' '.join(main)

#         # Generate wordcloud
#         wordcloud = WordCloud(width=800, height=800,
#                             background_color='white',
#                             stopwords=set(['s']),  # Add any stopwords here
#                             min_font_size=10).generate(text)

#         # Display wordcloud using matplotlib
#         plt.figure(figsize=(8, 8), facecolor=None)
#         plt.imshow(wordcloud, interpolation='bilinear')
#         plt.axis("off")
#         plt.tight_layout(pad=0)
#         st.pyplot()

#     # Dropdown for sector selection
#     selected_sector = st.selectbox("Select a sector", wordcloud_data['sector'].unique())
#     # Display the wordcloud for the selected sector
#     if selected_sector:
#         generate_wordcloud(selected_sector)

#     st.set_option('deprecation.showPyplotGlobalUse', False)



# # STREAMLIT LAYOUT
# st.header("Area vs Price")

# property_type = st.selectbox("Select poperty type", ["flat", "house"])

# # PLOTTING SCATTER PLOT AREA VS PRICE
# if property_type == "flat":
#     fig1 = px.scatter(new_df[new_df["property_type"] == "flat"], x="built_up_area", y="price", color="bedRoom")
#     st.plotly_chart(fig1, use_container_width=True)
# else:
#     fig1 = px.scatter(new_df[new_df["property_type"] == "house"], x="built_up_area", y="price", color="bedRoom")
#     st.plotly_chart(fig1, use_container_width=True)



# # STREAMLIT LAYOUT
# st.header("BHK Pie Chart")

# sector_list = new_df["sector"].unique().tolist()
# sector_list.insert(0, "overall")

# selected_sector = st.selectbox("Select sector", sector_list)
# # PLOTTING PIE CHART FOR BEDROOMS SECTORWISE
# if selected_sector == "overall":
#     fig2 = px.pie(new_df, names="bedRoom")
#     st.plotly_chart(fig2, use_container_width=True)
# else:
#     fig2 = px.pie(new_df[new_df["sector"] == selected_sector], names="bedRoom")
#     st.plotly_chart(fig2, use_container_width=True)
    
    

# # STREAMLIT LAYOUT
# st.header("BHK price range")

# allsectors = new_df["sector"].unique().tolist()
# allsectors.insert(0, "overall")

# sector_selected = st.selectbox("Select required sector", allsectors)
# # BOXPLOT FOR BHK WIS PRICE
# if sector_selected == "overall":
#     fig3 = px.box(new_df[new_df["bedRoom"] <= 4], x="bedRoom", y="price")
#     st.plotly_chart(fig3, use_container_width=True)
# else:
#     fig3 = px.box(new_df[(new_df["sector"] == sector_selected) & (new_df["bedRoom"] <= 4)], x="bedRoom", y="price")
#     st.plotly_chart(fig3, use_container_width=True)
    
    
    
# # STREAMLIT LAYOUT
# st.header("Distribution of flat prices vs house prices")

# property_selected = st.selectbox("Select poperty", ["flat", "house"])

# # DISTRIBUTION PLOT
# if property_selected == "flat":
#     fig4 = px.histogram(new_df[new_df["property_type"] == "flat"], x="price", color_discrete_sequence=['green'])
#     st.plotly_chart(fig4, use_container_width=True)
# else:
#     fig4 = px.histogram(new_df[new_df["property_type"] == "house"], x="price")
#     st.plotly_chart(fig4, use_container_width=True)