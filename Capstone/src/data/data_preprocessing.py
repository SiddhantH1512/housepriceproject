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

class DataPreprocessing:
    def __init__(self, dataframe):
        self.df = dataframe
        logging.info("Load dataframe")
        
    def check_duplicates(self):
        self.df.drop_duplicates(inplace=True)
        logging.info("Check for duplicates to remove them")
   
    def unwanted_columns_drop(self):
        self.df.drop(columns=["link", "description", "property_id"], inplace=True)
        logging.info("Removed unwanted columns")
        
    def clean_price(self):
        self.df = self.df[self.df["price"] != "Price on Request"]
        def price(value):
            if type(value) == float:
                return value
            else:
                if value[1] == "Lac":
                    return round(float(value[0])/100, 2)
                else:
                    return round(float(value[0]),2)
        self.df.loc[:, "price"] = self.df["price"].str.split(" ").apply(price)
        logging.info("Removed the 'Price on Request' column and converted the prices into crores")
        
    def clean_society(self):
        def regex(value):
            cleaned_value = re.sub(r'\d+(\.\d+)?\s?★', "", str(value))
            cleaned_value = cleaned_value.lower().strip()
            return cleaned_value
        self.df.loc[:, "society"] = self.df["society"].apply(regex)
        logging.info("Cleaned the socieety column")
    
    def rename_clean_col(self):
        self.df.rename(columns={"area":"price_per_sqft"}, inplace=True)
        logging.info("Renaming area column")
    
    def clean_price_per_sqft(self):
        self.df["price_per_sqft"] = self.df["price_per_sqft"].str.split("/").str.get(0).str.replace("₹", "").str.replace(",","").str.strip().astype(float)
        logging.info("Renamed and cleaned price_per_sqft")
    
    def create_feature(self):
        self.df.insert(loc=4, column="area", value=round((self.df["price"] * 10000000)/self.df["price_per_sqft"],2))
        self.df.insert(loc=2, column="property_type", value="flat")
        logging.info("Created a new feature 'area' from price and price_per_sqft and added a column called property_type which is flat")
    
    def clean_other_columns(self):
        self.df["bedRoom"] = self.df["bedRoom"].str.split(" ").str.get(0).str.strip().astype(int)
        self.df["bathroom"] = self.df["bathroom"].str.split(" ").str.get(0).str.strip().astype(int)
        self.df["balcony"] = self.df["balcony"].str.split(" ").str.get(0).str.strip()
        self.df["additionalRoom"].fillna("not available", inplace=True)
        self.df["additionalRoom"] = self.df["additionalRoom"].str.lower()
        self.df["floorNum"] = self.df["floorNum"].str.split(" ").str.get(0).replace("Ground", "0").str.replace("Basement", "-1").str.replace('Lower', "0").str.extract(r'(\d+)nd')
        self.df["facing"].fillna("NA", inplace=True)
        logging.info("Cleaned the remaining columns")
    
    def combined_run(self):
        try:
            self.check_duplicates()
            self.unwanted_columns_drop()
            self.clean_price()
            self.clean_society()
            self.rename_clean_col()
            self.clean_price_per_sqft()
            self.create_feature()
            self.clean_other_columns()
        except Exception as e:
            raise CustomException(e, sys)
        logging.info("Final run of the script")
        
        return self.df
   
   
def run_preprocessing(input_path, output_path):
    df = pd.read_csv(input_path)    
    preprocessor = DataPreprocessing(df)
    processed_df = preprocessor.combined_run()
    processed_df.to_csv(output_path, index=False)

if __name__ == "__main__":
    try:
        filepath = "/Users/siddhant/housepriceproject/Capstone/data/raw/flats.csv"
        output_path = "/Users/siddhant/housepriceproject/Capstone/pipeline_generated_data/flats_processed.csv"
        run_preprocessing(filepath, output_path)
    except Exception as e:
        logging.info("The following error occurred")
        raise CustomException(e, sys)
   
    

      