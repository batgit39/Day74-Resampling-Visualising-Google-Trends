#!/usr/bin/env python
# coding: utf-8

# # Introduction

# Google Trends gives us an estimate of search volume. Let's explore if search popularity relates to other kinds of data. Perhaps there are patterns in Google's search volume and the price of Bitcoin or a hot stock like Tesla. Perhaps search volume for the term "Unemployment Benefits" can tell us something about the actual unemployment rate? 
# 
# Data Sources: <br>
# <ul>
# <li> <a href="https://fred.stlouisfed.org/series/UNRATE/">Unemployment Rate from FRED</a></li>
# <li> <a href="https://trends.google.com/trends/explore">Google Trends</a> </li>  
# <li> <a href="https://finance.yahoo.com/quote/TSLA/history?p=TSLA">Yahoo Finance for Tesla Stock Price</a> </li>    
# <li> <a href="https://finance.yahoo.com/quote/BTC-USD/history?p=BTC-USD">Yahoo Finance for Bitcoin Stock Price</a> </li>
# </ul>

# # Import Statements

# In[50]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# # Read the Data
# 
# Download and add the .csv files to the same folder as your notebook.

# In[3]:


df_tesla = pd.read_csv('TESLA Search Trend vs Price.csv')

df_btc_search = pd.read_csv('Bitcoin Search Trend.csv')
df_btc_price = pd.read_csv('Daily Bitcoin Price.csv')

df_unemployment = pd.read_csv('UE Benefits Search vs UE Rate 2004-19.csv')


# # Data Exploration

# ### Tesla

# **Challenge**: <br>
# <ul>
# <li>What are the shapes of the dataframes? </li>
# <li>How many rows and columns? </li>
# <li>What are the column names? </li>
# <li>Complete the f-string to show the largest/smallest number in the search data column</li> 
# <li>Try the <code>.describe()</code> function to see some useful descriptive statistics</li>
# <li>What is the periodicity of the time series data (daily, weekly, monthly)? </li>
# <li>What does a value of 100 in the Google Trend search popularity actually mean?</li>
# </ul>

# In[4]:


df_tesla.shape


# In[5]:


df_tesla.describe()


# In[6]:


df_tesla.columns


# In[7]:


largest_value = df_tesla['TSLA_WEB_SEARCH'].max()
smallest_value = df_tesla['TSLA_WEB_SEARCH'].min()


# In[8]:


print(f'Largest value for Tesla in Web Search: {largest_value}')
print(f'Smallest value for Tesla in Web Search: {smallest_value}')


# ### Unemployment Data

# In[9]:


df_unemployment.describe


# In[11]:


print('Largest value for "Unemployemnt Benefits" '
      f'in Web Search: {df_unemployment["UE_BENEFITS_WEB_SEARCH"].max()}')


# ### Bitcoin

# In[12]:


df_btc_search.describe


# In[13]:


largest_btc = df_btc_search['BTC_NEWS_SEARCH'].max()


# In[14]:


print(f'largest BTC News Search: {largest_btc}')


# # Data Cleaning

# ### Check for Missing Values

# **Challenge**: Are there any missing values in any of the dataframes? If so, which row/rows have missing values? How many missing values are there?

# In[18]:


print(f'Missing values for Tesla?: {df_tesla.isna().values.any()}')
print(f'Missing values for U/E?: {df_unemployment.isna().values.any()}')
print(f'Missing values for BTC Search?: {df_btc_search.isna().values.any()}')


# In[19]:


print(f'Missing values for BTC price?: {df_btc_price.isna().values.any()}')


# In[21]:


print(f'Number of missing values: {df_btc_price.isna().values.sum()}')


# In[22]:


df_btc_price[df_btc_price.CLOSE.isna()]


# **Challenge**: Remove any missing values that you found. 

# In[23]:


df_btc_price.dropna(inplace=True)


# ### Convert Strings to DateTime Objects

# **Challenge**: Check the data type of the entries in the DataFrame MONTH or DATE columns. Convert any strings in to Datetime objects. Do this for all 4 DataFrames. Double check if your type conversion was successful.

# In[25]:


type(df_tesla.MONTH[0])


# In[26]:


df_tesla.MONTH = pd.to_datetime(df_tesla.MONTH)
df_btc_search.MONTH = pd.to_datetime(df_btc_search.MONTH)
df_unemployment.MONTH = pd.to_datetime(df_unemployment.MONTH)
df_btc_price.DATE = pd.to_datetime(df_btc_price.DATE)


# In[27]:


type(df_tesla.MONTH[0])


# ### Converting from Daily to Monthly Data
# 
# [Pandas .resample() documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html) <br>

# In[32]:


df_btc_price


# In[29]:


df_btc_monthly = df_btc_price.resample('M', on='DATE').last()


# In[31]:


df_btc_monthly = df_btc_price.resample('M', on='DATE').mean()


# In[33]:


df_btc_monthly


# # Data Visualisation

# ### Notebook Formatting & Style Helpers

# In[51]:


# Create locators for ticks on the time axis
years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')


# In[21]:


# Register date converters to avoid warning messages


# ### Tesla Stock Price v.s. Search Volume

# **Challenge:** Plot the Tesla stock price against the Tesla search volume using a line chart and two different axes. Label one axis 'TSLA Stock Price' and the other 'Search Trend'. 

# In[66]:


ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('TSLA Stock Price', color = 'r')
ax2.set_ylabel('Search Trend', color = 'skyblue')

ax1.set_ylim([0, 600])
ax1.set_xlim([df_tesla.MONTH.min(), df_tesla.MONTH.max()])

ax1.plot(df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE, color = 'r', linewidth = 3)
ax2.plot(df_tesla.MONTH, df_tesla.TSLA_WEB_SEARCH, color = 'skyblue', linewidth = 3)


# **Challenge**: Add colours to style the chart. This will help differentiate the two lines and the axis labels. Try using one of the blue [colour names](https://matplotlib.org/3.1.1/gallery/color/named_colors.html) for the search volume and a HEX code for a red colour for the stock price. 
# <br>
# <br>
# Hint: you can colour both the [axis labels](https://matplotlib.org/3.3.2/api/text_api.html#matplotlib.text.Text) and the [lines](https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D) on the chart using keyword arguments (kwargs).  

# In[69]:


ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('TSLA Stock Price', color = '#ff0000')
ax2.set_ylabel('Search Trend', color = 'skyblue')

ax1.set_ylim([0, 600])
ax1.set_xlim([df_tesla.MONTH.min(), df_tesla.MONTH.max()])

ax1.plot(df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE, color = '#ff0000', linewidth = 3)
ax2.plot(df_tesla.MONTH, df_tesla.TSLA_WEB_SEARCH, color = 'skyblue', linewidth = 3)


# **Challenge**: Make the chart larger and easier to read. 
# 1. Increase the figure size (e.g., to 14 by 8). 
# 2. Increase the font sizes for the labels and the ticks on the x-axis to 14. 
# 3. Rotate the text on the x-axis by 45 degrees. 
# 4. Make the lines on the chart thicker. 
# 5. Add a title that reads 'Tesla Web Search vs Price'
# 6. Keep the chart looking sharp by changing the dots-per-inch or [DPI value](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.figure.html). 
# 7. Set minimum and maximum values for the y and x axis. Hint: check out methods like [set_xlim()](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.set_xlim.html). 
# 8. Finally use [plt.show()](https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.show.html) to display the chart below the cell instead of relying on the automatic notebook output.

# In[ ]:


lt.figure(figsize=(14,8))
plt.title('Tesla Web Search vs Price', fontsize=18)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('TSLA Stock Price', color = 'r')
ax2.set_ylabel('Search Trend', color = 'skyblue')

ax1.set_ylim([0, 600])
ax1.set_xlim([df_tesla.MONTH.min(), df_tesla.MONTH.max()])

ax1.plot(df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE, color = 'r', linewidth = 3)
ax2.plot(df_tesla.MONTH, df_tesla.TSLA_WEB_SEARCH, color = 'skyblue', linewidth = 3)

plt.show()


# How to add tick formatting for dates on the x-axis. 

# In[ ]:


lt.figure(figsize=(14,8))
plt.title('Tesla Web Search vs Price', fontsize=18)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('TSLA Stock Price', color = 'r')
ax2.set_ylabel('Search Trend', color = 'skyblue')

ax1.set_ylim([0, 600])
ax1.set_xlim([df_tesla.MONTH.min(), df_tesla.MONTH.max()])

ax1.plot(df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE, color = 'r', linewidth = 3)
ax2.plot(df_tesla.MONTH, df_tesla.TSLA_WEB_SEARCH, color = 'skyblue', linewidth = 3)

# format the ticks
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

plt.show()


# ### Bitcoin (BTC) Price v.s. Search Volume

# **Challenge**: Create the same chart for the Bitcoin Prices vs. Search volumes. <br>
# 1. Modify the chart title to read 'Bitcoin News Search vs Resampled Price' <br>
# 2. Change the y-axis label to 'BTC Price' <br>
# 3. Change the y- and x-axis limits to improve the appearance <br>
# 4. Investigate the [linestyles](https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.plot.html ) to make the BTC price a dashed line <br>
# 5. Investigate the [marker types](https://matplotlib.org/3.2.1/api/markers_api.html) to make the search datapoints little circles <br>
# 6. Were big increases in searches for Bitcoin accompanied by big increases in the price?

# In[72]:


plt.figure(figsize=(14,8), dpi=120)

plt.title('Bitcoin News Search vs Resampled Price', fontsize=18)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('BTC Price', color='#F08F2E', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.set_ylim(bottom=0, top=15000)
ax1.set_xlim([df_btc_monthly.index.min(), df_btc_monthly.index.max()])

# Experiment with the linestyle and markers
ax1.plot(df_btc_monthly.index, df_btc_monthly.CLOSE, color='#F08F2E', linewidth=3, linestyle='--')
ax2.plot(df_btc_monthly.index, df_btc_search.BTC_NEWS_SEARCH, color='skyblue', linewidth=3, marker='o')

plt.show()


# In[ ]:





# ### Unemployement Benefits Search vs. Actual Unemployment in the U.S.

# **Challenge** Plot the search for "unemployment benefits" against the unemployment rate. 
# 1. Change the title to: Monthly Search of "Unemployment Benefits" in the U.S. vs the U/E Rate <br>
# 2. Change the y-axis label to: FRED U/E Rate <br>
# 3. Change the axis limits <br>
# 4. Add a grey [grid](https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.grid.html) to the chart to better see the years and the U/E rate values. Use dashes for the line style<br> 
# 5. Can you discern any seasonality in the searches? Is there a pattern? 

# In[81]:


plt.figure(figsize=(14,8), dpi=120)
plt.title('Monthly Search of "Unemployment Benefits" in the U.S. vs the U/E Rate', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)
 
ax1 = plt.gca()
ax2 = ax1.twinx()
 
ax1.set_ylabel('FRED U/E Rate', color='green', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.set_ylim(bottom=3, top=10.5)
ax1.set_xlim([df_unemployment.MONTH.min(), df_unemployment.MONTH.max()])

ax1.grid(color='grey', linestyle='--')
# Experiment with the linestyle and markers
ax1.plot(df_unemployment.MONTH, df_unemployment.UNRATE, color='green', linewidth=3, linestyle='--')
ax2.plot(df_unemployment.MONTH, df_unemployment.UE_BENEFITS_WEB_SEARCH, color='skyblue', linewidth=3, marker='o')

plt.show()


# **Challenge**: Calculate the 3-month or 6-month rolling average for the web searches. Plot the 6-month rolling average search data against the actual unemployment. What do you see in the chart? Which line moves first?
# 

# In[87]:


plt.figure(figsize=(14,8), dpi=120)
plt.title('Monthly Search of "Unemployment Benefits" in the U.S. vs the U/E Rate', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)
 
ax1 = plt.gca()
ax2 = ax1.twinx()
 
ax1.set_ylabel('FRED U/E Rate', color='green', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.set_ylim(bottom=3, top=10.5)
ax1.set_xlim([df_unemployment.MONTH.min(), df_unemployment.MONTH.max()])

roll_df = df_unemployment[['UE_BENEFITS_WEB_SEARCH', 'UNRATE']].rolling(window=6).mean()

ax1.grid(color='grey', linestyle='--')
# Experiment with the linestyle and markers
ax1.plot(df_unemployment.MONTH, roll_df.UNRATE, color='green', linewidth=3, linestyle='--')
ax2.plot(df_unemployment.MONTH, roll_df.UE_BENEFITS_WEB_SEARCH, color='skyblue', linewidth=3, marker='o')

plt.show()


# ### Including 2020 in Unemployment Charts

# **Challenge**: Read the data in the 'UE Benefits Search vs UE Rate 2004-20.csv' into a DataFrame. Convert the MONTH column to Pandas Datetime objects and then plot the chart. What do you see?

# In[88]:


df_ue_2020 = pd.read_csv('UE Benefits Search vs UE Rate 2004-20.csv')
df_ue_2020.MONTH = pd.to_datetime(df_ue_2020.MONTH)


# In[90]:


df_ue_2020.columns


# In[92]:


plt.figure(figsize=(14,8), dpi=120)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)
plt.title('Monthly US "Unemployment Benefits" Web Search vs UNRATE incl 2020', fontsize=18)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('FRED U/E Rate', color='purple', fontsize=16)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=16)

ax1.set_xlim([df_ue_2020.MONTH.min(), df_ue_2020.MONTH.max()])

ax1.plot(df_ue_2020.MONTH, df_ue_2020.UNRATE, 'purple', linewidth=3)
ax2.plot(df_ue_2020.MONTH, df_ue_2020.UE_BENEFITS_WEB_SEARCH, 'skyblue', linewidth=3)

plt.show()


# In[ ]:




