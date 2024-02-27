import boto3
import sys
sys.path.append("/Users/siddhant/housepriceproject")
from Capstone.logger import logging
from botocore.exceptions import NoCredentialsError

def upload_to_s3(file_paths, bucket_name, s3_model_paths):
    """
    Uploads multiple files to S3.

    :param file_paths: List of local file paths to upload.
    :param bucket_name: S3 bucket name.
    :param s3_model_paths: List of S3 file paths where the files will be uploaded.
    """
    logging.info("Creating S3 client")
    s3 = boto3.client('s3')
    logging.info("S3 client created")

    for local_file, s3_file in zip(file_paths, s3_model_paths):
        try:
            logging.info(f"Uploading file {local_file} to S3 bucket {bucket_name} at {s3_file}")
            s3.upload_file(local_file, bucket_name, s3_file)
            logging.info(f"File {local_file} uploaded successfully to {bucket_name}/{s3_file}")
        except FileNotFoundError:
            logging.exception(f"The file {local_file} was not found.")
        except NoCredentialsError:
            logging.exception("Credentials not available.")
        except Exception as e:
            logging.exception(f"An error occurred while uploading {local_file}: {e}")

local_model_path = '/Users/siddhant/housepriceproject/Capstone/pipeline.pkl'
local_df_path = '/Users/siddhant/housepriceproject/Capstone/df2.pkl'
s3_bucket_name = 'capstone-houseprice-prediction'
s3_model_path = 'models/pipeline.pkl'
s3_df_path = 'models/df2.pkl'

upload_to_s3([local_model_path, local_df_path], s3_bucket_name, [s3_model_path, s3_df_path])
