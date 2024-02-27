import streamlit as st 
import pandas as pd 
import plotly.express as px
import matplotlib.pyplot as plt 
import pickle
import ast
import numpy as np 
import boto3
import sys
sys.path.append("/Users/siddhant/housepriceproject")

from botocore.exceptions import NoCredentialsError


model_path1 = '/app/models/cosinse_sim.pkl'
model_path2 = '/app/models/cosinse_sim2.pkl'
model_path3 = '/app/models/cosinse_sim3.pkl'
wordcloud = '/app/models/wordcloud_data.pkl'
df_path = '/app/models/locationdf.pkl'

s3_path1 = 'models/cosinse_sim.pkl'
s3_path2 = 'models/cosinse_sim2.pkl'
s3_path3 = 'models/cosinse_sim3.pkl'
s3_path_df_4 = 'files/locationdf.pkl'
s3_path_wordcloud_5 = 'files/wordcloud_data.pkl'



bucket_name = "capstone-houseprice-prediction"

def s3_download(s3_bucket, s3_file_path, local_file):
    s3 = boto3.client("s3")
    s3.download_file(s3_bucket, s3_file_path, local_file)


# Upload each file
s3_download(bucket_name, s3_path1, model_path1)
s3_download(bucket_name, s3_path2, model_path2)
s3_download(bucket_name, s3_path2, model_path3)
s3_download(bucket_name, s3_path_df_4, df_path)



with open(model_path1, 'rb') as file:
    cosine_sim1 = pickle.load(file)

with open(model_path2, 'rb') as file:
    cosine_sim2 = pickle.load(file)
    
with open(model_path3, 'rb') as file:
    cosine_sim3 = pickle.load(file)
    
with open(df_path, 'rb') as file:
    locationdf = pickle.load(file)
    

# DROP DOWN FOR LOCATIONS
st.title("Select a location and radius 📍")
location = st.selectbox("Locations", sorted(locationdf.columns.tolist()))
radius = st.number_input("Radius (kms)")

if st.button("Search"):
    result = locationdf[locationdf[location] < radius*1000][location].sort_values()

    if result.empty:  # Check if the Series is empty
        st.write(f"No properties found within {radius} kms.")
    else:
        for title, dist in result.items():
            # df = pd.DataFrame({"Apartments":title, "Distance (kms)":round(dist/1000, 2)})
            # st.dataframe(df)
            st.text(f"{title}: {round(dist/1000, 2)} kms")
            
            
            
# RECOMMENDATION SYSTEM FOR DROP DOWN APARTMENTS
def recommend_properties_with_scores2(property_name, top_n=5):
    cosine_sim_matrix = 2*cosine_sim1 + 4*cosine_sim2 + 1*cosine_sim3

    property_idx = locationdf.index.get_loc(property_name)
    scores = list(enumerate(cosine_sim_matrix[property_idx]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
    top_properties = locationdf.index[top_indices].tolist()

    new_recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

    return new_recommendations_df

# DROP DOWN FOR APARTMENTS
st.title("Select an apartment 🏠")
apartment = st.selectbox("Apartments", sorted(locationdf.index.tolist()))

if st.button("Recommend"):
    recommendation_df = recommend_properties_with_scores2(apartment)
    st.dataframe(recommendation_df, hide_index=True)
    









# import streamlit as st
# import pandas as pd
# import numpy as np
# import pickle

# # Initialize session states
# if 'apartments' not in st.session_state:
#     st.session_state['apartments'] = []
# if 'selected_apartment' not in st.session_state:
#     st.session_state['selected_apartment'] = None

# st.set_page_config(page_title="Recommend Apartments", layout="wide", page_icon="🏠")

# dataframe = pickle.load(open("/Users/siddhant/housepriceproject/Capstone/datasets/locationdf.pkl", "rb"))

# # DROP DOWN FOR LOCATIONS
# st.title("Select a location and radius")
# location = st.selectbox("Locations", sorted(dataframe.columns.tolist()))
# radius = st.number_input("Radius (kms)")

# if st.button("Search"):
#     st.session_state.apartments = []
#     result = dataframe[dataframe[location] < radius*1000][location].sort_values()

#     if result.empty:  # Check if the Series is empty
#         st.write(f"No properties found within {radius} kms.")
#     else:
#         for title, dist in result.items():
#             st.session_state.apartments.append(f"{title}: {round(dist/1000, 2)} kms")

# if st.session_state.apartments:
#     st.session_state.selected_apartment = st.radio(
#         "Make your selection",
#         st.session_state.apartments
#     )

#     st.write(f"You selected: {st.session_state.selected_apartment}")
