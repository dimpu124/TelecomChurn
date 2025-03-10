import os
import shutil
from datetime import datetime


# Define storage paths
RAW_DATA_PATH = r"C:\Users\sahus\Documents\Mtech\Second Sem\DMML\Assgn\raw_data"
ARCHIVE_PATH = r"C:\Users\sahus\Documents\Mtech\Second Sem\DMML\Assgn\archive"

# Create directories if they don't exist
os.makedirs(RAW_DATA_PATH, exist_ok=True)
os.makedirs(ARCHIVE_PATH, exist_ok=True)

# Define folder structure: source/type/timestamp
def get_storage_path(source, data_type):
    timestamp = datetime.now().strftime('%Y-%m-%d')
    return os.path.join(RAW_DATA_PATH, source, data_type, timestamp)

# Move ingested files to structured storage
def store_raw_data(file_path, source, data_type):
    try:
        destination_path = get_storage_path(source, data_type)
        os.makedirs(destination_path, exist_ok=True)
        shutil.move(file_path, os.path.join(destination_path, os.path.basename(file_path)))
        print(f"Stored {file_path} in {destination_path}")
    except Exception as e:
        print(f"Error storing file {file_path}: {e}")

# Example usage
store_raw_data(r"C:\Users\sahus\Documents\Mtech\Second Sem\DMML\Assgn\output\transactions_api.csv", "api", "source")
store_raw_data(r"C:\Users\sahus\Documents\Mtech\Second Sem\DMML\Assgn\output\transactions_raw.csv", "csv", "source")
