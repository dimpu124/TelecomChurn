from fastapi import FastAPI
from feast import FeatureStore
import pandas as pd

app = FastAPI()



# Initialize Feast feature store
store = FeatureStore(repo_path="c:/Users/sahus/Documents/DMML/feature_repo/feature_repo")

@app.get("/features/{customer_id}")
def get_customer_features(customer_id: int):
    entity_df = pd.DataFrame({"customer_id": [customer_id]})
    
    feature_vector = store.get_online_features(
        features=[
            "customer_features_view:Age",
            "customer_features_view:Gender",
            "customer_features_view:Tenure",
            "customer_features_view:Usage Frequency",
            "customer_features_view:Support Calls",
            "customer_features_view:Payment Delay",
            "customer_features_view:Subscription Type",
            "customer_features_view:Contract Length",
            "customer_features_view:Total Spend",
            "customer_features_view:Last Interaction",
            "customer_features_view:Churn",
            "customer_features_view:Avg Monthly Spend",
            "customer_features_view:Activity Rate"
        ],
        entity_rows=entity_df.to_dict(orient="records"),
    ).to_dict()

    return feature_vector
