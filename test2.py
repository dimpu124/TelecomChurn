import pandas as pd
from datetime import datetime, timedelta
df = pd.read_parquet(r'C:\Users\sahus\Documents\TelecomChurn\customer_churn_feature_store\feature_repo\data\dataprep.parquet')
df["Last Interaction"] = pd.Timestamp.utcnow()
df.to_parquet(r'C:\Users\sahus\Documents\TelecomChurn\customer_churn_feature_store\feature_repo\data\dataprep.parquet')
print(df['Last Interaction'])