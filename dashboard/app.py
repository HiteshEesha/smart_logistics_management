import streamlit as st

from shipment_dashboard import shipment_dashboard
from courier_dashboard import courier_dashboard
from warehouse_dashboard import warehouse_dashboard
from cost_dashboard import cost_dashboard

st.set_page_config(
    page_title="Smart Logistics Dashboard",
    layout="wide"
)

st.title("🚚 Smart Logistics Management Dashboard")

menu = st.sidebar.selectbox(
    "Select Dashboard",
    [
        "Shipment",
        "Courier",
        "Warehouse",
        "Cost"
    ]
)

if menu == "Shipment":
    shipment_dashboard()

elif menu == "Courier":
    courier_dashboard()

elif menu == "Warehouse":
    warehouse_dashboard()

else:
    cost_dashboard()