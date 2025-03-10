import mlflow
from mlflow.models import infer_signature

import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from mlflow.models import infer_signature
import os
import pickle

dbname='postgres'
user='postgres'
password='admin'
host='localhost'
port='5432'


engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/{dbname}')
query = "SELECT * FROM transformed_data"
df = pd.read_sql(query, engine)

X = df.drop(columns=["CustomerID", "Churn"])
y = df["Churn"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Set our tracking server uri for logging
mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")

# Create a new MLflow Experiment
mlflow.set_experiment("Telcom_Churn_Predictionv1")

loaded_model = mlflow.pyfunc.load_model('runs:/24bf851ccf084f1898d190c6c34d51b0/churn_model')

predictions = loaded_model.predict(X_test)

result = pd.DataFrame(X_test)
result["actual_class"] = y_test
result["predicted_class"] = predictions

print(result[:10])