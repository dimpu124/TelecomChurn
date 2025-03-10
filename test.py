import pandas as pd
from datetime import datetime, timedelta
from feast import FeatureStore
from datetime import datetime, timezone, timedelta

# Initialize Feature Store
store = FeatureStore(repo_path=".")

# Create Entity DataFrame
entity_df = pd.DataFrame({
    "CustomerID": [2, 3, 4,5,6],
    "event_timestamp": [
        datetime.utcnow().replace(tzinfo=timezone.utc),  # ✅ Convert to UTC
        datetime.utcnow().replace(tzinfo=timezone.utc),
        datetime.utcnow().replace(tzinfo=timezone.utc),
        datetime.utcnow().replace(tzinfo=timezone.utc),
        datetime.utcnow().replace(tzinfo=timezone.utc),
    ]
})


entity_df["event_timestamp"] = pd.to_datetime(entity_df["event_timestamp"]) 

# Fetch Features
feature_data = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "customer_features_view:Age",
        "customer_features_view:Total Spend",
    ]
).to_df()

print(feature_data)
