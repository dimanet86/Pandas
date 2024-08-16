"""
Practical Task 1: Basic Data Exploration and Cleaning with Pandas
"""
import pandas as pd
import numpy as np

"""
Data Loading and Initial Inspection
"""

df = pd.read_csv("D:\\Capgemini\\Pandas\\archive\\AB_NYC_2019.csv")

df.head()

df.info()

"""
Handling Missing Values
"""
# Identify columns with missing values and count the number of missing entries per column.
missing_vals_cols = list(df.count()[df.count() < df.index.size].index) # obtaining list of cols containing missing values

# Handle missing values in the name, host_name, and last_review columns:
# For name and host_name, fill missing values with the string "Unknown".
df['name'].fillna(value='Unknown', inplace=True)
df['host_name'].fillna(value='Unknown', inplace=True)

# For last_review, fill missing values with a special value “NaT". “NaT" stands for Not a Time.
df['last_review'].fillna(value=pd.NaT, inplace=True)

"""
Data Transformation
"""
# Categorize Listings by Price Range:
# Create a new column price_category that categorizes listings into different price ranges, such as Low, Medium, High, 
# based on defined thresholds (e.g., Low: price < $100, Medium: $100 <= price < $300, High: price >= $300).
df['price_category'] = df['price'].apply(lambda x: 'Low' if x <= 100 else 'Medium' if x > 100 and x <= 300 else 'High')

# Create a length_of_stay_category column:
# Categorize listings based on their minimum_nights into short-term, medium-term, and long-term stays.
# For example, short-term might be minimum_nights <= 3, medium-term minimum_nights between 4 and 14, and long-term minimum_nights > 14.
df['length_of_stay_category'] = df['minimum_nights'].apply(lambda x: 'short-term' if x <= 3 else 'medium-term' if x > 3 and x <= 14 else 'long-term')

# Removing rows with price value equals to 0
df = df[df['price'] > 0]

# Saving cleaned dataset 
df.to_csv("D:\\Capgemini\\Pandas\\archive\\cleaned_airbnb_data.csv", index=False)