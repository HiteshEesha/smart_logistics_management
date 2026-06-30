import streamlit as st
import pandas as pd
import mysql.connector

def shipment_dashboard():

    st.header("Shipment Dashboard")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="logistics"
    )

    query = """
    SELECT
        shipment_status,
        COUNT(*) AS total
    FROM shipment
    GROUP BY shipment_status
    """

    df = pd.read_sql(query, conn)

    st.dataframe(df)

    st.bar_chart(
        df.set_index("shipment_status")
    )