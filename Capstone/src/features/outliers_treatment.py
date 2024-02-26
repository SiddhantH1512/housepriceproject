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

class TreatOutliers:
    def __init__(self, dataframe):
        self.df = dataframe
        
    def drop_duplicates(self):
        logging.info("Dropping duplicates")
        self.df.drop_duplicates(inplace=True)
        logging.info("Dropped duplicates")
        
    @staticmethod
    def calculate_iqr_stats(df, column_name):
        Q1 = df[column_name].quantile(0.25)
        Q3 = df[column_name].quantile(0.75)

        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outlier_df = df[(df[column_name] > upper_bound) | (df[column_name] < lower_bound)]

        return outlier_df
        
    def price_per_sqft_outlier_treatment(self):
        logging.info("Creating a price_per_sqft outlier dataframe from the current dataframe")
        outlier_persqft = TreatOutliers.calculate_iqr_stats(self.df, 'price_per_sqft')
        logging.info("Dataframe created")
        
        logging.info("Converting some values from in column froom yards to sqft")
        outlier_persqft["area"] = outlier_persqft["area"].apply(lambda x: x*9 if x < 1000 else x)
        logging.info("Conversion complete")
        
        logging.info("Calculating price per sqft")
        outlier_persqft["price_per_sqft"] = round((outlier_persqft['price']*10000000)/outlier_persqft['area'])
        logging.info("Calculation done")
        
        logging.info("Updating the original Dataframe")
        self.df.update(outlier_persqft)
        logging.info("Dataframe updated")
        
        logging.info("Capping the outliers in the main dataframe to 50000")
        self.df =  self.df[self.df["price_per_sqft"] <= 50000]
        logging.info("Successfully capped the outliers")
        
        
    def area_outlier_treatment(self):
        logging.info("Filtering the dataframe to have area less than 100000")
        self.df = self.df[self.df["area"] < 100000]
        logging.info("Filtered the dataframe")
        
        logging.info("Deleting rows where area is a data discrepency")
        values_to_drop = [98977.95, 65517.24, 65517.24, 58227.85, 55000.00, 49122.81, 45283.02, 34426.23]
        self.df = self.df[~self.df["area"].isin(values_to_drop)]
        logging.info("Deleted the rows")
        
        logging.info("Replacing unrealistic area values")
        self.df["area"] = self.df["area"].replace({82781.46: 115*9, 
                                                   65261.04: 7250, 
                                                   46794.87: 5800, 
                                                   22498.20: 2660,
                                                   20250.37: 2850,
                                                   18129.08: 1812,
                                                   15478.84: 2160,
                                                   12644.51: 1175,
                                                   10799.14: 3500})
        logging.info("Replaced")
        
    
    def bedroom_outliers(self):
        logging.info("Filtering dataframe with bedrooms less than 10")
        self.df = self.df[self.df["bedRoom"] <= 10]
        logging.info("Filtered dataframe")
        
        
    def carpet_area_outliers(self):
        logging.info("Inserting appropriate area value")
        self.df["carpet_area"] = self.df["carpet_area"].replace({18122.0: 1812})
        logging.info("Value inserted")
        
        
    def reclean_price_per_sqft(self):
        logging.info("Recleaning the outliers in the columns due to changes made in the area column")
        self.df["price_per_sqft"] = round((self.df['price']*10000000)/self.df['area'])
        logging.info("Cleaning done")
        
        logging.info("Creating area to room ratio column")
        self.df["area_room_ratio"] = self.df["area"] / self.df["bedRoom"]
        logging.info("area_room_ratio Column created")
        
        logging.info("Removing data points where the area to room ratio is less than 100")
        self.df =  self.df[ self.df["area_room_ratio"] > 100]
        logging.info("Filtered the dataframe")
        
        logging.info("Creating an outlier dataframe where the area to room ratio is less than 250 and number of rooms are more than 3")
        outlier_df1 = self.df[(self.df["area_room_ratio"] < 250) & (self.df["bedRoom"] > 3)]
        logging.info("Outlier dataframe created")
        
        logging.info("Updating original dataframe")
        self.df.update(outlier_df1)
        logging.info("Daraframe updated")
        
        logging.info("Filtering dataframe where the area to room ratio is less than 250 and number of rooms are more than 4")
        self.df = self.df[~((self.df["area_room_ratio"] < 250) & (self.df["bedRoom"] > 4))]
        logging.info("Dataframe filtered")
        
    
    def combined_run5(self):
        self.drop_duplicates()
        self.price_per_sqft_outlier_treatment()
        self.area_outlier_treatment()
        self.bedroom_outliers()
        self.carpet_area_outliers()
        self.reclean_price_per_sqft()
        
        return self.df
    
    def run_preprocessing(input_path, output_path):
        df = pd.read_csv(input_path)    
        preprocessor = TreatOutliers(df)
        processed_df = preprocessor.combined_run5()
        processed_df.to_csv(output_path, index=False)
    
if __name__ == "__main__":
    try:
        datapath = "/Users/siddhant/housepriceproject/Capstone/pipeline_generated_data/feature_engineered.csv"
        output_path = "/Users/siddhant/housepriceproject/Capstone/pipeline_generated_data"
        destination_path = os.path.join(output_path, "outliers_treated.csv")
        
        df = pd.read_csv(datapath)
        outlier = TreatOutliers(df)
        finaldf = outlier.combined_run5()
        finaldf.to_csv(destination_path, index=False)
    except Exception as e:
        logging.info(f"Following error occurred: {e}")
        raise CustomException(e, sys)
        

    
        
        
        
        
        
        
        
        
        
        
        
        
        
    
   
   


   
