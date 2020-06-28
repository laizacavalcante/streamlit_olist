import pandas as pd
import streamlit as st
import plotly.express as px

# Boxplot not correctly working


def main():
    # -----------------------------
    # Initial description
    st.image('./dataset-cover.png', width=900)
    st.title('Analysis of e-commerce dataset')
    st.markdown("""Here, I will introduce some basic descriptive analysis of
                the Olist brazilian e-commerce dataset. This dataset contains 
                more than 110K orders from 2016 to 2018 with detailed costumer 
                transactions. The dataset consists of **9 files**, which 
                describe orders, products and their categories, user reviews, 
                information about delivery estimate date, payment method, 
                geolocation, and much, much more.    \n """)

    st.markdown("""All datasets are available 
                on [Kaggle](https://www.kaggle.com/olistbr/brazilian-ecommerce)
                .""")

    st.markdown("""Initially, I will start using **4 datasets**: 
                *Items, Orders, Products description and Payment.*""")

    st.markdown("Here, I will cover some basic info about the datasets "
                "(number of orders, how many variables are available, possible"
                " payment methods, etc.) and explore some data visualization"
                " (histogram, bar plot, and boxplot).  \n So, let's start!")

    # -----------------------------
    # Import dataset
    st.header("**Dataset investigation**")
    st.markdown("Let's take a look on data...")

    items = pd.read_csv("./olist_dataset/olist_order_items_dataset.csv")
    orders = pd.read_csv("./olist_dataset/olist_orders_dataset.csv")
    products = pd.read_csv("./olist_dataset/olist_products_dataset.csv")
    payment = pd.read_csv("./olist_dataset/olist_order_payments_dataset.csv")

    # Slider for dataframe.head
    slider_bar = st.slider(label='Select a number of rows to take a look on datasets?',
                           min_value=1, max_value=10)

    st.markdown('**Items**')
    st.markdown("""This dataset describes the relationship among orders, sellers,
                order  price, shipping cost and date.""")
    st.dataframe(items.head(slider_bar))

    st.markdown('**Orders **')
    st.markdown("""Here, We have info about order status: purchased time,
                order status, if was already shipped, for example...""")
    st.dataframe(orders.head(slider_bar))

    st.markdown('**Products**')
    st.markdown("""Products dataset describes products by categories, weight, 
                and dimensions""")
    st.dataframe(products.head(slider_bar))

    st.markdown('**Payment**')
    st.markdown("""Last but not least, this dataset shows payment value and 
                method.""")
    st.dataframe(payment.head(slider_bar))

    # Columns description
    add_info = st.checkbox('Want additional info about variables?')
    if add_info:
        st.markdown("""Basically, keep in mind that with these variables bellow,
                    we can track orders along the datasets: \n"""
                    "* order_id: identify products that are in the same basket. \n"
                    "* product_id: identify unique products within the dataset. \n"
                    "* customerid:  identify unique customers within the dataset. \n"
                    "* seller_id: identify unique sellers within the dataset. \n ")

    # -----------------------------
    # Dataset shape
    st.header("**Common questions**")
    cols_box = st.checkbox("How many columns and rows are in datasets?")
    if cols_box:
        st.markdown(f"Items: {items.shape}")
        st.markdown(f"Orders: {orders.shape}")
        st.markdown(f"Products: {products.shape}")
        st.markdown(f"Payments: {payment.shape}")

    order_box = st.checkbox("How many orders are in Order dataset?")
    if order_box:
        st.markdown(f"""Total number of orders: 
                    {orders['order_id'].nunique()}""")

    order_customers = st.checkbox("How many customers are?")
    if order_customers:
        st.markdown(f"""Total number of customers:
                    {orders['order_id'].nunique()}""")

    products_box = st.checkbox("What are the product categories?")
    if products_box:
        products_categories = products['product_category_name'].unique().tolist()
        st.write(f'There are {len(products_categories)} categories.')
        st.dataframe(products_categories)

    payment_type = st.checkbox("""What are the different payment
                              methods?""")
    if payment_type:
        st.markdown(f"""There are {payment['payment_type'].nunique()}
                     payment options:""")
        st.dataframe(payment['payment_type'].unique())

    order_customers = st.checkbox("""What are the possible delievery status
                                   on sales orders?""")
    if order_customers:
        order_status = orders['order_status'].unique().tolist()
        st.dataframe(order_status)

    # -----------------------------
    # Merging dataset ---- add code to streamlit
    st.header("**Descriptive analysis**")
    st.markdown("""First, let's merge our datasets:""")

    orders_items = pd.merge(orders, items, on='order_id')
    products_slice = products.drop(['product_name_lenght',
                                    'product_description_lenght'],
                                    axis='columns')

    merge_df = pd.merge(orders_items, products_slice, on='product_id')
    merge_df = pd.merge(merge_df, payment, on='order_id')

    # -----------------------------
    # Select columns to .describe()
    st.markdown("""A common task is to extract basic information about the 
                dataset, as the maximum and minimum value per variable, 
                find the mean, quantiles, etc. So, you can choose some
                columns to investigate it.""")

    cols = ['price', 'freight_value', 'product_weight_g', 'product_length_cm',
            'product_photos_qty', 'product_length_cm', 'product_height_cm',
            'product_width_cm', 'payment_installments', 'payment_value']

    columns_box = st.multiselect("""Select columns to calculate max, min, 
                                 mean, median and quantiles""", cols)
    if columns_box:
        df_columns_box = merge_df[columns_box]
        st.dataframe(df_columns_box.describe().T)

    # -----------------------------
    # Missing data
    st.markdown("""Another important task is to check types present on the 
                dataset and if exist any missing values. Keep in mind that 
                it is important to handle this effectively, because missing 
                values can impact our interpretation.""")

    missing = pd.DataFrame({'missing count': merge_df.isnull().sum(),
                            'dtype': merge_df.dtypes,
                            'missing %': (merge_df.isnull().sum()/merge_df.shape[0])*100})
    st.dataframe(missing.head(25))

    # Filling missing data
    missing_box = st.checkbox("Do you want to fill missing data?")

    if missing_box:
        st.markdown("""Great, since we have variables with different 
                    types, let's focus focus on numeric types""")

        # Filling in numeric columns
        missing_op = st.selectbox('How do you want to fill missing values',
                                  ('Mean', '0'))

        if missing_op == '0':
            st.markdown('')
            numeric_cols = ['product_photos_qty', 'product_weight_g',
                            'product_length_cm', 'product_height_cm',
                            'product_width_cm']

            for col in numeric_cols:
                merge_df[col] = merge_df[col].fillna(value=0)

        if missing_op == 'Mean':
            st.markdown('')
            numeric_cols = ['product_photos_qty', 'product_weight_g',
                            'product_length_cm', 'product_height_cm',
                            'product_width_cm']

            for col in numeric_cols:
                merge_df[col] = merge_df[col].fillna(value=merge_df[col].mean())

        # Filling in objetc columns
        st.markdown("""Also, Let's handle columns which have 
                    object' types:""")

        missing_obj = st.selectbox("""Do you want to drop rows with missing 
                                   data or ignore it?""", ('Drop', 'Ignore'))

        if missing_obj == 'Drop':
            st.markdown('Sorry, this feature is under construction :(')
            merge_df['product_category_name'] = merge_df['product_category_name'].fillna(value='no_info')
            # object_cols = ['order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date']
            # merge_df = merge_df[merge_df[object_cols].notna()]

        if missing_obj == 'Ignore':
            st.markdown('')

        # Recheck missing data
        missing_box2 = st.checkbox("Want to check the result?")
        if missing_box2:
            missing2 = pd.DataFrame({'missing count': merge_df.isnull().sum(),
                                    'dtype': merge_df.dtypes,
                                    'missing %': (merge_df.isnull().sum()/merge_df.shape[0])*100})
            st.dataframe(missing2.head(25))

    # -----------------------------
    # Data visualization
    st.header("""**Visualization**""")
    st.markdown("""Data visualization it's an important task on data analysis,
                which allows extracting interesting patterns from data and, 
                making it easier to understand. So, Let's start plotting""")

    # Histogram - columns
    st.subheader("Histogram")
    numeric_cols = ['price', 'product_photos_qty', 'product_weight_g',
                    'freight_value', 'product_length_cm', 'product_height_cm',
                    'product_width_cm', 'payment_value', 'payment_installments']

    hist_col = st.selectbox('What column do you want to create a histogram?:', 
                            numeric_cols)
    if hist_col:
        fig_hist = px.histogram(merge_df, x=hist_col)
        st.write(fig_hist)

    # Boxplot - columns
    st.subheader("Boxplot")
    boxplot_col = st.multiselect("""What column do you want to create 
                               boxplot?""", numeric_cols)

    if boxplot_col:
        fig_boxplot = px.box(merge_df, x=boxplot_col)
        st.write(fig_boxplot)

    # Barplot - Products Ordered
    st.subheader("How many products people generally order?")

    number_orders = merge_df.groupby('order_id')['order_item_id'].aggregate('sum').reset_index()
    number_orders = number_orders['order_item_id'].value_counts()
    number_orders.index += 1
    fig_bar = px.bar(number_orders, x=number_orders.index, y=number_orders.values)
    st.write(fig_bar)

    # Barplot - Most bought products
    st.subheader("**Which categories people buy at most?**")
    categories_prods = merge_df.groupby('product_category_name').count().reset_index().sort_values('order_id')
    fig_bar_p = px.bar(categories_prods, y='product_category_name', x='order_id',
                       orientation='h')
    st.write(fig_bar_p)

    # Money spent

    # Barplot - Payment methods
    st.subheader("What is the most common payment method?")
    pay_type = merge_df.groupby('payment_type')['order_id'].count().reset_index()
    pay_type = pay_type.sort_values(by='order_id', ascending=False)
    pay_type = pay_type.rename(columns={'order_id': 'value_count'})
    fig_pay = px.bar(pay_type, y='value_count', x='payment_type',
                     orientation='v')
    st.write(fig_pay)

    # -----------------------------
    # The end!
    st.header("That's all folks!")
    # st.balloons()

    st.markdown("""This work was developed using these excellent Kaggle repositories
                [A] (https://www.kaggle.com/gsdeepakkumar/e-commerce-dataset-analysis/notebook),
                [B] (https://www.kaggle.com/kabure/simple-eda-sales-and-customer-patterns/notebook).
                   \n So, if you want to dive in this dataset, you totally should check them.""")
    st.markdown("""Thank you so much for checking my job! If you liked, please,
                check my [github]
                 (https://github.com/cavalcante-l?tab=repositories)
                and my [linkedin]
                 (https://www.linkedin.com/in/laizacavalcante/). """)
    st.markdown("Developed by Laíza Cavalcante.")


if __name__ == '__main__':
    main()

# Resource: https://www.kaggle.com/olistbr/brazilian-ecommerce/discussion/66851
# https://www.kaggle.com/duygut/brazilian-e-commerce-data-analysis/notebook
# https://www.kaggle.com/gsdeepakkumar/e-commerce-dataset-analysis/notebook
# https://www.kaggle.com/kabure/simple-eda-sales-and-customer-patterns
# https://www.kaggle.com/gsdeepakkumar/e-commerce-dataset-analysis/notebook
# https://www.kaggle.com/hoonkeng/eda-understand-brazil-e-commerce-geographically/data?select=olist_public_dataset_v2.csv
# https://discuss.streamlit.io/t/select-an-item-from-multiselect-on-the-sidebar/1276/2
