
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow
import mlflow.sklearn
import psycopg2  # PostgreSQL
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

conn = psycopg2.connect(
    dbname='postgres', user='postgres', password='admin', host='localhost', port='5432'
)

def train_model():
    engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/{dbname}')
    query = "SELECT * FROM transformed_data"
    df = pd.read_sql(query, engine)
    print(df.head())

    X = df.drop(columns=["CustomerID", "Churn"])
    y = df["Churn"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Evaluate Model
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print(f"Model Performance:\n Accuracy: {accuracy}\n Precision: {precision}\n Recall: {recall}\n F1 Score: {f1}")
    return model,accuracy,precision,recall,f1,X_train

def save_model(model,accuracy,precision,recall,f1,X_train):
    #Save Model with MLflow
    mlflow.set_tracking_uri(uri="http://127.0.0.1:5000")
    mlflow.set_experiment("Telcom_Churn_Predictionv1")
    with mlflow.start_run():

    # Log the loss metric
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1", f1)

        # Set a tag that we can use to remind ourselves what this run was for
        mlflow.set_tag("Training Info", "Basic Model for Telecom Churn")

        # Infer the model signature
        signature = infer_signature(X_train, model.predict(X_train))

        # Log the model
        model_info = mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="churn_model",
        signature=signature,
        input_example=X_train,
        registered_model_name="Telecom_churn_model",
        )
        print("Model saved to MLflow.")
        filename = 'churn_model.pkl'
        folder = str(model_info.model_uri).split('/')[1]
        mlflow.sklearn.save_model(model,f'c:/Users/sahus/Documents/DMML/mlruns/{folder}/',serialization_format=mlflow.sklearn.SERIALIZATION_FORMAT_CLOUDPICKLE)
        pickle.dump(model, open(filename, 'wb'))

    return model_info

    


# Set our tracking server uri for logging
# Create a new MLflow Experiment
model,accuracy,precision,recall,f1,X_train = train_model()
model_info = save_model(model,accuracy,precision,recall,f1,X_train)
print(model_info.model_uri)