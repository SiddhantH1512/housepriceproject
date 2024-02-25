import pandas as pd
import numpy as np 
import os 
from Capstone.logger import logging
from Capstone.exception import CustomException
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    flats_preprocessing_path = str=os.path.join("/Users/siddhant/housepriceproject/Capstone/data/ready", "flats_preprocessed.csv")
    houses_preprocessing_path = str=os.path.join("/Users/siddhant/housepriceproject/Capstone/data/ready", "houses_preprocessed.csv")
    merged_path = str=os.path.join("/Users/siddhant/housepriceproject/Capstone/data/ready", "merged.csv")
    merged_preprocessing_path = str=os.path.join("/Users/siddhant/housepriceproject/Capstone/data/ready", "merged_preprocessed.csv")
    feature_engineering_path = str=os.path.join("/Users/siddhant/housepriceproject/Capstone/data/ready", "merged_processed.csv")
    outliers_treatment_path = str=os.path.join("/Users/siddhant/housepriceproject/Capstone/data/ready", "outliers_preprocessed.csv")
    missing_value_impute_path = str=os.path.join("/Users/siddhant/housepriceproject/Capstone/data/ready", "missing_imputed.csv")
    feature_selection_path = str=os.path.join("/Users/siddhant/housepriceproject/Capstone/data/ready", "post_feature_sel.csv")
    model_pipeline_path = str=os.path.join("/Users/siddhant/housepriceproject/Capstone/data/ready", "pipeline.pkl")
    model_dataframe_path = str=os.path.join("/Users/siddhant/housepriceproject/Capstone/data/ready", "dataframe.pkl")
    recommendation_cossim1_path = str=os.path.join("/Users/siddhant/housepriceproject/Capstone/data/ready", "cosine_sim1.pkl")
    recommendation_cossim2_path = str=os.path.join("/Users/siddhant/housepriceproject/Capstone/data/ready", "cosine_sim2.pkl")
    recommendation_cossim3_path = str=os.path.join("/Users/siddhant/housepriceproject/Capstone/data/ready", "cosine_sim3.pkl")
    recommendation_df_path = str=os.path.join("/Users/siddhant/housepriceproject/Capstone/data/ready", "location_df.pkl")
    
    
class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.ingestion_config = config
    
    