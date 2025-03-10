import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'folder_with_data/raw.csv')
df['Churn']=df['Churn'].map({0: 'False', 1: 'True'})

num_cols = df.select_dtypes(include=['number']).columns.drop("Churn", errors="ignore")

cat_cols = df.select_dtypes(include=['object']).columns



if len(cat_cols) > 0:
    # Fill missing categorical values with the most frequent value
    mode_imputer = SimpleImputer(strategy="most_frequent")
    df[cat_cols] = mode_imputer.fit_transform(df[cat_cols])

# --------------- Step 1: Handle Missing Values ---------------
# Fill missing numerical values with median
if len(num_cols) > 0:
    median_imputer = SimpleImputer(strategy="median")
    df[num_cols] = median_imputer.fit_transform(df[num_cols])

# --------------- Step 2: Normalize Numerical Features ---------------
scaler = StandardScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

# --------------- Step 3: Encode Categorical Variables using LabelEncoder ---------------
le = LabelEncoder()
for col in cat_cols:
    df[col] = le.fit_transform(df[col])

df.to_csv('folder_with_data/dataprep.csv')

# --------------- Step 4: Perform Exploratory Data Analysis (EDA) ---------------
# Plot distributions of numerical features
df[num_cols].hist(figsize=(10, 6), bins=20)
plt.show()

# Boxplots to detect outliers
plt.figure(figsize=(10, 6))
sns.boxplot(data=df[num_cols])
plt.xticks(rotation=90)
plt.title("Outlier Detection")
plt.show()

# Churn Rate Visualization
plt.figure(figsize=(5, 4))
sns.countplot(x="Churn", data=df)
plt.title("Churn Distribution")
plt.show()