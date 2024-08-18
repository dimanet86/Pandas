"""
Practical Task 2: 
"""
import numpy as np
import pandas as pd

def print_grouped_data(gdf, msg=""):
    print(msg)
    print(gdf)

df = pd.read_csv("cleaned_airbnb_data.csv")

"""
Data Selection and Filtering:
"""
# Use .iloc and .loc to select specific rows and columns based on both position and labels.
x = df.iloc[0:4, 0:df.columns.size]
y = df.loc[:, ['price', 'price_category', 'minimum_nights', 'length_of_stay_category']]

# Filter the dataset to include only listings in specific neighborhoods (e.g., Manhattan, Brooklyn).
sunnyside = df[df['neighbourhood'] == 'Sunnyside']
sunnyside.head()
flatbush = df[df['neighbourhood'] == 'Flatbush']
flatbush.head()

# Further filter the dataset to include only listings with a price greater than $100 and a number_of_reviews greater than 10.
mask = (df['price'] > 100) & (df['number_of_reviews'] > 10)
filtered_listings = df[mask]
filtered_listings[['price', 'number_of_reviews']].head()

# Select columns of interest such as neighbourhood_group, price, minimum_nights, number_of_reviews, price_category and availability_365 for further analysis.
df2 = df[['neighbourhood_group', 'neighbourhood', 'price', 'price_category', 'minimum_nights', 'number_of_reviews', 'availability_365', 'length_of_stay_category']]

"""
Aggregation and Grouping
"""
# Group the filtered dataset by neighbourhood_group and price_category to calculate aggregate statistics:
# Calculate the average price and minimum_nights for each group.
groups = df2.groupby(['neighbourhood_group', 'price_category'])

groups['price'].mean().to_frame('Mean price')

# Let's check 'manually' the result above
df[(df['neighbourhood_group'] == 'Bronx') & (df['price_category'] == 'High')]['price'].mean()

# Compute the average number_of_reviews and availability_365 for each group to understand typical 
# review counts and availability within each neighborhood and price category.
groups[['number_of_reviews', 'availability_365']].mean()

"""
Data Sorting and Ranking:
"""
# Sort the data by price in descending order and by number_of_reviews in ascending order.
df2.sort_values(['price', 'number_of_reviews'], ascending=[False, True])

# Create a ranking of neighborhoods based on the total number of listings and the average price.
# by price (the more the higher price)
df.groupby('neighbourhood')['price'].mean().rank().sort_values(ascending=False) 
# by number of reviews (the more the higher number of rooms in neighbourhood)
df.groupby('neighbourhood').size().rank().astype(int).sort_values(ascending=False) 