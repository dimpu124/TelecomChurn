from feast import FeatureStore
import pandas as pd

# Load the feature store
store = FeatureStore(repo_path=".")

# Define a list of customer IDs you want features for
customer_df = pd.DataFrame({"customer_id": ["2", "3"]})

# Fetch features
features = store.get_online_features(
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
        "customer_features_view:Churn",
    ],
    entity_rows=customer_df.to_dict("records"),
).to_df()

print(features)