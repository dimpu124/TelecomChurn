import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import psycopg2  # PostgreSQL
from sqlalchemy import create_engine
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, confusion_matrix, classification_report,
                             ConfusionMatrixDisplay, roc_curve, auc)
from sklearn.model_selection import train_test_split, GridSearchCV, learning_curve

data = pd.read_csv(r'C:\Users\sahus\OneDrive\Documents\TelecomChurn\folder_with_data\raw.csv')
data = data.drop(columns=['customerID'], errors='ignore')
print(data.columns)
# 2. Encode binary categorical variables
binary_columns = ['gender']
label_enc = LabelEncoder()
for column in binary_columns:
    if column in data.columns:  # Check if column exists
        data[column] = label_enc.fit_transform(data[column].astype(str))


multi_class_columns = ['Subscription Type', 'Contract Length']

data = pd.get_dummies(data, columns=multi_class_columns, drop_first=True)


# 4. Convert 'MonthlyCharges', 'TotalCharges', and 'tenure' to numeric, coercing errors to NaN
data['Total Spend'] = pd.to_numeric(data['Total Spend'], errors='coerce')
data['Tenure'] = pd.to_numeric(data['Tenure'], errors='coerce')

# Fill NaN values in 'TotalCharges' with 0 (or another strategy, e.g., mean or median)
data['Total Spend'] = data['Total Spend'].fillna(0)


# 5. Create new features
# LongTermCustomer flag: customers with tenure > 12 months
data['LongTermCustomer'] = (data['Tenure'] > 12).astype(int)

# Total Charges per Tenure
data['TotalChargesPerTenure'] = data['Total Spend'] / (data['Tenure'] + 1)


# 6. Ensure all values are numeric
data = data.apply(pd.to_numeric, errors='coerce')


if data.isnull().sum().any():
    print("\nThere are NaN values in the DataFrame after conversion:")
    print(data.isnull().sum())
    data = data.fillna(0)  # Handle NaN values by filling with 0 or an appropriate strategy


dbname='postgres'
user='postgres'
password='admin'
host='localhost'
port='5432'

conn = psycopg2.connect(
    dbname='postgres', user='postgres', password='admin', host='localhost', port='5432'
)

data.to_parquet(r'C:\Users\sahus\OneDrive\Documents\TelecomChurn\folder_with_data\dataprep')
engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/{dbname}')
data.to_sql('transformed_data', engine,if_exists='replace',index=False)

