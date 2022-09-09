from time import time
import pandas as pd
import streamlit as st
from scrape import *
from visualize import *

st.title("Fetch Twitter Data")

query = st.text_input("Enter your query", help="Please enter your Twitter query here.")

limit = st.slider("Enter tweets limit", 0, 10000, 2500)

# filename = st.text_input("Enter your file_name")
filename = ''

if st.button('Fetch Data'):
    if len(query.strip()) != 0:
        data_df = scrape_data(query, limit, filename)
        # print(data_df)
        # data_df = pd.read_csv("data/Fifa.csv")
        processed_df = preprocess(data_df)

        # Data visualization
        timeline_graph(processed_df)
        hashtag_graph(processed_df)
        accounts_tweeted_graph(processed_df)
        verified_graph(processed_df)
        non_verified_graph(processed_df)
        users_ratio_graph(processed_df)
        user_timeline_graph(processed_df)
        user_creation_annually(processed_df)
        try:
            st.dataframe(processed_df)
        except:
            pass

        # @st.cache
        def download_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv_file = download_df(processed_df)
        st.download_button(
        label="Download data as CSV",
        data=csv_file,
        file_name= filename + '.csv',
        mime='text/csv',
        )
    else:
        st.error('Please enter a query to search')
else:
    # st.error('Please enter a query to search!')
    pass
