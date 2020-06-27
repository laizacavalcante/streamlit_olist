import pandas as pd
import streamlit as st
import plotly.express as px

# cd ./Data-Science-Online/'Semana 3'/study/desafio_extra/
# streamlit run streamlit_olist.py


def main():
    # -----------------------------
    # Initial description
    st.image('./dataset-cover.png', width=900)
    st.title('Analysis of e-commerce dataset')
    st.markdown("""Here, I will introduce some basic descriptive anlyses of
                Olist brazilian e-commerce dataset.This dataset contains
                more than 110K orders from 2016 to 2018. This dataset consists
                of a detailed custumer transaction details.
             """)
    st.markdown("""The dataset consists of **9 datasets**, which describe orders,
                items and their categories, users reviews, information about
                estimate date of deliver, payment method, geolocation,
                and much, much more.""")

    st.markdown("""Initially, I will start using **4 datasets**: 
                olist_orders_dataset, olist_order_items_dataset,
                and olist_products_dataset. So, let's start:""")

    # -----------------------------
    # Import dataset
    st.header("**Dataset Investigation**")
    items = pd.read_csv("./olist_dataset/olist_order_items_dataset.csv")
    orders = pd.read_csv("./olist_dataset/olist_orders_dataset.csv")
    products = pd.read_csv("./olist_dataset/olist_products_dataset.csv")
    payment = pd.read_csv("./olist_dataset/olist_order_payments_dataset.csv")

    # Slider for dataframe.head
    slider_bar = st.slider(label='How many rows do you want to  see?', 
                           min_value=1, max_value=10)
    st.markdown('**Items dataset**')
    st.dataframe(items.head(slider_bar))

    st.markdown('**Orders dataset**')
    st.dataframe(orders.head(slider_bar))

    st.markdown('**Products dataset**')
    st.dataframe(products.head(slider_bar))

    st.markdown('**Payment dataset**')
    st.dataframe(payment.head(slider_bar))

    # Columns description
    add_info = st.checkbox('Want additional info of columns?')
    if add_info:
        st.markdown("* order_id: identify products that are in the same basket. \n"
                    "* product_id: identify unique products within the dataset. \n"
                    "* customerid:  identify unique customers within the dataset. \n"
                    "* seller_id: identify unique sellers within the dataset. \n ")

    # -----------------------------
    # Dataset shape
    st.header("**Common questions**")
    cols_box = st.checkbox("How many columns and rows they have?")
    if cols_box:
        st.markdown(f"Items: {items.shape}")
        st.markdown(f"Orders: {orders.shape}")
        st.markdown(f"Products: {products.shape}")
        st.markdown(f"Payments: {payment.shape}")

    order_box = st.checkbox("How many orders?")
    if order_box:
        st.markdown(f"Total number of orders : {orders['order_id'].nunique()}")

    order_customers = st.checkbox("How many customers?")
    if order_customers:
        st.markdown(f"""Total number of customers:
                    {orders['order_id'].nunique()}""")
    
    payment_type = st.checkbox("What are the payment options?")
    if payment_type:
        st.markdown(f"""There are {payment['payment_type'].nunique()}
                     payment options:""")
        st.dataframe(payment['payment_type'].unique())
    
    order_customers = st.checkbox("""How are the possible status for
                                  delivery orders?""")
    if order_customers:
        order_status = orders['order_status'].unique().tolist()
        st.dataframe(order_status)

    products_box = st.checkbox("What are the products categories?")
    if products_box:
        products_categories = products['product_category_name'].unique().tolist()
        st.write(f'There are {len(products_categories)} categories.')
        st.dataframe(products_categories)
    
    # -----------------------------
    # Merging dataset ---- add code to streamlit
    st.header("**Descriptive analysis**")
    st.markdown("""First, let's merge our datasets:""")

    orders_items = pd.merge(orders, items, on='order_id')
    products_slice = products.drop(['product_name_lenght', 'product_description_lenght'],
                                   axis='columns')
    merge_df = pd.merge(orders_items, products_slice, on='product_id')
    merge_df = pd.merge(merge_df, payment, on='order_id')

    # -----------------------------
    # Select columns to .describe()
    st.markdown("""A common task is extract basic information about the dataset, as the maximum
                and minimum value per variable, find the mean, extract information of
                data distribution with quantiles, etc. So, to discover the data you can
                chose some columns to get this information """)

    cols = ['price', 'freight_value', 'product_weight_g', 'product_length_cm',
            'product_photos_qty', 'product_length_cm', 'product_height_cm',
            'product_width_cm', 'payment_installments', 'payment_value']

    columns_box = st.multiselect("Select Columns to calculate max, min, mean, median and quantiles",
                                 cols)
    if columns_box:
        df_columns_box = merge_df[columns_box]
        st.dataframe(df_columns_box.describe().T)

    # -----------------------------
    # Missing data
    st.markdown("""Another important task is check types present on dataset and if
                exist any missing values. Keep in mind that is important to handle
                this effectively, because missing values can impact our interpretation.
                """)
    missing = pd.DataFrame({'missing count': merge_df.isnull().sum(),
                        'dtype': merge_df.dtypes,
                        'missing %': (merge_df.isnull().sum()/merge_df.shape[0])*100})
    st.dataframe(missing.head(25))

    # Filling missing data
    missing_box = st.checkbox("Do you want to fill missing data?")

    if missing_box:
        st.markdown("""Great, pay attention that we have different types on data.
                    So, first we will focus on numeric types""")

        # Filling in numeric columns
        missing_op = st.selectbox('How do you want to fill missing values', ('Mean', '0'))

        if missing_op == '0':
            st.markdown('')
            numeric_cols = ['product_photos_qty','product_weight_g', 'product_length_cm',
                            'product_height_cm', 'product_width_cm']

            for col in numeric_cols:
                merge_df[col] = merge_df[col].fillna(value=0)

        if missing_op == 'Mean':
            st.markdown('')
            numeric_cols = ['product_photos_qty','product_weight_g', 'product_length_cm',
                'product_height_cm', 'product_width_cm']

            for col in numeric_cols:
                merge_df[col] = merge_df[col].fillna(value=merge_df[col].mean())

        # Filling in objetc columns
        st.markdown("""Also, Let's handle columns which have 'object' types:""")
        missing_obj = st.selectbox('Do you want to drop rows with missing data or ignore it?', ('Drop', 'Ignore'))

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
                with it, we can extract interesting patterns from data and, making
                easier to understand.""")

    st.markdown("""So, Let's start  with histogram plotting""")
    numeric_cols = ['price', 'product_photos_qty', 'product_weight_g',
                    'freight_value', 'product_length_cm', 'product_height_cm',
                    'product_width_cm', 'payment_value', 'payment_installments']

    # Histogram - columns
    hist_col = st.selectbox('What column do you want to plot histogram?:', numeric_cols)
    if hist_col:
        fig_hist = px.histogram(merge_df, x=hist_col, title='Histogram')
        st.write(fig_hist)

    # Boxplot - columns
    boxplot_fig = st.selectbox('What column do you want to create boxplot?:', numeric_cols)
    if boxplot_fig:
        fig_boxplot = px.box(merge_df, x=hist_col, title='Boxplot')
        st.write(fig_boxplot)

    # Barplot - Products Ordered
    st.markdown("**How many products people generally order?**")
    number_orders = merge_df.groupby('order_id')['order_item_id'].aggregate('sum').reset_index()
    number_orders = number_orders['order_item_id'].value_counts()
    number_orders.index += 1
    fig_bar = px.bar(number_orders, x=number_orders.index, y=number_orders.values)
    st.write(fig_bar)

    # Barplot - Most bought products
    st.markdown("**Which categories people buy at most?**")
    categories_prods = merge_df.groupby('product_category_name').count().reset_index().sort_values('order_id')
    fig_bar_p = px.bar(categories_prods, y='product_category_name', x='order_id',
                       orientation='h')
    st.write(fig_bar_p)

    # Money spent

    # Barplot - Payment methods
    pay_type = merge_df.groupby('payment_type')['order_id'].count().reset_index()
    pay_type = pay_type.sort_values(by='order_id',ascending=False)
    pay_type = pay_type.rename(columns={'order_id': 'value_count'})
    fig_pay = px.bar(pay_type, y='value_count', x='payment_type',
                     orientation='v')
    st.write(fig_pay)

    # -----------------------------
    # The end!
    st.markdown("Well that's all folks!")
    # st.balloons()

    st.markdown("""This work was developed using these excellent Kaggle repositories
                [A] (https://www.kaggle.com/gsdeepakkumar/e-commerce-dataset-analysis/notebook),
                [B] (https://www.kaggle.com/kabure/simple-eda-sales-and-customer-patterns/notebook).
                So, if you want to dive in this dataset, you totally should check them.""")
    st.markdown("""Thank you so much for checking my job! If you liked, please,
                check my [github]
                 (https://github.com/cavalcante-l?tab=repositories)
                and my [linkedin]
                 (https://www.linkedin.com/in/laizacavalcante/). """)


if __name__ == '__main__':
    main()

# Resource: https://www.kaggle.com/olistbr/brazilian-ecommerce/discussion/66851
# https://www.kaggle.com/duygut/brazilian-e-commerce-data-analysis/notebook
# https://www.kaggle.com/gsdeepakkumar/e-commerce-dataset-analysis/notebook
# https://www.kaggle.com/kabure/simple-eda-sales-and-customer-patterns
# https://www.kaggle.com/gsdeepakkumar/e-commerce-dataset-analysis/notebook
# https://www.kaggle.com/hoonkeng/eda-understand-brazil-e-commerce-geographically/data?select=olist_public_dataset_v2.csv
# https://discuss.streamlit.io/t/select-an-item-from-multiselect-on-the-sidebar/1276/2