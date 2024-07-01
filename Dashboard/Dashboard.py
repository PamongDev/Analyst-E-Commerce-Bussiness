from matplotlib.font_manager import FontManager
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import streamlit as st
from datetime import datetime

# arguments :
# grafik yang dibuat
# 1. 

def create_sum_customer_seller(df):
    sum_seller_df = df['seller_id'].nunique()
    sum_customer_df = df['customer_id'].nunique()
    return sum_customer_df, sum_seller_df

def create_sum_product_order_price(df):
    sum_product = df['product_id'].nunique()
    sum_order = df['order_id'].nunique()
    sum_price = df['price'].sum()
    return sum_product ,sum_order, sum_price

def create_order_distribution(df):
    persebaran_kota = df.groupby(['customer_city', 'seller_city']).agg({
    'order_id' : 'nunique',
    }).sort_values('order_id',ascending=False).reset_index().head(10)
    distribusi_list = []
    
    for customer, seller in zip(persebaran_kota['customer_city'],
                                    persebaran_kota['seller_city']):
        distribusi = f"{customer} - {seller}"
        distribusi_list.append(distribusi)
    
    persebaran_kota.rename(columns={
        'order_id' : 'order_count'
    }, inplace=True)

    persebaran_kota['distribusi'] = distribusi_list

    persebaran_negara = df.groupby(['customer_state', 'seller_state']).agg({
    'order_id' : 'nunique',
    }).sort_values('order_id',ascending=False).reset_index().head(10)
    distribusi_list = []
    
    for customer, seller in zip(persebaran_negara['customer_state'],
                                    persebaran_negara['seller_state']):
        distribusi = f"{customer} - {seller}"
        distribusi_list.append(distribusi)
    
    persebaran_negara['distribusi'] = distribusi_list
    persebaran_negara.rename(columns={
        'order_id' : 'order_count'
    }, inplace=True)
    return persebaran_kota, persebaran_negara

def create_order_development(df):
    penjualan = df.copy()   
    output_penjualan = penjualan.groupby('order_purchase_timestamp').agg({
    'order_id' : 'nunique',
    }).sort_values('order_purchase_timestamp', ascending=False).head(31)
    output_penjualan.rename(columns={
        'order_id' : 'order_count'
    }, inplace=True)
    return output_penjualan.sort_values('order_purchase_timestamp',ascending=True)

def create_product_score(df):
    df['review_score'] = df['review_score'].astype('int')
    product_score = df.groupby('product_category_name').agg({
        'review_score' :  'mean'
    }).sort_values('review_score', ascending=False).reset_index().head(10)

    product_score.rename(columns={
        'product_category_name' : 'product_category'
    }, inplace=True)
    return product_score

def create_delivery_status(df):
    delivery_status = df.groupby('delivery_status').agg({
    'order_id' : 'nunique',
    })

    delivery_status.rename(columns={
        'order_id' : 'order_count'
    }, inplace=True)

    return delivery_status
def format_number(number):
    return f"{number:,}".replace(",", ".")

data = pd.read_csv('Dashboard/all_df_lite.csv.gz', compression='gzip')
tanggal1, tanggal2 = st.columns(2)
min_date = datetime(2016, 9, 15)
max_date = datetime(2018, 1, 1)
data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])
with tanggal1:
    start = st.date_input(
        'Pilih tanggal awal:',
        value=min_date, min_value=min_date, max_value=max_date)
    
with tanggal2:
    ends = st.date_input(
        'Pilih tanggal akhir:',
        value=max_date, min_value=min_date, max_value=max_date)

if start > ends:
    st.error('Tanggal mulai tidak boleh lebih besar dari tanggal akhir')
else:
    data = data[(data['order_purchase_timestamp'] >= pd.to_datetime(start)) & (data['order_purchase_timestamp'] <= pd.to_datetime(ends))]

sum_customer, sum_seller = create_sum_customer_seller(data)
sum_product, sum_order, sum_price = create_sum_product_order_price(data)
distribution_city, distribution_state = create_order_distribution(data)
order_development = create_order_development(data)
top_review_score = create_product_score(data)
delivery_status = create_delivery_status(data)


st.title('Dashboard Shopmi')
st.write('##### By Muhamad Fahmi Ammar')
st.write("Dataset yang digunakan : [E-commerce Dataset](https://drive.google.com/file/d/1MsAjPM7oKtVfJL_wRp1qmCajtSG1mdcK/view)")
st.write('___')
col1, col2, col3 = st.columns(3)

with col1:
    st.metric('Total Products', value=format_number(sum_product))
with col2:
    st.metric('Total Orders', value=format_number(sum_order))
with col3:
    st.metric('Total Prices', value=f"${format_number(sum_price)}")

col4, col5, _ = st.columns(3)

with col4:
    st.metric('Total Customers', value=format_number(sum_customer))
with col5:
    st.metric('Total Sellers', value=format_number(sum_seller))

st.write('___')
st.write('### 10 Cities with the Highest Orders')
fig1, ax1 = plt.subplots(figsize=(10,6))
bars = ax1.barh(np.arange(len(distribution_city['distribusi'])), distribution_city['order_count'], tick_label=distribution_city['distribusi'])
bars[0].set_color('red')
ax1.set_xlabel('Customer City - Seller City', fontsize = 14)
ax1.set_ylabel('Order Count', fontsize = 14)
# ax1.set_title('', fontsize = 16)
st.pyplot(fig1)

st.write('___')
st.write('### 10 States with the Highest Orders')
fig2, ax2 = plt.subplots(figsize=(10,6))
bars1 = ax2.barh(np.arange(len(distribution_state['distribusi'])), distribution_state['order_count'], tick_label=distribution_state['distribusi'])
bars1[0].set_color('red')
ax2.set_xlabel('Customer State - Seller State', fontsize = 14)
ax2.set_ylabel('Order Count', fontsize = 14)
# ax1.set_title('', fontsize = 16)
st.pyplot(fig2)

st.write('___')
st.write('### Order Development in the Last Month')
fig3, ax3 = plt.subplots(figsize=(10,5))
ax3.plot(order_development.index, order_development['order_count'], marker='o', linewidth=2, color='red')
# bars1[0].set_color('red')
ax3.set_xlabel('Order Date', fontsize = 14)
ax3.set_ylabel('Order Count', fontsize = 14)
ax3.set_xticks(order_development.index[::6])
st.pyplot(fig3)

st.write('___')
st.write('### 10 Category Product with HIgh review Score')
fig4, ax4 = plt.subplots(figsize=(10,6))
bars3 = ax4.barh(top_review_score['product_category'], top_review_score['review_score'], tick_label=top_review_score['product_category'])
bars3[0].set_color('red')
ax4.set_xlabel('Category Product', fontsize = 14)
ax4.set_ylabel('Review Score', fontsize = 14)
st.pyplot(fig4)

st.write('___')
st.write('### Delivery Status')
fig5, ax5 = plt.subplots(figsize=(10,6))
explode = (0.3, 0, 0)  
colors = ['gold', 'yellowgreen', 'lightcoral']

_, texts, auto = ax5.pie(delivery_status['order_count'], explode=explode, colors = colors,
       autopct='%1.1f%%', shadow=False)

for text in texts:
    text.set_color('red')
    text.set_fontsize(20)
    
auto[0].set_fontsize(20)
auto[1].set_fontsize(15)
auto[2].set_fontsize(15)

ax5.legend(delivery_status.index, loc='lower right')

st.pyplot(fig5)
st.caption('Copyright © Dicoding Project Python Analyst 2024')
