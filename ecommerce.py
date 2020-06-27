#%%
import os
import numpy as np
import pandas as pd
import streamlit as slt

path = '/home/liz/Documents/Programming/Codenation/Data-Science-Online/Semana 3/study/desafio_extra/olist_dataset/'
lst = [file for file in os.listdir(path) if file.endswith('.csv')]
#https://www.kaggle.com/kabure/simple-eda-sales-and-customer-patterns
# %%
df_item = pd.read_csv("./olist_dataset/olist_order_items_dataset.csv")
df_reviews = pd.read_csv("./olist_dataset/olist_order_reviews_dataset.csv")
df_orders = pd.read_csv("./olist_dataset/olist_orders_dataset.csv")
df_products = pd.read_csv("./olist_dataset/olist_products_dataset.csv")
df_geolocation = pd.read_csv("./olist_dataset/olist_geolocation_dataset.csv")
df_sellers = pd.read_csv("./olist_dataset/olist_sellers_dataset.csv")
df_order_pay = pd.read_csv("./olist_dataset/olist_order_payments_dataset.csv")
df_customers = pd.read_csv("./olist_dataset/olist_customers_dataset.csv")
df_category = pd.read_csv("./olist_dataset/product_category_name_translation.csv")


'''

order_id: identify products that are in the same basket.
product_id: identify unique products within the dataset.
customerid: identify unique customers within the dataset. We usually don't look that much to customers, that is because Olist sells through marketplaces and we don't have to worry about customer acquisition and retention. But it is possible to create a customerid from their document numbers.
seller_id: identify unique sellers within the dataset. In our business model multiple sellers might fulfill an order. So identifying which seller fulfilled the order might be useful as well.
'''
# %%
# Merging

df_train = df_orders.merge(df_item, on='order_id', how='left')
df_train = df_train.merge(df_order_pay, on='order_id', how='outer', validate='m:m')
df_train = df_train.merge(df_reviews, on='order_id', how='outer')
df_train = df_train.merge(df_products, on='product_id', how='outer')
df_train = df_train.merge(df_customers, on='customer_id', how='outer')
df_train = df_train.merge(df_sellers, on='seller_id', how='outer')

#%%
df_train.to_csv('./olist_dataset_merge.csv')

#%%
# Trying my merge
dfm = pd.merge(df_item, df_reviews, on='order_id')