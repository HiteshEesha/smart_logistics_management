import streamlit as st
import pandas as pd
import mysql.connector

def warehouse_dashboard():

    st.header("Warehouse Dashboard")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="logistics"
    )

    query = """
    SELECT
        warehouse_name,
        COUNT(*) AS shipments
    FROM shipment
    GROUP BY warehouse_name
    """

    df = pd.read_sql(query, conn)

    st.dataframe(df)

    st.bar_chart(
        df.set_index("warehouse_name")
    )