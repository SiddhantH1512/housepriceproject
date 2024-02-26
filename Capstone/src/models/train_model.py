import sys
sys.path.append('/Users/siddhant/housepriceproject')
import pandas as pd 
import numpy as np 
from Capstone.logger import logging
from Capstone.exception import CustomException
from sklearn.preprocessing import OneHotEncoder, StandardScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer
import category_encoders as ce
from sklearn.metrics import r2_score, mean_absolute_error
from hyperopt import hp, fmin, tpe, STATUS_OK, Trials, space_eval
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
import mlflow
from mlflow.sklearn import log_model
import warnings
import os
import re

warnings.filterwarnings("ignore")

class HyperParameterTune:
    def __init__(self, dataframe):
        self.df = dataframe
        self.transform = self.data_transform()
        self.data_split()
        self.pipeline()
        self.space = {
        'XGBRegressor__n_estimators': hp.choice('n_estimators', range(50, 1500, 50)),
        'XGBRegressor__learning_rate': hp.uniform('learning_rate', 0.01, 0.3),
        'XGBRegressor__max_depth': hp.choice('max_depth', range(3, 21, 1)),
        'XGBRegressor__min_samples_split': hp.choice('min_samples_split', range(2, 21, 2)),
        'XGBRegressor__min_samples_leaf': hp.choice('min_samples_leaf', range(1, 21, 1)),
        'XGBRegressor__max_features': hp.choice('max_features', ['sqrt', 'log2', None]),
        'XGBRegressor__subsample': hp.uniform('subsample', 0.5, 1.0)
    }

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
    
    def pipeline(self):
        pipeline = Pipeline([
            ('Transformer', self.transform),
            ('XGBRegressor', XGBRegressor())
        ])
        
        return pipeline

    def data_split(self):
        logging.info("Splitting the data into training and testing sets")
        X = self.df.drop(columns="price")
        y = self.df["price"]
        y_transformed = np.log1p(y)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y_transformed, test_size=0.2, random_state=42)
        logging.info("Data split successfully")
   
   
    @staticmethod
    def objective(params, pipeline, x, y):
        pipeline.set_params(**params)
        score = cross_val_score(pipeline, x, y, scoring='r2', cv=5).mean()
        loss = -score
        return {'loss': loss, 'status': STATUS_OK}
    
    def hyperopt(self):
        trials = Trials()
        best_params = fmin(
            fn=lambda params: self.objective(params, self.pipeline(), self.X_train, self.y_train),
            space=self.space,
            algo=tpe.suggest,
            max_evals=500,
            trials=trials
        )
        # convert best_params to the right format if necessary
        final_params = space_eval(self.space, best_params)
        logging.info("Best parameters recorded from hyperopt")
        return final_params
    
    def final_model_run(self, parameters):
        pipe = self.pipeline()
        pipe.set_params(**parameters)  
        pipe.fit(self.X_train, self.y_train)
        
        logging.info("Making prediction")
        y_pred = pipe.predict(self.X_test)  
        score = r2_score(np.expm1(self.y_test), np.expm1(y_pred))  
        logging.info("Prediction made and r2 score calculated")
        
        return score, pipe
        
    def run_all(self):
        best_params = self.hyperopt()
        r2_score, pipe = self.final_model_run(best_params)
        return [('XGBoost', r2_score, pipe)]
        
if __name__ == "__main__":
    try:
        mlflow.set_experiment("Final Model")

        with mlflow.start_run():
            datapath = "/Users/siddhant/housepriceproject/Capstone/pipeline_generated_data/missing_imputed.csv"
            df = pd.read_csv(datapath)
            tuner = HyperParameterTune(df)

            # Run the tuning and final model training
            model_name, r2, model_pipeline = tuner.run_all()[0]  # Access the first (and only) result

            # Debugging print statements
            print(f"Logging to MLflow. Model: {model_name}, R2: {r2}")

            # Log the metrics and model to MLflow
            mlflow.log_metric(f"{model_name}_R2", r2)
            log_model(model_pipeline, model_name)

            mlflow.end_run()

        logging.info("Model training and evaluation completed.")
    except Exception as e:
        logging.error(f"Following error occurred: {e}")
        raise CustomException(e, sys)


        
      
        

