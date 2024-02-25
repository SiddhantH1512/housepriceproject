import sys
sys.path.append('/Users/siddhant/housepriceproject')
import pandas as pd 
import numpy as np 
from Capstone.logger import logging
from Capstone.exception import CustomException
from dataclasses import dataclass
from sklearn.impute import KNNImputer
import warnings
import os
import re

warnings.filterwarnings("ignore")

class MissingValueImpute:
    def __init__(self, dataframe):
        self.df = dataframe
        self.drop_duplicates()
        self.calculate_ratios_and_missing_df()
        
    def drop_duplicates(self):
        logging.info("Dropping duplicates")
        self.df.drop_duplicates(inplace=True)
        logging.info("Dropped duplicates")
        
    
    @staticmethod
    def area_ratios(df, column_name_1, column_name_2):
        no_null_areas = df[~(df[column_name_1].isnull()) & ~(df[column_name_2].isnull())]
        ratio = (no_null_areas[column_name_1] / no_null_areas[column_name_2]).median()
        return ratio
    
    def getting_ratios(self):
        logging.info("Calculating area ratios")
        super_to_built_up_area_ratio = MissingValueImpute.area_ratios(self.df, "super_built_up_area", "built_up_area")
        carpet_to_built_up_area_ratio = MissingValueImpute.area_ratios(self.df, "carpet_area", "built_up_area")
        logging.info("Ratios calculated")
        return super_to_built_up_area_ratio, carpet_to_built_up_area_ratio
    
    
    def impute_builtup_area(self):
        logging.info("Creating a df where only the Builtup area column is all nulls")
        missing_built_up = self.df[~(self.df["super_built_up_area"].isnull()) & (self.df["built_up_area"].isnull() & ~(self.df["carpet_area"].isnull()))]
        logging.info("Dataframe created")
        
        return missing_built_up
    
    def calculate_ratios_and_missing_df(self):
        self.super_to_built_up_area_ratio, self.carpet_to_built_up_area_ratio = self.getting_ratios()
        self.missing_built_up = self.impute_builtup_area()
        
    def impute_builtup_missing(self, missing_built_up, super_to_built_up_area_ratio, carpet_to_built_up_area_ratio):
        logging.info("Imputing missing built-up areas")
        missing_built_up["built_up_area"].fillna(
            round(((missing_built_up["super_built_up_area"] / super_to_built_up_area_ratio) +
                   (missing_built_up["carpet_area"] / carpet_to_built_up_area_ratio)) / 2), inplace=True)
        logging.info("Imputation complete")
        
        logging.info("Updating main dataframe")
        self.df.update(missing_built_up)
        logging.info("Dataframe updated")
    
    def impute_builtup_area_with_carpet_area(self, carpet_to_built_up_area_ratio):
        logging.info("Creating a df where only the Carpet area is not null and other two areas are all nulls")
        present_carpet = self.df[(self.df["super_built_up_area"].isnull()) & (self.df["built_up_area"].isnull() & ~(self.df["carpet_area"].isnull()))]
        logging.info("Dataframe created")
        
        logging.info("Imputing missing built-up areas")
        present_carpet["built_up_area"].fillna(round(present_carpet["carpet_area"]/carpet_to_built_up_area_ratio), inplace=True)
        logging.info("Imputation complete")
        
        logging.info("Updating main dataframe")
        self.df.update(present_carpet)
        logging.info("Dataframe updated")
    
    def impute_builtup_area_with_super_builtup_area(self, super_to_built_up_area_ratio):
        logging.info("Creating a df where only the super builtup area is not null and other two areas are all nulls")
        present_super_builtup = self.df[~(self.df["super_built_up_area"].isnull()) & (self.df["built_up_area"].isnull() & (self.df["carpet_area"].isnull()))]
        logging.info("Dataframe created")
        
        logging.info("Imputing missing built-up areas")
        present_super_builtup["built_up_area"].fillna(round(present_super_builtup["super_built_up_area"]/super_to_built_up_area_ratio), inplace=True)
        logging.info("Imputation complete")
        
        logging.info("Updating main dataframe")
        self.df.update(present_super_builtup)
        logging.info("Dataframe updated")

    
    @staticmethod
    def extract_plot(row): 
        pattern = r'Plot area \d+ \(([\d.]+) sq\.m\.\)'
        # r'Plot area \d+\(([\d.]+) sq\.m\.\)'
        match = re.match(pattern, row, re.IGNORECASE)
        
        if match:
            return match.group(1)
        else:
            return None
       
    def plot_area_extract(self):
        logging.info("Extracting plot area")
        self.df["plot_area"] = self.df["areaWithType"].apply(MissingValueImpute.extract_plot) 
        logging.info("Extraction complete")
        
    def impute_builtup_area_with_plot_area(self):
        logging.info("Creating a df where plot area is not null and builtup area is null")
        null_builtup = self.df[(self.df["built_up_area"].isnull()) & ~(self.df["plot_area"].isnull())]
        logging.info("Df created")
        
        logging.info("Converting values in Sqft")
        null_builtup["plot_area_sqft"] = [float(row) * 10.7639 for row in null_builtup["plot_area"]]
        logging.info("Conversion successful")
        
        logging.info("Imputing null values in builtup area with plot area values")
        null_builtup["built_up_area"].fillna(round(null_builtup["plot_area_sqft"]), inplace=True)
        logging.info("Imputation complete")
        
        logging.info("Updating main dataframe")
        self.df.update(null_builtup)
        logging.info("Dataframe updated")
        
        logging.info("There are just 5 remaining null values in the main df in builtup area")
        self.df = self.df[~(self.df["built_up_area"].isnull())]
        logging.info("Remaining 5 null values discarded")
        
    def impute_super_builtup_and_carpet_area(self, super_to_built_up_area_ratio, carpet_to_built_up_area_ratio):
        logging.info("Creating a df where super builtup area is null and imputing the nulls")
        null_super = self.df[(self.df["super_built_up_area"].isnull()) & ~(self.df["built_up_area"].isnull())]
        null_super["super_built_up_area"].fillna((super_to_built_up_area_ratio * null_super["built_up_area"]), inplace=True)
        null_super["super_built_up_area"] = null_super["super_built_up_area"].apply(lambda x: round(x, 2))
        logging.info("Imputation complete")
        
        logging.info("Updating main dataframe")
        self.df.update(null_super)
        logging.info("Dataframe updated")
        
        logging.info("Creating a df where carpet area is null and imputing the nulls")
        null_carpet = self.df[(self.df["carpet_area"].isnull()) & ~(self.df["built_up_area"].isnull())]
        null_carpet["carpet_area"].fillna((carpet_to_built_up_area_ratio * null_carpet["built_up_area"]), inplace=True)
        null_carpet["carpet_area"] = null_carpet["carpet_area"].apply(lambda x: round(x, 2))
        logging.info("Imputation complete")
        
        logging.info("Updating main dataframe")
        self.df.update(null_carpet)
        logging.info("Dataframe updated")
        
        logging.info("Filtering dataframe where only properties with builtup area less than 20000 are present")
        self.df = self.df[self.df["built_up_area"] < 20000]
        logging.info("Filtering complete")
        
        logging.info("Filtering dataframe where builtup area less than 2000 are price is more than 2.5 crores")
        error_df = self.df[(self.df["built_up_area"] < 2000) & (self.df["price"] > 2.5)][["price", "area", "built_up_area"]]
        error_df["built_up_area"] = error_df["area"]
        logging.info("Filtering complete")
        
        logging.info("Updating main dataframe")
        self.df.update(error_df)
        logging.info("Dataframe updated")
    
    def impute_floor_num(self):
        logging.info("Creating a df where the floor numbers are null for houses")
        null_house = self.df[(self.df['property_type'] == 'house') & (self.df["floorNum"].isnull())]
        logging.info("Df created")
        
        logging.info("Imputing nulls with median")
        null_house["floorNum"].fillna(2, inplace=True)
        logging.info("Imputation complete")
        
        logging.info("Updating main dataframe")
        self.df.update(null_house)
        logging.info("Dataframe updated")
        
        logging.info("Creating a df where the floor numbers are null for flats")
        flat_null = self.df[self.df['property_type'] == 'flat']
        flat_null.drop(columns=["facing", "plot_area"], inplace=True)
        logging.info("Df created")
        
        logging.info("Imputing the null values with KNN Imputer")
        imputer = KNNImputer(n_neighbors=5)
        columns_to_impute = ["price", "area", "bedRoom", "floorNum"]
        imputed_data = imputer.fit_transform(flat_null[columns_to_impute])
        imputed_df = pd.DataFrame(imputed_data, columns=columns_to_impute, index=flat_null.index)
        imputed_df.drop(columns=["price", "area", "bedRoom"], inplace=True)
        logging.info("Imputation complete")
        
        logging.info("Updating main dataframe")
        self.df.update(imputed_df)
        self.df.drop(columns=['area','areaWithType', 'facing','super_built_up_area','carpet_area','area_room_ratio', 'plot_area'],inplace=True)
        logging.info("Dataframe updated")
        
    def impute_society(self):
        logging.info("Only one Nan so dropping it")
        self.df = self.df[~(self.df["society"].isnull())]
        logging.info("Dropped")
        
    def impute_age_possession(self):
        logging.info("Using mode to impute missing values")
        mode_value = self.df['agePossession'].str.lower().replace('undefined', np.nan).mode()[0]
        self.df['agePossession'] = self.df['agePossession'].str.lower().replace('undefined', mode_value)
        logging.info("Imputation complete")
    
    def few_cleanups(self):
        logging.info("Deleting unnecessary columns")
        self.df.drop(columns=["society", "price_per_sqft"], inplace=True)
        logging.info("Columns deleted")
    
    @staticmethod
    def luxury(row):
        if 0 <= row < 50:
            return "Low"
        elif 50 <= row < 120:
            return "Medium"
        elif 120 <= row:
            return "High"
        else:
            return None
        
    @staticmethod
    def floor(row):
        if 0 <= row <= 2:
            return "Low Floor"
        elif 3 <= row <= 10:
            return "Mid Floor"
        elif 11 <= row <= 51:
            return "High Floor"
        else:
            return None
        
    def creating_categorical_columns(self):
        logging.info("Creating luxury level column")
        self.df["luxury_level"] =  self.df["luxury_score"].apply(MissingValueImpute.luxury)
        logging.info("Creation complete")
    
        logging.info("Creating floor category column")
        self.df["floor_category"] = self.df["floorNum"].apply(MissingValueImpute.floor)
        logging.info("Creation complete")
        
        self.df["Cluster_Labels"] = self.df["Cluster_Labels"].replace({0:3})
        self.df.rename(columns={"Cluster_Labels":"furniture_type"}, inplace=True)
        self.df["furniture_type"].replace({3: 1, 1: 3, 2: 2}, inplace=True)
        
        logging.info("Deleting unnecessary columns")
        self.df.drop(columns=["floorNum", "luxury_score"], inplace=True)
        # self.df.drop(columns=["others"], inplace=True)
        logging.info("Columns deleted")
        
    def combined_run6(self):
        self.impute_builtup_missing(self.missing_built_up, self.super_to_built_up_area_ratio, self.carpet_to_built_up_area_ratio)
        self.impute_builtup_area_with_carpet_area(self.carpet_to_built_up_area_ratio)
        self.impute_builtup_area_with_super_builtup_area(self.super_to_built_up_area_ratio)
        self.plot_area_extract()
        self.impute_builtup_area_with_plot_area()
        self.impute_super_builtup_and_carpet_area(self.super_to_built_up_area_ratio, self.carpet_to_built_up_area_ratio)
        self.impute_floor_num()
        self.impute_society()
        self.impute_age_possession()
        self.few_cleanups()
        self.creating_categorical_columns()
    
        return self.df
    
if __name__ == "__main__":
    try:
        datapath = "/Users/siddhant/housepriceproject/Capstone/data/ready/outliers_treated.csv"
        output_path = "/Users/siddhant/housepriceproject/Capstone/data/ready"
        destination_path = os.path.join(output_path, "missing_imputed.csv")
        
        df = pd.read_csv(datapath)
        outlier = MissingValueImpute(df)
        finaldf = outlier.combined_run6()
        finaldf.to_csv(destination_path, index=False)
    except Exception as e:
        logging.info(f"Following error occurred: {e}")
        raise CustomException(e, sys)
        

        
        
        
       