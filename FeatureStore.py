import pandas as pd
from sklearn.preprocessing import StandardScaler
import psycopg2  # PostgreSQL
from sqlalchemy import create_engine
from feast.types import Int64, Float32, String
from datetime import datetime
import os
from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import PostgreSQLSource
from feast import Entity, FeatureStore, FeatureView, FileSource, ValueType,Field
from datetime import datetime, timedelta

# Define the data source
customer_data_source = FileSource(
    path="data/dataprep.csv",  # Ensure the file path is correct
    timestamp_field="Last_Interaction",  # Event time (e.g., customer activity)
    created_timestamp_column="Ingestion_Time"  # Column for data ingestion time
)

# Define the Customer entity
customer = Entity(name="CustomerID", join_keys=["CustomerID"], value_type=ValueType.INT64)  # Ensure "CustomerID" exists in the dataset

# Define feature view
customer_features = FeatureView(
    name="customer_features_view",
    entities=["customer_id"],
    ttl=None,
    schema=[  # ✅ Use Field instead of Feature
        Field(name="Age", dtype=Int32),
        Field(name="Gender", dtype=String),
        Field(name="Tenure", dtype=Int32),
        Field(name="Usage_Frequency", dtype=Float32),
        Field(name="Support_Calls", dtype=Int32),
        Field(name="Payment_Delay", dtype=Float32),
        Field(name="Subscription_Type", dtype=String),
        Field(name="Contract_Length", dtype=Int32),
        Field(name="Total_Spend", dtype=Float32),
        Field(name="Churn", dtype=String),
    ],
    source=customer_data_source
)