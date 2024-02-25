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

class MergeFiles:
    def __init__(self, dataframe1, dataframe2):
        self.df1 = dataframe1
        self.df2 = dataframe2
        
    def merge(self):
        self.df = pd.concat([self.df1, self.df2], ignore_index=True)
        logging.info("Merged Flats and Houses dataframes")
        
    def remove_duplicate(self):
        self.df.drop_duplicates(keep="last", inplace=True)
        logging.info("Removed duplicates")
    
    def combined_run(self):
        self.merge()
        self.remove_duplicate()
        
        return self.df
    logging.info("Merged Dataframe")
    
if __name__ == "__main__":
    try:
        filepath1 = "/Users/siddhant/housepriceproject/Capstone/data/ready/flats_processed.csv"
        filepath2 = "/Users/siddhant/housepriceproject/Capstone/data/ready/house_processed.csv"
        destination_path = "/Users/siddhant/housepriceproject/Capstone/data/ready"
        filename = "merged_data.csv"
        
        df1 = pd.read_csv(filepath1)
        df2 = pd.read_csv(filepath2)
        
        merge = MergeFiles(df1, df2)
        merged_df = merge.combined_run()
        merged_df.to_csv(os.path.join(destination_path, filename), index=False)
    except Exception as e:
        logging.info("File error occured")
        raise CustomException(e, sys)
        