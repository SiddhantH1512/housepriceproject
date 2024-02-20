import streamlit as st 
import pandas as pd 
import numpy as np 
import pickle




st.title("Page 1")

with open("/Users/siddhant/housepriceproject/Capstone/df.pkl", 'rb') as file:
    df = pickle.load(file) 
    
with open("/Users/siddhant/housepriceproject/Capstone/pipeline.pkl", 'rb') as file:
    pipeline = pickle.load(file)

st.dataframe(df)

st.header("Enter your input")

# TYPE OF PROPERTY
property_type =  st.selectbox('Property Type', df["property_type"].unique().tolist())

# SECTOR 
sector = st.selectbox('Sector', sorted(df["sector"].unique().tolist()))

# BEDROOM 
bedroom = int(st.selectbox('Number of Bedrooms', sorted(df["bedRoom"].unique().tolist())))

# BATHROOM 
bathroom = int(st.selectbox('Number of Bathroom', sorted(df["bathroom"].unique().tolist())))

# BALCONY 
balcony = st.selectbox('Number of Balconies', sorted(df["balcony"].unique().tolist()))

# AGE POSSESSION 
age = st.selectbox('Property Age', sorted(df["agePossession"].unique().tolist()))

# BUILTUP AREA 
area = float(st.number_input('Builtup Area'))

# SERVANT ROOM 
servant_room = int(st.selectbox('Servant room', sorted(df["servant room"].unique().tolist())))

# STORE ROOM 
store_room = int(st.selectbox('Store room', sorted(df['store room'].unique().tolist())))

# FURNISHING TYPE 
furniture_type = int(st.selectbox('Furnishing type', sorted(df['furniture_type'].unique().tolist())))

# LUXURY CATEGORY
luxury_level = st.selectbox('Luxury level', sorted(df['luxury_level'].unique().tolist()))

# FLOOR CATEGORY
floor_category = st.selectbox('Desired Floor', sorted(df['floor_category'].unique().tolist()))

# CREATE A BUTTON FOR PREDICT
if st.button('Get Quotation'):
# 1. Form a dataframe from the input that user has given
    data = [[property_type, sector, bedroom, bathroom, balcony, age, area, servant_room, store_room, furniture_type,
    luxury_level, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
    'agePossession', 'built_up_area', 'servant room', 'store room',
    'furniture_type', 'luxury_level', 'floor_category']
    
    dataframe = pd.DataFrame(data, columns=columns)
# 2. Predict using this dataframe
    base_price = np.expm1(pipeline.predict(dataframe))[0]
    low = base_price - 0.22
    high = base_price + 0.22
# 3. Display
    st.text(f"The price of the flat is between {round(low, 2)} - {round(high, 2)} crores")



