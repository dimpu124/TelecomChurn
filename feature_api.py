import pandas as pd
from datetime import datetime, timezone, timedelta
from feast import FeatureStore
from fastapi import FastAPI

app = FastAPI()

# Initialize Feature Store
store = FeatureStore(repo_path=r"C:\Users\sahus\Documents\TelecomChurn\customer_churn_feature_store\feature_repo")

#uvicorn feature_api:app --reload


@app.get("/fetch_features")
def fetch_features(customer_id: int):
    # Create Entity DataFrame with the provided CustomerID
    entity_df = pd.DataFrame({
        "CustomerID": [customer_id],
        "event_timestamp": [datetime.utcnow().replace(tzinfo=timezone.utc)]
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

    # Convert to JSON and return
    return feature_data.to_dict(orient="records")
