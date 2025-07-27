import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load and clean data
df = pd.read_csv('carbon_data.csv')
df.columns = df.columns.str.strip()

print("✅ Columns in dataset:", df.columns.tolist())

# Fixed column name
X = df[['Fuel', 'EngineSize', 'Mileage']]
y = df['CO2']

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), ['Fuel'])
    ],
    remainder='passthrough'
)

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

model.fit(X, y)

# Save model
with open('carbon_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Save encoder separately (if needed)
encoder = OneHotEncoder()
encoder.fit(df[['Fuel']])
with open('encoder.pkl', 'wb') as f:
    pickle.dump(encoder, f)

print("✅ Model and encoder saved successfully.")
