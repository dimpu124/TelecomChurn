import pandas as pd
from sklearn.preprocessing import StandardScaler
import psycopg2  # PostgreSQL
from sqlalchemy import create_engine
from feast.types import Int64, Float32, String, Int32
from datetime import datetime
import os
from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import PostgreSQLSource
from feast import Entity, FeatureStore, FeatureView, FileSource, ValueType, Field
from datetime import datetime, timedelta

# Define the Customer entity (✅ Fix: Use Entity object)
customer = Entity(name="CustomerID", value_type=ValueType.INT64)

# Define the data source
customer_data_source = FileSource(
    path="data/dataprep.parquet",  # Ensure the file path is correct
    timestamp_field="Last Interaction",  # Event time (e.g., customer activity)
)


# Define feature view (✅ Fix: Pass entity object instead of string)
customer_features = FeatureView(
    name="customer_features_view",
    entities=[customer],  # ✅ Fix: Pass the entity object
    ttl=None,
    schema=[
        Field(name="Age", dtype=Int32),
        Field(name="Gender", dtype=Int32),
        Field(name="Tenure", dtype=Int32),
        Field(name="Usage_Frequency", dtype=Int32),
        Field(name="Support Calls", dtype=Int32),
        Field(name="Payment Delay", dtype=Float32),
        Field(name="Total Spend", dtype=Float32),
        Field(name="Churn", dtype=Int32),
        Field(name="Subscription Type Premium", dtype=Int32),
        Field(name="Subscription Type Standard", dtype=Int32),
        Field(name="Contract Length Monthly", dtype=Int32),
        Field(name="Contract Length Quarterly", dtype=Int32),
        Field(name="LongTermCustomer", dtype=Int32),
        Field(name="TotalChargesPerTenure", dtype=Float32)
    ],
    source=customer_data_source
)
