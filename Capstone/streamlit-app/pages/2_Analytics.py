import streamlit as st 
import pandas as pd 
import plotly.express as px
import matplotlib.pyplot as plt 
from wordcloud import WordCloud
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
image_path = '/app/files/image.pkl'

s3_path1 = 'models/cosinse_sim.pkl'
s3_path2 = 'models/cosinse_sim2.pkl'
s3_path3 = 'models/cosinse_sim3.pkl'
s3_path_df_4 = 'files/locationdf.pkl'
s3_path_wordcloud_5 = 'files/wordcloud_data.pkl'
s3_image = 'files/image.pkl'



bucket_name = "capstone-houseprice-prediction"

def s3_download(s3_bucket, s3_file_path, local_file):
    s3 = boto3.client("s3")
    s3.download_file(s3_bucket, s3_file_path, local_file)

# Upload each file
s3_download(bucket_name, s3_path1, model_path1)
s3_download(bucket_name, s3_path2, model_path2)
s3_download(bucket_name, s3_path3, model_path3)
s3_download(bucket_name, s3_path_df_4, df_path)
s3_download(bucket_name, s3_path_wordcloud_5, wordcloud)
s3_download(bucket_name, s3_image, image_path)

with open(model_path1, 'rb') as file:
    cosine_sim1 = pickle.load(file)

with open(model_path2, 'rb') as file:
    cosine_sim2 = pickle.load(file)
    
with open(model_path3, 'rb') as file:
    cosine_sim3 = pickle.load(file)
    
with open(df_path, 'rb') as file:
    locationdf = pickle.load(file)
    
with open(wordcloud, 'rb') as file:
    wordcloud_data = pickle.load(file)
    

st.title("Page 2")

# STREAMLIT LAYOUT
st.header("Sector wise price per sqft map")

# PREPARING DATA FOR GEOMAP
new_df = pd.read_csv("/app/src/data_viz1.csv")
groupdf = new_df.groupby("sector")[['price','price_per_sqft','built_up_area','latitude','longitude']].mean()

# GEOMAP
fig = px.scatter_mapbox(groupdf, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                mapbox_style="open-street-map", width=1200, height=700, hover_name=groupdf.index)
st.plotly_chart(fig, use_container_width=True)





# STREAMLIT LAYOUT
st.header("Sector-specific Wordcloud")
# LOADING THE DATAFRAME
wordclouddata = pickle.load(open("Capstone/datasets/wordcloud_data.pkl", "rb"))
# FUNCTION TO PLOT SECTOR WISE WORDCLOUD
def generate_wordcloud(sector):
    # Extracting features for the selected sector
    features = wordcloud_data[wordcloud_data['sector'] == sector]['features']
    main = []
    for feature_list in features.dropna():
        main.extend(ast.literal_eval(feature_list))
    text = ' '.join(main)

    # Generate wordcloud
    wordcloud = WordCloud(width=800, height=800,
                        background_color='white',
                        stopwords=set(['s']),  # Add any stopwords here
                        min_font_size=10).generate(text)

    # Display wordcloud using matplotlib
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot()

# Dropdown for sector selection
selected_sector = st.selectbox("Select a sector", wordcloud_data['sector'].unique())
# Display the wordcloud for the selected sector
if selected_sector:
    generate_wordcloud(selected_sector)

st.set_option('deprecation.showPyplotGlobalUse', False)



# STREAMLIT LAYOUT
st.header("Area vs Price")

property_type = st.selectbox("Select poperty type", ["flat", "house"])

# PLOTTING SCATTER PLOT AREA VS PRICE
if property_type == "flat":
    fig1 = px.scatter(new_df[new_df["property_type"] == "flat"], x="built_up_area", y="price", color="bedRoom")
    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.scatter(new_df[new_df["property_type"] == "house"], x="built_up_area", y="price", color="bedRoom")
    st.plotly_chart(fig1, use_container_width=True)



# STREAMLIT LAYOUT
st.header("BHK Pie Chart")

sector_list = new_df["sector"].unique().tolist()
sector_list.insert(0, "overall")

selected_sector = st.selectbox("Select sector", sector_list)
# PLOTTING PIE CHART FOR BEDROOMS SECTORWISE
if selected_sector == "overall":
    fig2 = px.pie(new_df, names="bedRoom")
    st.plotly_chart(fig2, use_container_width=True)
else:
    fig2 = px.pie(new_df[new_df["sector"] == selected_sector], names="bedRoom")
    st.plotly_chart(fig2, use_container_width=True)
    
    

# STREAMLIT LAYOUT
st.header("BHK price range")

allsectors = new_df["sector"].unique().tolist()
allsectors.insert(0, "overall")

sector_selected = st.selectbox("Select required sector", allsectors)
# BOXPLOT FOR BHK WIS PRICE
if sector_selected == "overall":
    fig3 = px.box(new_df[new_df["bedRoom"] <= 4], x="bedRoom", y="price")
    st.plotly_chart(fig3, use_container_width=True)
else:
    fig3 = px.box(new_df[(new_df["sector"] == sector_selected) & (new_df["bedRoom"] <= 4)], x="bedRoom", y="price")
    st.plotly_chart(fig3, use_container_width=True)
    
    
    
# STREAMLIT LAYOUT
st.header("Distribution of flat prices vs house prices")

property_selected = st.selectbox("Select poperty", ["flat", "house"])

# DISTRIBUTION PLOT
if property_selected == "flat":
    fig4 = px.histogram(new_df[new_df["property_type"] == "flat"], x="price", color_discrete_sequence=['green'])
    st.plotly_chart(fig4, use_container_width=True)
else:
    fig4 = px.histogram(new_df[new_df["property_type"] == "house"], x="price")
    st.plotly_chart(fig4, use_container_width=True)