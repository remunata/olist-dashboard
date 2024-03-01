import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency


def create_daily_orders_df(df):
    daily_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
        'order_id': 'nunique',
        'price': 'sum',
    })
    daily_df.reset_index()
    daily_df.rename(columns={'order_id': 'total_orders', 'price': 'total_sales'}, inplace=True)
    return daily_df


def create_product_performance_df(df):
    products_df = df.groupby('product_category_name').agg({
        'order_id': 'nunique',
        'price': 'sum'
    })
    products_df.reset_index(inplace=True)
    products_df.rename(columns={'order_id': 'total_orders', 'price': 'total_sales'}, inplace=True)
    return products_df


# Load data
order_products_df = pd.read_csv('order_products.csv', parse_dates=['order_purchase_timestamp'])
order_products_df.sort_values(by='order_purchase_timestamp', inplace=True)
order_products_df.reset_index()

min_date = order_products_df['order_purchase_timestamp'].min()
max_date = order_products_df['order_purchase_timestamp'].max()

with st.sidebar:
    st.image('olist_logo.png')

    start_date, end_date = st.date_input(
        label="Select date range",
        min_value=min_date,
        max_value=max_date,
        value=[max_date - pd.DateOffset(days=10), max_date]
    )

order_products_df = order_products_df[
    (order_products_df['order_purchase_timestamp'] >= pd.to_datetime(start_date)) &
    (order_products_df['order_purchase_timestamp'] <= pd.to_datetime(end_date))
    ]

daily_orders_df = create_daily_orders_df(order_products_df)
product_performance_df = create_product_performance_df(order_products_df)

st.header('Olist Business Intelligence Dashboard')

# Daily Orders
st.subheader('Daily Orders and Sales')

col1, col2 = st.columns(2)

with col1:
    st.metric('Total Orders', value=daily_orders_df['total_orders'].sum())

with col2:
    total_sales = format_currency(daily_orders_df['total_sales'].sum(), "BRL", locale="pt_BR")
    st.metric('Total Sales', value=total_sales)

fig, ax = plt.subplots(figsize=(15, 7))
ax.plot(
    daily_orders_df.index,
    daily_orders_df['total_orders'],
    marker='o',
    linewidth=2
)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
ax.set_title('Daily Orders', fontsize=25)

st.pyplot(fig)

fig, ax = plt.subplots(figsize=(15, 7))
ax.plot(
    daily_orders_df.index,
    daily_orders_df['total_sales'],
    marker='o',
    linewidth=2
)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
ax.set_title('Daily Sales', fontsize=25)

st.pyplot(fig)

# Product Performance
st.subheader('Best & Worst Product Performance by Total Orders')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(y='product_category_name', x='total_orders',
            data=product_performance_df.sort_values(by='total_orders', ascending=False).head(5),
            ax=ax[0], palette='viridis')
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)
ax[0].yaxis.set_label_position("left")
ax[0].yaxis.tick_left()
ax[0].tick_params(axis='x', labelsize=30)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].set_title("Top 5 Best Selling Product Categories", fontsize=40)

sns.barplot(y='product_category_name', x='total_orders',
            data=product_performance_df.sort_values(by='total_orders', ascending=True).head(5),
            ax=ax[1], palette='viridis')
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='x', labelsize=30)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].set_title("Top 5 Best Selling Product Categories", fontsize=40)

st.pyplot(fig)

st.subheader('Best & Worst Product Performance by Total Sales')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(y='product_category_name', x='total_sales',
            data=product_performance_df.sort_values(by='total_sales', ascending=False).head(5),
            ax=ax[0], palette='viridis')
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)
ax[0].yaxis.set_label_position("left")
ax[0].yaxis.tick_left()
ax[0].tick_params(axis='x', labelsize=30)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].set_title("Top 5 Best Selling Product Categories", fontsize=40)

sns.barplot(y='product_category_name', x='total_orders',
            data=product_performance_df.sort_values(by='total_sales', ascending=True).head(5),
            ax=ax[1], palette='viridis')
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='x', labelsize=30)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].set_title("Top 5 Best Selling Product Categories", fontsize=40)

st.pyplot(fig)