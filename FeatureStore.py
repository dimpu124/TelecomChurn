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

DB_NAME='postgres'
DB_USER='postgres'
DB_PASSWORD='admin'
DB_HOST='localhost'
DB_PORT='5432'

customer = Entity(name="customer_id", value_type=ValueType.INT64)

f_source = FileSource(
    path=r"C:\Users\sahus\Documents\DMML\feature_repo\feature_repo\data\raw.csv",
    timestamp_field="event_timestamp",
    created_timestamp_column="created",
)

customer_features_fv = FeatureView(
    name="customer_features_view",
    ttl=timedelta(days=3),
    entities=[customer],
    schema=[
        Field(name="Age", dtype=Int64),
        Field(name="Gender", dtype=Int64),
        Field(name="Tenure", dtype=Int64),
        Field(name="Usage Frequency", dtype=Int64),
        Field(name="Support Calls", dtype=Int64),
        Field(name="Payment Delay", dtype=Int64),
        Field(name="Subscription Type", dtype=Int64),
        Field(name="Contract Length", dtype=Int64),
        Field(name="Total Spend", dtype=Float32),
        Field(name="Last Interaction", dtype=Int64),
        Field(name="Churn", dtype=Int64),
        Field(name="Avg Monthly Spend", dtype=Float32),
        Field(name="Activity Rate", dtype=Float32),
    ],
    source=f_source
)

# Save Feast feature repository
repo_path = r"c:/Users/sahus/Documents/DMML/feature_repo/feature_repo"

store = FeatureStore(repo_path)
store.apply([customer, customer_features_fv])

print("Feast feature store configured for telecom churn data.")