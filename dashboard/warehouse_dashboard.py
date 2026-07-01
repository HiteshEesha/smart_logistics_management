import plotly.express as px
import streamlit as st

from db import run_query


def warehouse_dashboard():
    st.header("Warehouse Insights")

    capacity = run_query("""
        SELECT warehouse_id, city, state, capacity
        FROM warehouses
        ORDER BY capacity DESC
    """)

    traffic = run_query("""
        SELECT w.warehouse_id, w.city, w.state, w.capacity,
               COUNT(DISTINCT s.shipment_id) AS traffic
        FROM warehouses w
        LEFT JOIN shipment s
               ON s.origin = w.city OR s.destination = w.city
        GROUP BY w.warehouse_id, w.city, w.state, w.capacity
        ORDER BY traffic DESC
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Warehouse Capacity Comparison")
        fig = px.bar(
            capacity, x="city", y="capacity",
            color="state",
            title="Capacity by Warehouse City",
            labels={"capacity": "Capacity (units)", "city": "City"},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("High-Traffic Warehouse Cities")
        fig2 = px.bar(
            traffic, x="city", y="traffic",
            color="traffic", color_continuous_scale="Blues",
            title="Shipment Traffic by Warehouse City",
            labels={"traffic": "Shipments", "city": "City"},
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Capacity vs Traffic")
        fig3 = px.scatter(
            traffic, x="capacity", y="traffic",
            hover_name="city", size="traffic",
            color="state",
            title="Warehouse Capacity vs Shipment Traffic",
            labels={"capacity": "Capacity (units)", "traffic": "Shipments"},
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("Warehouse Details")
        st.dataframe(
            traffic[["city", "state", "capacity", "traffic"]],
            use_container_width=True,
        )
