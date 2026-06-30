import streamlit as st
import pandas as pd
import mysql.connector

def cost_dashboard():

    st.header("Shipping Cost Dashboard")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="logistics"
    )

    query = """
    SELECT
        courier_name,
        SUM(shipping_cost) AS total_cost
    FROM shipment
    GROUP BY courier_name
    """

    df = pd.read_sql(query, conn)

    st.dataframe(df)

    st.bar_chart(
        df.set_index("courier_name")
    )