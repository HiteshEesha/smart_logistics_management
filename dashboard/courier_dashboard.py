import streamlit as st
import pandas as pd
import mysql.connector

def courier_dashboard():

    st.header("Courier Performance")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="logistics"
    )

    query = """
    SELECT
        courier_name,
        COUNT(*) AS total_shipments
    FROM shipment
    GROUP BY courier_name
    """

    df = pd.read_sql(query, conn)

    st.dataframe(df)

    st.bar_chart(
        df.set_index("courier_name")
    )