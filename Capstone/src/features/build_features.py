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
import ast
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

warnings.filterwarnings("ignore")

class FeatureEngineering:
    weights = {
    '24/7 Power Backup': 8,
    '24/7 Water Supply': 4,
    '24x7 Security': 7,
    'ATM': 4,
    'Aerobics Centre': 6,
    'Airy Rooms': 8,
    'Amphitheatre': 7,
    'Badminton Court': 7,
    'Banquet Hall': 8,
    'Bar/Chill-Out Lounge': 9,
    'Barbecue': 7,
    'Basketball Court': 7,
    'Billiards': 7,
    'Bowling Alley': 8,
    'Business Lounge': 9,
    'CCTV Camera Security': 8,
    'Cafeteria': 6,
    'Car Parking': 6,
    'Card Room': 6,
    'Centrally Air Conditioned': 9,
    'Changing Area': 6,
    "Children's Play Area": 7,
    'Cigar Lounge': 9,
    'Clinic': 5,
    'Club House': 9,
    'Concierge Service': 9,
    'Conference room': 8,
    'Creche/Day care': 7,
    'Cricket Pitch': 7,
    'Doctor on Call': 6,
    'Earthquake Resistant': 5,
    'Entrance Lobby': 7,
    'False Ceiling Lighting': 6,
    'Feng Shui / Vaastu Compliant': 5,
    'Fire Fighting Systems': 8,
    'Fitness Centre / GYM': 8,
    'Flower Garden': 7,
    'Food Court': 6,
    'Foosball': 5,
    'Football': 7,
    'Fountain': 7,
    'Gated Community': 7,
     'Golf Course': 10,
    'Grocery Shop': 6,
    'Gymnasium': 8,
    'High Ceiling Height': 8,
    'High Speed Elevators': 8,
    'Infinity Pool': 9,
    'Intercom Facility': 7,
    'Internal Street Lights': 6,
    'Internet/wi-fi connectivity': 7,
    'Jacuzzi': 9,
    'Jogging Track': 7,
    'Landscape Garden': 8,
    'Laundry': 6,
    'Lawn Tennis Court': 8,
    'Library': 8,
    'Lounge': 8,
    'Low Density Society': 7,
    'Maintenance Staff': 6,
    'Manicured Garden': 7,
    'Medical Centre': 5,
    'Milk Booth': 4,
    'Mini Theatre': 9,
    'Multipurpose Court': 7,
    'Multipurpose Hall': 7,
    'Natural Light': 8,
    'Natural Pond': 7,
    'Park': 8,
    'Party Lawn': 8,
    'Piped Gas': 7,
    'Pool Table': 7,
    'Power Back up Lift': 8,
    'Private Garden / Terrace': 9,
    'Property Staff': 7,
    'RO System': 7,
    'Rain Water Harvesting': 7,
    'Reading Lounge': 8,
    'Restaurant': 8,
    'Salon': 8,
    'Sauna': 9,
    'Security / Fire Alarm': 9,
    'Security Personnel': 9,
    'Separate entry for servant room': 8,
    'Sewage Treatment Plant': 6,
    'Shopping Centre': 7,
    'Skating Rink': 7,
    'Solar Lighting': 6,
    'Solar Water Heating': 7,
    'Spa': 9,
    'Spacious Interiors': 9,
    'Squash Court': 8,
    'Steam Room': 9,
    'Sun Deck': 8,
    'Swimming Pool': 8,
    'Temple': 5,
    'Theatre': 9,
    'Toddler Pool': 7,
    'Valet Parking': 9,
    'Video Door Security': 9,
    'Visitor Parking': 7,
    'Water Softener Plant': 7,
    'Water Storage': 7,
    'Water purifier': 7,
    'Yoga/Meditation Area': 7
}
    
    def __init__(self, dataframe):
        self.df = dataframe
        
    @staticmethod
    def get_super_built_up_area(text):
            match = re.search(r'Super Built up area (\d+\.?\d*)', text)
            if match:
                return float(match.group(1))
            return None
        
    @staticmethod
    def get_area(text, area_type):
            match = re.search(area_type + r'\s*:\s*(\d+\.?\d*)', text)
            if match:
                return float(match.group(1))
            return None
    
    @staticmethod
    def convert_to_sqft(text, area_value):
            if area_value is None:
                return None
            match = re.search(r'{} \((\d+\.?\d*) sq.m.\)'.format(area_value), text)
            if match:
                sq_m_value = float(match.group(1))
                return sq_m_value * 10.7639  
            return area_value
        
    @staticmethod
    def extract_plot_area(value):
            match = re.search(r'Plot area (\d+\.?\d*)', value)
            return float(match.group(1))
        
    @staticmethod
    def unit_conversion(value):
        if np.isnan(value["area"]) or np.isnan(value["built_up_area"]):
            return value["built_up_area"]
        else:
            if round(value["area"]/value["built_up_area"],2) == 9:
                return value["built_up_area"] * 9
            elif round(value["area"]/value["built_up_area"],2) == 11:
                return value["built_up_area"] * 10.7
            elif round(value["area"]/value["built_up_area"],2) == 1:
                return value["built_up_area"] 
    
    def extract_super(self):      
        logging.info("Extracting Super Builtup area")
        self.df['super_built_up_area'] = self.df['areaWithType'].apply(self.get_super_built_up_area)
        logging.info("Super Builtup Area extracted")
        
    def area_extract(self):
        logging.info("Extracting Builtup area")
        self.df['built_up_area'] = self.df['areaWithType'].apply(lambda x: self.get_area(x, 'Built Up area'))
        logging.info("Builtup area Extracted")
        
        logging.info("Extracting Carpet area")
        self.df['carpet_area'] = self.df['areaWithType'].apply(lambda x: self.get_area(x, 'Carpet area'))
        logging.info("Carpet area Extracted")
    
    def area_conversion(self):
        logging.info("Converting Super Builtup Area to Sqft")
        self.df['super_built_up_area'] = self.df.apply(lambda x: self.convert_to_sqft(x['areaWithType'], x['super_built_up_area']), axis=1)
        logging.info("Converted Super Builtup Area to Sqft")
        
        logging.info("Converting Builtup Area to Sqft")
        self.df['built_up_area'] = self.df.apply(lambda x: self.convert_to_sqft(x['areaWithType'], x['built_up_area']), axis=1)
        logging.info("Converted Builtup Area to Sqft")
        
        logging.info("Converting Carpet Area to Sqft")
        self.df['carpet_area'] = self.df.apply(lambda x: self.convert_to_sqft(x['areaWithType'], x['carpet_area']), axis=1)
        logging.info("Converted Carpet Area into Sqft")
    
    def newcols_null(self):
        df_null = self.df[((self.df["super_built_up_area"].isnull()) & (self.df["built_up_area"].isnull()) & (self.df["carpet_area"].isnull()))][['price','property_type','area','areaWithType','super_built_up_area','built_up_area','carpet_area']]
        return df_null
        
    def plot_extract(self, df):
        logging.info("Extracting Plot Area")
        df["built_up_area"] = df["areaWithType"].apply(self.extract_plot_area)
        logging.info("Extracted Plot Area")
        
    def area_unit_conversion(self, df):
        logging.info("Unit conversion of Builtup Area started")
        df["built_up_area"] = df.apply(FeatureEngineering.unit_conversion, axis=1)
        logging.info("Unit conversion of Builtup Area completed")
    
    def process_and_update(self):
        df_nulls = self.newcols_null()
        logging.info("Created a new dataframe from instance's dataframe")
        self.plot_extract(df_nulls)
        self.area_unit_conversion(df_nulls)
        
        logging.info("Updating back to original df")
        self.df.update(df_nulls)
        logging.info("Original DataFrame updated with transformed data.")
        
    def additional_room(self):
        columns = ["servant room", "pooja room", "store room", "study room", "others"] 
        logging.info("Begining to break down each column category into a seperate column")
        for col in columns:
            self.df[col] = self.df['additionalRoom'].str.contains(col).astype(int)
        logging.info("Broke down each column category into a seperate column")
    
    
    
    @staticmethod
    def categorisation(value):
        if pd.isna(value):
            return "undefined"
        if "0 to 1 Year Old" in value or "Within 3 months" in value or "Within 6 months" in value:
            return "new property"
        if "1 to 5 Year Old" in value:
            return "relatively new"
        if "5 to 10 Year Old" in value:
            return "moderately new"
        if "10+ Year Old" in value:
            return "old property"
        if "Under Construction" in value or "By" in value:
            return "under construction"
        
        try:
            int(value.split(" ")[-1])
            return "under construction"
        except:
            return "Undefined"   
    
    def age_possession(self):
        logging.info("Renaming each subcategory")
        self.df["agePossession"] = self.df["agePossession"].apply(self.categorisation)
        logging.info("Renamed each subcategory")
        
        
        
    @staticmethod
    def get_furnishing_count(details, furnishing):
        if isinstance(details, str):
            if f"No {furnishing}" in details:
                return 0
            pattern = re.compile(f"(\d+) {furnishing}")
            match = pattern.search(details)
            if match:
                return int(match.group(1))
            elif furnishing in details:
                return 1
        return 0  
        
    def furnish_detail(self):
        all_furnishings = []
        logging.info("Extracting unique details from furnishing details column")
        for detail in self.df['furnishDetails'].dropna():
            furnishings = detail.replace('[', '').replace(']', '').replace("'", "").split(', ')
            all_furnishings.extend(furnishings)
        unique_furnishings = list(set(all_furnishings))
        logging.info("Extracted unique details from furnishing details column")
        
        logging.info("Simplify the furnishings list by removing NO prefix and numbers")
        columns_to_include = [re.sub(r'No |\d+', '', furnishing).strip() for furnishing in unique_furnishings]
        logging.info("Simplied the furnishings list by removing NO prefix and numbers")
        
        logging.info("Extracting unique furnishing")
        columns_to_include = list(set(columns_to_include))  
        logging.info("Extracted unique furnishing")
        
        logging.info("Removing empty strings")
        columns_to_include = [furnishing for furnishing in columns_to_include if furnishing] 
        logging.info("Removed empty strings")
        
        logging.info("Create new columns for each unique furnishing and populate with counts")
        for furnishing in columns_to_include:
            self.df[furnishing] = self.df['furnishDetails'].apply(lambda x: self.get_furnishing_count(x, furnishing))
        logging.info("Created new columns for each unique furnishing and populate with counts")
        
        logging.info("Create the new dataframe with the required columns")
        furnishings_df = self.df[['furnishDetails'] + columns_to_include]   
        logging.info("Created the new dataframe with the required columns")     
        
        return furnishings_df
    
    def append_cluster_labels(self, num_clusters=3):
        furnishings_df = self.furnish_detail()
        
        logging.info("Drop 'furnishDetails' column")
        furnishings_df = furnishings_df.drop('furnishDetails', axis=1)
        logging.info("Dropped 'furnishDetails' column")

        logging.info("Scaling the data")
        furnishings_scaled = scaler.fit_transform(furnishings_df)
        logging.info("Scaled the data")

        logging.info("Performing Kmeans Clustering")
        kmeans = KMeans(n_clusters=num_clusters, random_state=0)
        cluster_labels = kmeans.fit_predict(furnishings_scaled)
        logging.info("Generated cluster labels from clustering")

        logging.info("Append cluster labels to the main DataFrame")
        self.df['Cluster_Labels'] = cluster_labels
        logging.info("Dataframe updated with new column containing labels")
    
    def update_features_from_property(self, appartments_csv_path):
        logging.info("Loading another dataframe from a csv file")
        df2 = pd.read_csv(appartments_csv_path)
        df2["PropertyName"] = df2["PropertyName"].str.lower()
        logging.info("Loaded another dataframe from a csv file")
        
        logging.info("Select rows where 'features' is null in self.df")
        null_temp = self.df[self.df["features"].isnull()]
        logging.info("Null features selected")

        logging.info("Merging null_temp with df2 based on matching 'society' and 'PropertyName'")
        merged_df = null_temp.merge(df2, left_on="society", right_on="PropertyName", how="left")
        logging.info("Merged null_temp with df2 based on matching 'society' and 'PropertyName'")

        logging.info("Extracting 'TopFacilities' from the merged DataFrame")
        top_facilities = merged_df["TopFacilities"]
        logging.info("Extracted 'TopFacilities' from the merged DataFrame")

        logging.info("Updating 'features' in the main DataFrame for the indices corresponding to null_temp")
        self.df.loc[null_temp.index, "features"] = top_facilities.values
        logging.info("Update complete")
    
    def extract_unique_feature(self):
        logging.info("Converting each row in its literal form")
        self.df["features"] = self.df["features"].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) and x.startswith('[') else [])
        logging.info("Conversion complete")
        
        features_df = pd.DataFrame()
        unique_features = set()

        logging.info("Extracting unique features")
        for row in self.df["features"]:
            unique_features.update(row)
        logging.info("Extracted unique features")

        unique_features = [item.replace('/',"").replace('\\',"").strip() for item in unique_features]

        logging.info("Creating a new df with seperate column for each unique feature")
        for feature in unique_features:
            features_df[feature] = self.df["features"].apply(lambda x: 1 if feature in x else 0)
        logging.info("Dataframe created")
        
        return features_df
        
    
    
    @staticmethod
    def cal_feature_score(row):
        score = 0
        for feature, feature_score in FeatureEngineering.weights.items():
            if row.get(feature, 0) == 1:
                score += feature_score
        return score
    
    def luxury_score(self, df):
        logging.info("Calculating luxury score for each property")
        df["luxury_score"] = df.apply(self.cal_feature_score, axis=1)
        logging.info("Luxury Score calculated")
        
    def process_update2(self):
        features_df = self.extract_unique_feature()
        self.luxury_score(features_df)
        
        logging.info("Updating the original df with luxury score")
        self.df["luxury_score"] = features_df["luxury_score"]
        logging.info("Original df now has luxury score")
    
    def cols_drop(self):
        logging.info("Dropping unnecessary columns")
        self.df.drop(columns=["additionalRoom", "nearbyLocations", "furnishDetails", "features"], inplace=True)
        logging.info("Dropping unwanted columns")

    def combined_run4(self, appartments_csv_path):
        self.extract_super()
        self.area_extract()
        self.area_conversion()
        self.process_and_update()  # Internally handles the operations related to df_nulls
        self.additional_room()
        self.age_possession()
        self.append_cluster_labels(num_clusters=3)  # This method internally calls furnish_detail
        self.update_features_from_property(appartments_csv_path)
        self.process_update2()
        self.cols_drop()
        logging.info("Final run")

        return self.df

    def run_preprocessing(input_path, output_path):
        df = pd.read_csv(input_path)    
        preprocessor = FeatureEngineering(df)
        processed_df = preprocessor.combined_run4()
        processed_df.to_csv(output_path, index=False)
    

if __name__ == "__main__":
    try:
        datapath1 = "/Users/siddhant/housepriceproject/Capstone/pipeline_generated_data/merged_processed.csv"
        datapath2 = "/Users/siddhant/housepriceproject/Capstone/data/raw/appartments.csv"
        output_path = "/Users/siddhant/housepriceproject/Capstone/pipeline_generated_data"
        
        df = pd.read_csv(datapath1)
        
        engineer = FeatureEngineering(df)
        final_df = engineer.combined_run4(datapath2)
        final_df.to_csv(os.path.join(output_path, "feature_engineered.csv"))
    except Exception as e:
        logging.info(f"Error occured: {e}")
        raise CustomException(e, sys)