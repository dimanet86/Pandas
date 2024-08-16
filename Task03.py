import pandas as pd

df = pd.read_csv("D:\\Capgemini\\Pandas\\archive\\cleaned_airbnb_data.csv")

"""
Analyze Pricing Trends Across Neighborhoods and Room Types
"""
# Use the pivot_table function to create a detailed summary that reveals the average price for different combinations of neighbourhood_group and room_type.

pt = pd.pivot_table(df, values='price', index=df['neighbourhood_group'], columns=df['room_type'], aggfunc='mean')

"""
Prepare Data for In-Depth Metric Analysis
"""
# Transform the dataset from a wide format to a long format using the melt function. This restructuring facilitates more flexible and detailed analysis of key metrics like price and minimum_nights, enabling the identification of trends, outliers, and correlations.

# 1. Let's take subset of cols in df
# 2. As variables let's take 'neighbourhood', 'room_type', 'price_category', 'length_of_stay_category'
melted = df.iloc[:, [5,8,9,10,13,15,16,17]].melt(id_vars=['neighbourhood', 'room_type', 'price_category', 'length_of_stay_category'])

"""
Classify Listings by Availability
"""
# Create a new column availability_status using the apply function, classifying each listing into one of three categories based on the availability_365 column
# "Rarely Available": Listings with fewer than 50 days of availability in a year.
# "Occasionally Available": Listings with availability between 50 and 200 days.
# "Highly Available": Listings with more than 200 days of availability.

def status(x):
    if x < 50:
        return 'Rarely Available'
    elif x >= 50 and x <= 200:
        return 'Occasionally Available'
    elif x > 200:
        return 'Highly Available'
    else:
        return 'NA'

df['availability_status'] = df['availability_365'].apply(status)

# Analyze trends and patterns using the new availability_status column, and investigate potential correlations between availability and other key variables like price, number_of_reviews, and neighbourhood_group to uncover insights that could inform marketing and operational strategies.

# From this we can see, not using correlation or regression, that rooms with lower price is less available through the year
to_analyze = df.groupby(['neighbourhood_group', 'availability_status'])['price'].mean().sort_index()
# This shows almost no correlation between price and number_of_reviews
# although one can see that higher price leads to insignificantly lesser number of reviews
# probably because higher price rooms have less visitors 
num_of_reviews = df[['number_of_reviews', 'price']].corr() 

"""
Descriptive Statistics
"""
# Perform basic descriptive statistics (e.g., mean, median, standard deviation) on numeric columns such as price, minimum_nights, and number_of_reviews to summarize the dataset's central tendencies and variability, which is crucial for understanding overall market dynamics.
df.agg({
    'price': ["min", "max", "median", "std"],
    'minimum_nights': ["min", "max", "median", "std"], 
    'number_of_reviews': ["min", "max", "median", "std"], 
    'reviews_per_month': ["min", "max", "median", "std"], 
    'calculated_host_listings_count': ["min", "max", "median", "std"],
    'availability_365': ["min", "max", "median", "std"]
    })

"""
Time Series Analysis
"""
# Convert and Index Time Data
# Convert the last_review column to a datetime object and set it as the index of the DataFrame to facilitate time-based analyses.
df2 = df.copy()
df2['last_review'] = pd.to_datetime(df2['last_review'], errors='coerce')
df2 = df2[df2['last_review'].notna()] # let's get rid of rows with NaT in last-review cells. 
df2.set_index('last_review', inplace=True)

# Identify Monthly Trends:
# Resample the data to observe monthly trends in the number of reviews and average prices, 
# providing insights into how demand and pricing fluctuate over time.
# Group the data by month to calculate monthly averages 
# and analyze seasonal patterns, enabling better forecasting and strategic planning around peak periods.

# I have combined these tasks into one because in both tasks we are grouping data by month and analyze averages 

# Number of reviews per month grouped by month
# We can't take number of reviews as task requests because 
# this quantity is constant and calculated per particular room
ts = df2['reviews_per_month'].resample('ME').count() 

# Observing seasonal patterns for price
ts = df2[['price']].resample('QE') #
ts.mean()

# After inspecting dataset I concluded that no column fits 
# for time series analysis
# because here we have a set of rooms on airbnb
# and every row corresponds to certain room
# and data for that room doesn't change over time