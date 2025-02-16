import pandas as pd
import numpy as np
import pickle
import time
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
import math
import os

# Ensure the file exists
file_path = r'api/clean_dataset.pkl'
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File {file_path} does not exist.")

# Load the dataset with error handling
try:
    df = pickle.load(open(file_path, 'rb'))
except pickle.UnpicklingError:
    raise ValueError("Error unpickling file.")
except Exception as e:
    raise ValueError(f"Unexpected error occurred: {str(e)}")

# Ensure 'price' column exists
if 'price' not in df.columns:
    raise ValueError("The dataset does not contain the 'price' column.")

# Split the dataset
try:
    x_train, x_test, y_train, y_test = train_test_split(df.drop('price', axis=1), df['price'], test_size=0.1)
except KeyError as e:
    raise ValueError(f"Key error: {str(e)}")
except ValueError as e:
    raise ValueError(f"Value error: {str(e)}")
except Exception as e:
    raise ValueError(f"Unexpected error occurred: {str(e)}")

# Train the model
model = Lasso(alpha=1)
try:
    model.fit(x_train, y_train)
except ValueError as e:
    raise ValueError(f"Model fitting error: {str(e)}")
except Exception as e:
    raise ValueError(f"Unexpected error occurred: {str(e)}")

def predict_price(location, total_sqft, bath, bhk):
    if location not in df.columns:
        raise ValueError(f"Location '{location}' not found in dataset.")
    
    i = list(df.drop('price', axis=1).columns).index(location)
    x = np.zeros(len(list(df.drop('price', axis=1).columns)))
    x[0] = bhk
    x[1] = total_sqft
    x[2] = bath
    x[i] = 1
    
    try:
        prediction = model.predict([x])
    except ValueError as e:
        raise ValueError(f"Prediction error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error occurred: {str(e)}")
    
    return (math.ceil(prediction[0]) * 100000)

