import pandas as pd
import numpy as np
import sys
sys.path.append('/Users/siddhant/housepriceproject')
import category_encoders as ce
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import OneHotEncoder, StandardScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR

from Capstone.logger import logging
from Capstone.exception import CustomException

import mlflow
from mlflow.sklearn import log_model

class DataModelling:
    def __init__(self, dataframe):
        self.df = dataframe
        self.transform = self.data_transform()
        self.data_split()

    def data_transform(self):
        logging.info("Creating the transform Column transformer")
        columns_encode_ordinal = ['property_type', 'balcony', 'furniture_type', 'luxury_level', 'floor_category']
        columns_scale = ['bedRoom', 'bathroom', 'built_up_area', 'servant room', 'store room']
        columns_encode_ohe = ['agePossession']
        columns_target_encode = ['sector']

        transform = ColumnTransformer(transformers=[
            ('target', ce.TargetEncoder(), columns_target_encode),
            ('ordinal', OrdinalEncoder(), columns_encode_ordinal),
            ('ohe', OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False), columns_encode_ohe),
            ('scale', StandardScaler(), columns_scale)
        ], remainder="passthrough")
        logging.info("Column transformer created")
        
        return transform

    def data_split(self):
        logging.info("Splitting the data into training and testing sets")
        X = self.df.drop(columns="price")
        y = self.df["price"]
        y_transformed = np.log1p(y)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y_transformed, test_size=0.2, random_state=42)
        logging.info("Data split successfully")
    
    def scorer(self, model, model_name):
        pipeline = Pipeline([
            ('transform', self.transform),
            (model_name, model)
        ])
        kfold = KFold(n_splits=10, shuffle=True, random_state=42)
        score = cross_val_score(pipeline, self.X_train, self.y_train, cv=kfold, scoring='r2')
        mean_score = np.nanmean(score)
        
        pipeline.fit(self.X_train, self.y_train)
        y_pred = pipeline.predict(self.X_test)
        y_pred = np.expm1(y_pred)
        y_test = np.expm1(self.y_test)

        mae = mean_absolute_error(y_test, y_pred)
        
        return model_name, mean_score, mae, pipeline
    
    def train_and_evaluate_models(self):
        model_dict = {
            'linear_reg': LinearRegression(),
            'lasso_reg': Lasso(),
            'ridge_reg': Ridge(),
            'svr': SVR(),
            'randomforest_reg': RandomForestRegressor(),
            'extratree': ExtraTreesRegressor(),
            'gradientboost': GradientBoostingRegressor(),
            'adaboost': AdaBoostRegressor(),
            'xgboost': XGBRegressor(),
            'decisiontree': DecisionTreeRegressor()
        }
        
        model_output = []
        for model_name, model in model_dict.items():
            try:
                logging.info(f"Training and evaluating {model_name}...")
                output = self.scorer(model, model_name)
                model_output.append(output)
                logging.info(f"{model_name} trained and evaluated successfully.")
            except Exception as e:
                logging.error(f"Error occurred while training and evaluating {model_name}: {e}")
                raise CustomException(e)

        return model_output

if __name__ == "__main__":
    try:
        mlflow.set_experiment("House_Price_Prediction")

        with mlflow.start_run():
            datapath = "/Users/siddhant/housepriceproject/Capstone/data/ready/missing_imputed.csv"
            df = pd.read_csv(datapath)
            model_trainer = DataModelling(df)

            model_output = model_trainer.train_and_evaluate_models()

            for model_name, r2, mae, model_pipeline in model_output:
                mlflow.log_metric(f"{model_name}_R2", r2)
                mlflow.log_metric(f"{model_name}_MAE", mae)
                log_model(model_pipeline, model_name)

            mlflow.end_run()

        logging.info("Model training and evaluation completed.")
    except Exception as e:
        logging.info(f"Following error occurred: {e}")
        raise CustomException(e, sys)








        
        
        
        
        
        
        
        
        
        
        
        
