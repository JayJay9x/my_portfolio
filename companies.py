# -*- coding: utf-8 -*-
"""companies.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CXiM61JWmgYEGk4OXsjeAMVp-UAXp50c

Making investing firm by diving in the dataset of Unicorn Companies.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

companies = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Unicorn_Companies_project/Unicorn_Companies.csv')

# Let see what we have!
companies.head()

# More detail.
companies.info()
companies.shape

# Date Joined to datetime.
companies['Date Joined'] = pd.to_datetime(companies['Date Joined'])
# Any duplicated record here?
companies.duplicated().sum()

"""There are no need to drop_duplicates right!

Let begin the EDA journey!
"""

# Discover the unicorn companies history.
companies['Year Founded'].sort_values().value_counts()
sns.histplot(companies['Year Founded'])
plt.title('History of Unicorn Companies')
plt.show()

"""I have the statement that the old comapanies have the less chance to become Unicorn."""

''' To make deeper understanding in the route of Unicorn companies,
I will consider how long it takes to become Unicorn of each Insdustry.'''

companies['Year To Join'] = companies['Date Joined'].dt.year - companies['Year Founded']
route_to_unicorn = companies.groupby('Industry')['Year To Join'].mean().round(2).sort_values(ascending=True).reset_index()

# prompt: convert the currency as B to billion in Valuation and M to Million in Funding

def convert_currency(val):
  """Converts currency values from 'B' to billion and 'M' to million."""
  if isinstance(val, str):
    if val.endswith('B'):
      return float(int(val[1:-1])) * 1000000000
    elif val.endswith('M'):
      return float(int(val[1:-1])) * 1000000
    else:
      return 0
  return val


companies['Valuation'] = companies['Valuation'].apply(convert_currency).astype(float)
companies['Funding'] = companies['Funding'].apply(convert_currency).astype(float)
companies['Profit Returns'] = companies['Valuation'] - companies['Funding']
companies

ROI_unicorn = companies.groupby('Industry')['Profit Returns'].mean().round(2).sort_values(ascending=True).reset_index()
result_table = pd.merge(route_to_unicorn, ROI_unicorn, on='Industry', how='left')
result_table

# The average time and ammount for those investing firm
avg_investing = result_table.describe()
avg_investing

"""Combines a bar chart and a line chart to analyze Profit Returns by Year To Join, allowing for both detailed comparison and trend analysis along Industry."""

import altair as alt

# Create the bar chart with tooltip and industry label
bar_chart = alt.Chart(result_table).mark_bar().encode(
    x=alt.X('Year To Join', title='Year To Join'),
    y=alt.Y('Profit Returns', title='Profit Returns'),
    tooltip=['Industry', 'Year To Join', 'Profit Returns']
)

# Add Industry label on each bar
text = bar_chart.mark_text(
    align='center',
    baseline='bottom',
    dy=-10,  # Adjust vertical position of the label
    angle=45  # Rotate label by 45 degrees
).encode(
    text='Industry'
)

# Create the line chart showing average Profit Returns by Year To Join
line_chart = alt.Chart(avg_investing).mark_line(color='red').encode(
    x='Year To Join',
    y='Profit Returns',
    tooltip=['Year To Join', 'Profit Returns']
)

# Combine bar chart and line chart
combined_chart = (bar_chart + text + line_chart).properties(
    width=1000,
    height=300,
    title="Profit Returns by Year To Join"
)

combined_chart

"""*Summary*

This project analyzes the dataset of Unicorn Companies to identify potential investment opportunities.

**Key aspects of the project:**

1. **Data Exploration & Preprocessing:**
   - Loads the dataset of Unicorn Companies.
   - Cleans the data by converting 'Date Joined' to datetime and handling potential duplicates.
   - Explores the history of Unicorn Companies through the 'Year Founded' distribution.


2. **Analyzing Investment Potential:**
   - Calculates the "Year To Join" (the time it takes for a company to become a Unicorn).
   - Groups companies by Industry and calculates the average "Year To Join" and "Profit Returns" (Valuation - Funding).
   - Creates a table that combines both average "Year To Join" and "Profit Returns" by industry.

3. **Visualization & Insights:**
   - Uses Altair to generate a combined chart with bar chart and line chart.
   - Bar chart analyzes the Profit Returns by Year To Join, allowing for comparison across Industries.
   - Line chart shows the average Profit Returns by Year To Join, revealing any trends or patterns in the data.
   -  It aims to identify industries with shorter routes to unicorn status and potentially high profit returns, providing valuable insights for investment firms.


**Overall, the project aims to provide a data-driven approach to selecting promising industries and companies for investment, leveraging the insights gained from analyzing the historical data of Unicorn Companies.**

"""