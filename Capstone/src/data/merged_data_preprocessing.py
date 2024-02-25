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

class MergedPreprocessing:
    def __init__(self, dataframe):
        self.df = dataframe
        
    def create_sector(self):
       self.df.insert(loc=3, column="sector", value=(self.df["property_name"].str.split("in").str.get(1).str.replace("Gurgaon", "").str.strip()))
       self.df["sector"] = self.df["sector"].str.lower()
       logging.info("Sector column created")
       
    def clean_sector(self):
        self.df['sector'] = self.df['sector'].str.replace('dharam colony','sector 12')
        self.df['sector'] = self.df['sector'].str.replace('krishna colony','sector 7')
        self.df['sector'] = self.df['sector'].str.replace('suncity','sector 54')
        self.df['sector'] = self.df['sector'].str.replace('prem nagar','sector 13')
        self.df['sector'] = self.df['sector'].str.replace('mg road','sector 28')
        self.df['sector'] = self.df['sector'].str.replace('gandhi nagar','sector 28')
        self.df['sector'] = self.df['sector'].str.replace('laxmi garden','sector 11')
        self.df['sector'] = self.df['sector'].str.replace('shakti nagar','sector 11')
        self.df['sector'] = self.df['sector'].str.replace('baldev nagar','sector 7')
        self.df['sector'] = self.df['sector'].str.replace('shivpuri','sector 7')
        self.df['sector'] = self.df['sector'].str.replace('garhi harsaru','sector 17')
        self.df['sector'] = self.df['sector'].str.replace('imt manesar','manesar')
        self.df['sector'] = self.df['sector'].str.replace('adarsh nagar','sector 12')
        self.df['sector'] = self.df['sector'].str.replace('shivaji nagar','sector 11')
        self.df['sector'] = self.df['sector'].str.replace('bhim nagar','sector 6')
        self.df['sector'] = self.df['sector'].str.replace('madanpuri','sector 7')
        self.df['sector'] = self.df['sector'].str.replace('saraswati vihar','sector 28')
        self.df['sector'] = self.df['sector'].str.replace('arjun nagar','sector 8')
        self.df['sector'] = self.df['sector'].str.replace('ravi nagar','sector 9')
        self.df['sector'] = self.df['sector'].str.replace('vishnu garden','sector 105')
        self.df['sector'] = self.df['sector'].str.replace('bhondsi','sector 11')
        self.df['sector'] = self.df['sector'].str.replace('surya vihar','sector 21')
        self.df['sector'] = self.df['sector'].str.replace('devilal colony','sector 9')
        self.df['sector'] = self.df['sector'].str.replace('valley view estate','gwal pahari')
        self.df['sector'] = self.df['sector'].str.replace('mehrauli  road','sector 14')
        self.df['sector'] = self.df['sector'].str.replace('jyoti park','sector 7')
        self.df['sector'] = self.df['sector'].str.replace('ansal plaza','sector 23')
        self.df['sector'] = self.df['sector'].str.replace('dayanand colony','sector 6')
        self.df['sector'] = self.df['sector'].str.replace('sushant lok phase 2','sector 55')
        self.df['sector'] = self.df['sector'].str.replace('chakkarpur','sector 28')
        self.df['sector'] = self.df['sector'].str.replace('greenwood city','sector 45')
        self.df['sector'] = self.df['sector'].str.replace('subhash nagar','sector 12')
        self.df['sector'] = self.df['sector'].str.replace('sohna road road','sohna road')
        self.df['sector'] = self.df['sector'].str.replace('malibu town','sector 47')
        self.df['sector'] = self.df['sector'].str.replace('surat nagar 1','sector 104')
        self.df['sector'] = self.df['sector'].str.replace('new colony','sector 7')
        self.df['sector'] = self.df['sector'].str.replace('mianwali colony','sector 12')
        self.df['sector'] = self.df['sector'].str.replace('jacobpura','sector 12')
        self.df['sector'] = self.df['sector'].str.replace('rajiv nagar','sector 13')
        self.df['sector'] = self.df['sector'].str.replace('ashok vihar','sector 3')
        self.df['sector'] = self.df['sector'].str.replace('dlf phase 1','sector 26')
        self.df['sector'] = self.df['sector'].str.replace('nirvana country','sector 50')
        self.df['sector'] = self.df['sector'].str.replace('palam vihar','sector 2')
        self.df['sector'] = self.df['sector'].str.replace('dlf phase 2','sector 25')
        self.df['sector'] = self.df['sector'].str.replace('sushant lok phase 1','sector 43')
        self.df['sector'] = self.df['sector'].str.replace('laxman vihar','sector 4')
        self.df['sector'] = self.df['sector'].str.replace('dlf phase 4','sector 28')
        self.df['sector'] = self.df['sector'].str.replace('dlf phase 3','sector 24')
        self.df['sector'] = self.df['sector'].str.replace('sushant lok phase 3','sector 57')
        self.df['sector'] = self.df['sector'].str.replace('dlf phase 5','sector 43')
        self.df['sector'] = self.df['sector'].str.replace('rajendra park','sector 105')
        self.df['sector'] = self.df['sector'].str.replace('uppals southend','sector 49')
        self.df['sector'] = self.df['sector'].str.replace('sohna','sohna road')
        self.df['sector'] = self.df['sector'].str.replace('ashok vihar phase 3 extension','sector 5')
        self.df['sector'] = self.df['sector'].str.replace('south city 1','sector 41')
        self.df['sector'] = self.df['sector'].str.replace('ashok vihar phase 2','sector 5')
        self.df['sector'] = self.df['sector'].str.replace('sector 95a','sector 95')
        self.df['sector'] = self.df['sector'].str.replace('sector 23a','sector 23')
        self.df['sector'] = self.df['sector'].str.replace('sector 12a','sector 12')
        self.df['sector'] = self.df['sector'].str.replace('sector 3a','sector 3')
        self.df['sector'] = self.df['sector'].str.replace('sector 110 a','sector 110')
        self.df['sector'] = self.df['sector'].str.replace('patel nagar','sector 15')
        self.df['sector'] = self.df['sector'].str.replace('a block sector 43','sector 43')
        self.df['sector'] = self.df['sector'].str.replace('maruti kunj','sector 12')
        self.df['sector'] = self.df['sector'].str.replace('b block sector 43','sector 43')
        self.df['sector'] = self.df['sector'].str.replace('sector-33 sohna road','sector 33')
        self.df['sector'] = self.df['sector'].str.replace('sector 1 manesar','manesar')
        self.df['sector'] = self.df['sector'].str.replace('sector 4 phase 2','sector 4')
        self.df['sector'] = self.df['sector'].str.replace('sector 1a manesar','manesar')
        self.df['sector'] = self.df['sector'].str.replace('c block sector 43','sector 43')
        self.df['sector'] = self.df['sector'].str.replace('sector 89 a','sector 89')
        self.df['sector'] = self.df['sector'].str.replace('sector 2 extension','sector 2')
        self.df['sector'] = self.df['sector'].str.replace('sector 36 sohna road','sector 36')
        logging.info("Sector column cleaned")
    
    def filter_sector(self):
        include_sector = self.df['sector'].value_counts()[self.df['sector'].value_counts() >= 3]
        self.df = self.df[self.df['sector'].isin(include_sector.index)]
        logging.info("Sector filtered")
    
    def renaming_sector(self):
        self.df.loc[364,'sector'] = 'sector 37'
        self.df.loc[3681,'sector'] = 'sector 92'
        self.df.loc[3683,'sector'] = 'sector 90'
        self.df.loc[3702,'sector'] = 'sector 76'
        self.df.loc[878,'sector'] = 'sector 110'
        self.df.loc[2819,'sector'] = 'sector 110'
        self.df.loc[2842,'sector'] = 'sector 110'
        self.df.loc[3816,'sector'] = 'sector 110'
        self.df.loc[3921,'sector'] = 'sector 110'
        logging.info("Sectors renamed")
        
    def drop_cols(self):
        self.df.drop(columns=["property_name", "address", "rating"], inplace=True)
        logging.info("Unwanted columns dropped")
    
    def combined_run3(self):
        self.create_sector()
        self.clean_sector()
        self.filter_sector()
        self.renaming_sector()
        self.drop_cols()
        
        return self.df
        logging("Final run")
    
if __name__ == "__main__":
    try:
        data_path = "/Users/siddhant/housepriceproject/Capstone/data/ready/merged_data.csv"
        destination_path = "/Users/siddhant/housepriceproject/Capstone/data/ready"
        output_path = os.path.join(destination_path, "merged_processed.csv")
        df = pd.read_csv(data_path)
        preprocessor3 = MergedPreprocessing(df)
        preprocessed3_df = preprocessor3.combined_run3()
        preprocessed3_df.to_csv(output_path, index=False)
    except Exception as e:
        logging.info("Error occured:")
        raise CustomException(e, sys)