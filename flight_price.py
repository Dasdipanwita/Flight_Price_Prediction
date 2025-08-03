# Import necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import pickle

# Load the dataset
df = pd.read_excel("Data_Train .xlsx")

# --- Data Cleaning and Preprocessing ---
df.dropna(inplace=True)

# Convert 'Date_of_Journey' to datetime and extract day and month
if 'Date_of_Journey' in df.columns:
    df["Journey_day"] = pd.to_datetime(df['Date_of_Journey'], format="%d/%m/%Y").dt.day
    df["Journey_month"] = pd.to_datetime(df['Date_of_Journey'], format="%d/%m/%Y").dt.month
    df.drop(["Date_of_Journey"], axis=1, inplace=True)

# Extract hour and minute from 'Dep_Time'
if 'Dep_Time' in df.columns:
    df["Dep_hour"] = pd.to_datetime(df["Dep_Time"]).dt.hour
    df["Dep_min"] = pd.to_datetime(df["Dep_Time"]).dt.minute
    df.drop(["Dep_Time"], axis=1, inplace=True)

# Extract hour and minute from 'Arrival_Time'
if 'Arrival_Time' in df.columns:
    df["Arrival_hour"] = pd.to_datetime(df["Arrival_Time"]).dt.hour
    df["Arrival_min"] = pd.to_datetime(df["Arrival_Time"]).dt.minute
    df.drop(["Arrival_Time"], axis=1, inplace=True)

# Process 'Duration'
duration = list(df["Duration"])
for i in range(len(duration)):
    if len(duration[i].split()) != 2:
        if "h" in duration[i]:
            duration[i] = duration[i].strip() + " 0m"
        else:
            duration[i] = "0h " + duration[i]

duration_hours = []
duration_mins = []
for i in range(len(duration)):
    duration_hours.append(int(duration[i].split(sep="h")[0]))
    duration_mins.append(int(duration[i].split(sep="m")[0].split()[-1]))

df["Duration_hours"] = duration_hours
df["Duration_mins"] = duration_mins
df.drop(["Duration"], axis=1, inplace=True)

# --- Handling Categorical Data ---
# One-hot encode nominal data
df = pd.get_dummies(df, columns=['Airline', 'Source', 'Destination'], drop_first=True)

# Label encode ordinal data
df.replace({"non-stop": 0, "1 stop": 1, "2 stops": 2, "3 stops": 3, "4 stops": 4}, inplace=True)

# Drop unnecessary columns
df.drop(["Route", "Additional_Info"], axis=1, inplace=True)

# --- Model Training ---
X = df.drop("Price", axis=1)
y = df["Price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# --- Save the Model ---
with open('flight_price_rf.pkl', 'wb') as f:
    pickle.dump(rf, f)

print("Model saved as flight_price_rf.pkl")