import boto3
import sys
sys.path.append("/Users/siddhant/housepriceproject")
from Capstone.logger import logging
from botocore.exceptions import NoCredentialsError


file_paths = {
    "/Users/siddhant/housepriceproject/Capstone/datasets/cosinse_sim.pkl": "models/cosinse_sim.pkl",
    "/Users/siddhant/housepriceproject/Capstone/datasets/cosinse_sim2.pkl": "models/cosinse_sim2.pkl",
    "/Users/siddhant/housepriceproject/Capstone/datasets/cosinse_sim3.pkl": "models/cosinse_sim3.pkl",
    "/Users/siddhant/housepriceproject/Capstone/datasets/locationdf.pkl": "files/locationdf.pkl",
    "/Users/siddhant/housepriceproject/Capstone/datasets/wordcloud_data.pkl": "files/wordcloud_data.pkl"
}

bucket_name = "capstone-houseprice-prediction"

def s3_upload(local_file_path, s3_bucket, s3_file_path):
    s3 = boto3.client("s3")
    try:
        logging.info(f"Uploading file {local_file_path} to S3 bucket {s3_bucket} at {s3_file_path}")
        s3.upload_file(local_file_path, s3_bucket, s3_file_path)
        logging.info(f"Uploaded file {local_file_path} to S3 bucket {s3_bucket} at {s3_file_path}")
    except FileNotFoundError:
        logging.exception(f"The file {local_file_path} was not found.")
    except NoCredentialsError:
        logging.exception("Credentials not available.")
    except Exception as e:
        logging.exception(f"An error occurred while uploading {local_file_path}: {e}")

# Upload each file
for local_path, s3_path in file_paths.items():
    s3_upload(local_path, bucket_name, s3_path)
