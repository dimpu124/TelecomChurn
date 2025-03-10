import pandas as pd
import requests
import logging
import time
from datetime import datetime
import requests
import base64
import zipfile
import io
import pandas as pd


# Configure logging
logging.basicConfig(filename=r'C:\Users\sahus\Documents\Mtech\Second Sem\DMML\Assgn\log\ingestion.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_csv_data():
    try:
        df = pd.read_csv(r'C:\Users\sahus\Documents\Mtech\Second Sem\DMML\Assgn\input\customer_churn_dataset-training-master.csv')  # Replace with actual file path or cloud location
        df.to_csv(r'C:\Users\sahus\Documents\Mtech\Second Sem\DMML\Assgn\output\transactions_raw.csv', index=False)
        logging.info("Successfully ingested CSV data")
    except Exception as e:
        logging.error(f"Failed to ingest CSV data: {e}")

def fetch_api_data():
    try:
        base_url = "https://www.kaggle.com/api/v1"
        owner_slug = "blastchar"
        dataset_slug = "telco-customer-churn"
        dataset_version = "1"

        url = f"{base_url}/datasets/download/{owner_slug}/{dataset_slug}?datasetVersionNumber={dataset_version}"

        #2: Encoding the credentials and preparing the request header.
        username = "saumyaranjansahu"
        key = "b4f2ba64df7aa4cd4a731b412ae32354"
        creds = base64.b64encode(bytes(f"{username}:{key}", "ISO-8859-1")).decode("ascii")
        headers = {
          "Authorization": f"Basic {creds}"
        }

        #3: Sending a GET request to the URL with the encoded credentials.
        response = requests.get(url, headers=headers)
        print(response)
        #4: Loading the response as a file via io and opening it via zipfile.
        zf = zipfile.ZipFile(io.BytesIO(response.content))

        #5: Reading the CSV from the zip file and converting it to a dataframe.
        file_name = "WA_Fn-UseC_-Telco-Customer-Churn.csv"
        df = pd.read_csv(zf.open(file_name))
        df.to_csv(r'C:\Users\sahus\Documents\Mtech\Second Sem\DMML\Assgn\output\transactions_api.csv', index=False)
        logging.info(f"Data From API feteched successfully")
    except Exception as e:
        logging.error(f"Failed to fetch API data: {e}")

def run_ingestion():
    logging.info("Starting data ingestion pipeline")
    fetch_csv_data()
    fetch_api_data()
    logging.info("Data ingestion pipeline completed")

if __name__ == "__main__":
    run_ingestion()