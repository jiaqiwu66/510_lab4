import streamlit as st
from dotenv import load_dotenv
import os

import pandas as pd

from db import Database

load_dotenv()


# reference: https://medium.com/streamlit/paginating-dataframes-with-streamlit-2da29b080920
# Basically, we are splitting the dataframe into smaller dataframes based on the number of rows

def split_frame(input_df, rows):
    df = [input_df.loc[i: i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df


# Use context manager to manage the database connection
# Learn more about context managers: https://realpython.com/python-with-statement/
with Database(os.getenv('DATABASE_URL')) as pg:
    pg.create_table()
    df = pd.read_sql('SELECT * FROM books', pg.con)

    st.title('📖 Books Generator')
    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input(label="Search name", placeholder="Please input the keyword", key="search_term_1")
        if search_term:
            df = pd.read_sql(f"SELECT * FROM books "
                                f"WHERE name ILIKE '% {search_term}%' "
                                f"ORDER BY created_at DESC", pg.con)
    with col2:
        search_term = st.text_input(label="Search description", placeholder="Please input the keyword", key="search_term_2")
        if search_term:
            df = pd.read_sql(f"SELECT * FROM books "
                                f"WHERE description ILIKE '% {search_term}%' "
                                f"ORDER BY created_at DESC", pg.con)
            
    st.markdown("Filter and Order")
    col1, col2, col3, col4, col5 = st.columns(5)
     # sort by price
    with col1:
        price_sort_low = st.button("Sort Price ⬆️")
    with col2:
        price_sort_high = st.button("Sort Price ⬇️")
    if price_sort_low:
        df = pd.read_sql("SELECT * FROM books ORDER BY price", pg.con)
    if price_sort_high:
        df = pd.read_sql("SELECT * FROM books ORDER BY price DESC", pg.con)

    # sort by rating
    with col3:
        rating_sort_low = st.button("Sort Rating ⬆️")
    with col4:
        rating_sort_high = st.button("Sort Rating ⬇️")
    if rating_sort_low:
        df = pd.read_sql("SELECT * FROM books ORDER BY rating", pg.con)
    if rating_sort_high:
        df = pd.read_sql("SELECT * FROM books ORDER BY rating DESC", pg.con)
    
    # Create a placeholder
    container = st.container()

    bottom_menu = st.columns((4, 2, 1))
    with bottom_menu[2]:
        batch_size = st.selectbox("Page Size", options=[25, 50, 100])
    with bottom_menu[1]:
        total_pages = (
            int(len(df) / batch_size) if int(len(df) / batch_size) > 0 else 1
        )
        current_page = st.number_input(
            "Page", min_value=1, max_value=total_pages, step=1
        )
    with bottom_menu[0]:
        st.markdown(f"Page **{current_page}** of **{total_pages}** ")

    pages = split_frame(df, batch_size)

    # Write the dataframe component to the previously created container


    if len(pages) == 0:
        st.write("No books available")
    else:
        container.dataframe(data=pages[current_page - 1], use_container_width=True)