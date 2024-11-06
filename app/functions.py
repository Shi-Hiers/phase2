import pandas as pd
import matplotlib.pyplot as plt

def calculate_total_sales_by_region(df):
    # Group by region_name for total sales calculation
    total_sales = df.groupby('region_name').agg({'monthly_amount': 'sum'}).reset_index()
    return total_sales


def analyze_monthly_sales_trends(df):
    df['date'] = pd.to_datetime(df['date'])
    return df.groupby(df['date'].dt.to_period('M'))['monthly_amount'].sum().reset_index()

def get_top_performing_region(df):
    # Find the top region by total sales
    top_region = df.groupby('region')['monthly_amount'].sum().idxmax()
    total_sales = df.groupby('region')['monthly_amount'].sum().max()

    # Fetch the region_name for the top region
    region_name = df[df['region'] == top_region]['region_name'].iloc[0]

    return {'region_name': region_name, 'total_sales': total_sales}

def create_total_sales_chart(df):
    plt.figure(figsize=(10, 6))
    total_sales = df.groupby('region')['monthly_amount'].sum().reset_index()
    plt.bar(total_sales['region'], total_sales['monthly_amount'])
    plt.xlabel('Region')
    plt.ylabel('Total Sales Amount')
    plt.title('Total Sales by Region')
    plt.xticks(rotation=45)
