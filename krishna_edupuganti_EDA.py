import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
customers_file = r'C:\Users\Dell\Downloads\Customers.csv'
products_file = r'C:\Users\Dell\Downloads\Products.csv'
transactions_file = r'C:\Users\Dell\Downloads\Transactions.csv'
customers = pd.read_csv(customers_file)
products = pd.read_csv(products_file)
transactions = pd.read_csv(transactions_file)
# Convert date columns to datetime
customers['SignupDate'] = pd.to_datetime(customers['SignupDate'])
transactions['TransactionDate'] = pd.to_datetime(transactions['TransactionDate'])
# Merge datasets for EDA
transactions_merged = transactions.merge(customers, on='CustomerID', how='left').merge(products,
on='ProductID', how='left')
# Basic statistics
sales_summary = transactions_merged.describe(include='all')
# Aggregated Metrics for EDA
# 1. Total Sales by Region
sales_by_region = transactions_merged.groupby('Region')['TotalValue'].sum().reset_index()
# 2. Top-selling Product Categories
top_categories =
transactions_merged.groupby('Category')['Quantity'].sum().reset_index().sort_values(by='Quantity',
ascending=False)
# 3. Customer Signup Trends Over Time
signup_trends = customers.groupby(customers['SignupDate'].dt.to_period('M')).size()
# 4. Sales Trends Over Time
sales_trends =
transactions_merged.groupby(transactions_merged['TransactionDate'].dt.to_period('M'))['TotalValue
'].sum()
# 5. Average Order Value by Region
aov_by_region = transactions_merged.groupby('Region')['TotalValue'].mean().reset_index()
# Visualizations
plt.figure(figsize=(16, 10))
# Total Sales by Region
plt.subplot(2, 2, 1)
sns.barplot(x='Region', y='TotalValue', data=sales_by_region, palette='viridis')
plt.title('Total Sales by Region')
plt.xticks(rotation=45)
# Top-Selling Product Categories
plt.subplot(2, 2, 2)
sns.barplot(x='Category', y='Quantity', data=top_categories, palette='coolwarm')
plt.title('Top-Selling Product Categories')
plt.xticks(rotation=45)
# Customer Signup Trends
plt.subplot(2, 2, 3)
signup_trends.plot(kind='line', marker='o', color='b')
plt.title('Customer Signup Trends Over Time')
plt.xlabel('Month-Year')
plt.ylabel('Number of Signups')
# Sales Trends Over Time
plt.subplot(2, 2, 4)
sales_trends.plot(kind='line', marker='o', color='g')
plt.title('Sales Trends Over Time')
plt.xlabel('Month-Year')
plt.ylabel('Total Sales')
plt.tight_layout()
plt.show()
# Save visualizations and aggregated data for insights
(sales_by_region, top_categories, signup_trends, sales_trends, aov_by_region)