import sys
sys.path.append('/Users/siddhant/housepriceproject')
import pandas as pd 
import numpy as np 
from Capstone.logger import logging
from Capstone.exception import CustomException
from dataclasses import dataclass
import warnings
import os
import re

warnings.filterwarnings("ignore")

class DataPreprocessing2:
    def __init__(self, dataframe):
        self.df1 = dataframe
        logging.info("Load dataframe")
        
    def check_duplicates(self):
        self.df1.drop_duplicates(inplace=True)
        logging.info("Check for duplicates to remove them")
  
    def unwanted_columns_drop(self):
        self.df1.drop(columns=["link", "description", "property_id"], axis=1, inplace=True)
        logging.info("Removed unwanted columns")
        
    def clean_price(self):
        self.df1 = self.df1[self.df1["price"] != "Price on Request"]
        def price(value):
            if type(value) == float:
                return value
            else:
                if value[1] == "Lac":
                    return round(float(value[0])/100, 2)
                else:
                    return round(float(value[0]),2)
        self.df1.loc[:, "price"] = self.df1["price"].str.split(" ").apply(price)
        logging.info("Removed the 'Price on Request' column and converted the prices into crores")
        
    def clean_society(self):
        def regex(value):
            cleaned_value = re.sub(r'\d+(\.\d+)?\s?★', "", str(value))
            cleaned_value = cleaned_value.lower().strip()
            return cleaned_value
        self.df1.loc[:, "society"] = self.df1["society"].apply(regex)
        self.df1["society"] = self.df1["society"].replace('nan', "independent")
        logging.info("Cleaned the society column and replaced nan values")
    
    def rename_clean_col(self):
        self.df1.rename(columns={"rate":"price_per_sqft"}, inplace=True)
        logging.info("Renaming rate column")
    
    def clean_price_per_sqft(self):
        self.df1["price_per_sqft"] = self.df1["price_per_sqft"].str.split("/").str.get(0).str.replace("₹", "").str.replace(",","").str.strip().astype(float)
        logging.info("Cleaned price_per_sqft")
    
    def create_feature(self):
        self.df1["area"] =  round((self.df1["price"] * 10000000)/self.df1["price_per_sqft"],2)
        self.df1.insert(loc=2, column="property_type", value="house")
        logging.info("Created a new feature 'area' from price and price_per_sqft and added a column called property_type which is flat")
    
    def bedroom_null(self):
        self.df1 = self.df1[~self.df1['bedRoom'].isnull()]
        logging.info("Filtered out rows with null values in the 'bedRoom' column")

    def clean_other_columns(self):
        self.df1["bedRoom"] = self.df1["bedRoom"].str.split(" ").str.get(0).str.strip().astype(int)
        self.df1["bathroom"] = self.df1["bathroom"].str.split(" ").str.get(0).str.strip().astype(int)
        self.df1["balcony"] = self.df1["balcony"].str.split(" ").str.get(0).str.replace("No", "0")
        self.df1["additionalRoom"].fillna("not available", inplace=True)
        self.df1["additionalRoom"] = self.df1["additionalRoom"].str.lower()
        self.df1["noOfFloor"] = self.df1["noOfFloor"].str.split(" ").str.get(0)
        self.df1.rename(columns={'noOfFloor':'floorNum'},inplace=True)
        self.df1["facing"].fillna("NA", inplace=True) 
        logging.info("Cleaned the remaining columns")
    
    def combined_run(self):
        self.check_duplicates()
        self.unwanted_columns_drop()
        self.clean_price()
        self.clean_society()
        self.rename_clean_col()
        self.clean_price_per_sqft()
        self.create_feature()
        self.bedroom_null()
        self.clean_other_columns()
        
        return self.df1
    logging.info("Final run")
    
if __name__ == "__main__":
    try:
        data_path = "/Users/siddhant/housepriceproject/Capstone/data/raw/house.csv"
        destination_path = "/Users/siddhant/housepriceproject/Capstone/data/ready"
        output_path = os.path.join(destination_path, "house_processed.csv")
        df1 = pd.read_csv(data_path)
        preprocessor2 = DataPreprocessing2(df1)
        preprocessed2_df = preprocessor2.combined_run()
        preprocessed2_df.to_csv(output_path, index=False)
    except Exception as e:
        logging.info("Error occured:")
        raise CustomException(e, sys)