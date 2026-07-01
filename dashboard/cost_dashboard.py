import pandas as pd
import plotly.express as px
import streamlit as st

from db import run_query


def cost_dashboard():
    st.header("Cost Analytics")

    totals = run_query("""
        SELECT
            ROUND(SUM(fuel_cost),                          2) AS total_fuel,
            ROUND(SUM(labor_cost),                         2) AS total_labor,
            ROUND(SUM(misc_cost),                          2) AS total_misc,
            ROUND(SUM(fuel_cost + labor_cost + misc_cost), 2) AS total_cost
        FROM costs
    """)
    row = totals.iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Op. Cost",    f"${row['total_cost']:,.2f}")
    c2.metric("Total Fuel Cost",   f"${row['total_fuel']:,.2f}")
    c3.metric("Total Labor Cost",  f"${row['total_labor']:,.2f}")
    c4.metric("Total Misc Cost",   f"${row['total_misc']:,.2f}")

    st.divider()

    tab_breakdown, tab_route, tab_high = st.tabs([
        "🥧 Cost Breakdown",
        "🗺️ Cost per Route",
        "🔴 High-Cost Shipments",
    ])

    with tab_breakdown:
        _breakdown_section(row)

    with tab_route:
        _route_section()

    with tab_high:
        _high_cost_section()


# ─────────────────────────────────────────────
# Fuel / Labor / Misc breakdown
# ─────────────────────────────────────────────

def _breakdown_section(row):
    breakdown = pd.DataFrame({
        "Category": ["Fuel", "Labor", "Misc"],
        "Amount":   [row["total_fuel"], row["total_labor"], row["total_misc"]],
    })

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(
            breakdown, names="Category", values="Amount",
            title="Fuel vs Labor vs Misc Cost Share",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(
            breakdown, x="Category", y="Amount",
            color="Category",
            color_discrete_sequence=px.colors.qualitative.Set2,
            title="Absolute Cost by Category",
            labels={"Amount": "Cost ($)"},
        )
        st.plotly_chart(fig2, use_container_width=True)


# ─────────────────────────────────────────────
# Cost per Route
# ─────────────────────────────────────────────

def _route_section():
    route_cost = run_query("""
        SELECT s.origin, s.destination,
               COUNT(*)                                              AS shipments,
               ROUND(AVG(c.fuel_cost + c.labor_cost + c.misc_cost), 2) AS avg_cost,
               ROUND(SUM(c.fuel_cost + c.labor_cost + c.misc_cost), 2) AS total_cost
        FROM costs c
        JOIN shipment s ON c.shipment_id = s.shipment_id
        GROUP BY s.origin, s.destination
        ORDER BY avg_cost DESC
    """)
    route_cost["route"] = route_cost["origin"] + " → " + route_cost["destination"]

    st.subheader("Average Cost per Route (Top 15)")
    fig = px.bar(
        route_cost.head(15), x="avg_cost", y="route", orientation="h",
        color="avg_cost", color_continuous_scale="Reds",
        title="Top 15 Routes by Average Shipment Cost",
        labels={"avg_cost": "Avg Cost ($)", "route": ""},
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        route_cost[["route", "shipments", "avg_cost", "total_cost"]],
        use_container_width=True,
    )


# ─────────────────────────────────────────────
# High-Cost Shipments
# ─────────────────────────────────────────────

def _high_cost_section():
    high = run_query("""
        SELECT s.shipment_id, s.origin, s.destination, s.status,
               c.fuel_cost, c.labor_cost, c.misc_cost,
               ROUND(c.fuel_cost + c.labor_cost + c.misc_cost, 2) AS total_cost
        FROM costs c
        JOIN shipment s ON c.shipment_id = s.shipment_id
        ORDER BY total_cost DESC
        LIMIT 20
    """)

    st.subheader("Top 20 High-Cost Shipments")
    fig = px.bar(
        high, x="shipment_id", y="total_cost",
        color="status",
        title="Top 20 Costliest Shipments",
        labels={"total_cost": "Total Cost ($)", "shipment_id": "Shipment ID"},
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(high, use_container_width=True)
