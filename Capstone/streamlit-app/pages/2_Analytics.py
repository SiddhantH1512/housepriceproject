import streamlit as st 
import pandas as pd 
import plotly.express as px
import matplotlib.pyplot as plt 
from wordcloud import WordCloud
import pickle
import ast
import numpy as np 



st.title("Page 2")

# STREAMLIT LAYOUT
st.header("Sector wise price per sqft map")

# PREPARING DATA FOR GEOMAP
new_df = pd.read_csv("/Users/siddhant/housepriceproject/Capstone/datasets/data_viz1.csv")
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
    features = wordclouddata[wordclouddata['sector'] == sector]['features']
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
selected_sector = st.selectbox("Select a sector", wordclouddata['sector'].unique())
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