import pandas as pd
import plotly.express as px
import streamlit as st

from db import run_query


def shipment_dashboard():
    st.header("Shipment Dashboard")

    tab_kpi, tab_search, tab_delivery, tab_cancel = st.tabs([
        "📊 KPIs & Overview",
        "🔎 Search & Filter",
        "📈 Delivery Performance",
        "❌ Cancellation Analysis",
    ])

    with tab_kpi:
        _kpi_section()

    with tab_search:
        _search_section()

    with tab_delivery:
        _delivery_performance_section()

    with tab_cancel:
        _cancellation_section()


# ─────────────────────────────────────────────
# KPIs & Overview
# ─────────────────────────────────────────────

def _kpi_section():
    totals = run_query("""
        SELECT
            COUNT(*)  AS total,
            SUM(status = 'Delivered')  AS delivered,
            SUM(status = 'Cancelled')  AS cancelled
        FROM shipment
    """)

    total_cost = run_query("""
        SELECT ROUND(SUM(fuel_cost + labor_cost + misc_cost), 2) AS total_cost
        FROM costs
    """)

    row = totals.iloc[0]
    total      = int(row["total"])
    delivered  = int(row["delivered"])
    cancelled  = int(row["cancelled"])
    cost       = total_cost.iloc[0]["total_cost"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Shipments",   total)
    c2.metric("Delivered %",       f"{delivered / total * 100:.1f}%")
    c3.metric("Cancelled %",       f"{cancelled / total * 100:.1f}%")
    c4.metric("Total Op. Cost",    f"${cost:,.2f}")

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        status_df = run_query(
            "SELECT status, COUNT(*) AS count FROM shipment GROUP BY status"
        )
        fig = px.pie(
            status_df, names="status", values="count",
            title="Shipment Status Distribution",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        monthly = run_query("""
            SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
                   COUNT(*) AS shipments
            FROM shipment
            GROUP BY month
            ORDER BY month
        """)
        fig2 = px.line(
            monthly, x="month", y="shipments",
            title="Monthly Shipment Trend", markers=True,
        )
        st.plotly_chart(fig2, use_container_width=True)


# ─────────────────────────────────────────────
# Search & Filter
# ─────────────────────────────────────────────

def _search_section():
    df = run_query("""
        SELECT s.shipment_id, s.order_date, s.origin, s.destination,
               s.weight, s.status, s.delivery_date,
               c.name AS courier_name
        FROM shipment s
        JOIN courier_staff c ON s.courier_id = c.courier_id
    """)

    df["order_date"]    = pd.to_datetime(df["order_date"])
    df["delivery_date"] = pd.to_datetime(df["delivery_date"])

    st.subheader("Filters")
    col1, col2 = st.columns(2)

    with col1:
        search_id = st.text_input("Search by Shipment ID")
        status_filter = st.multiselect(
            "Status",
            options=sorted(df["status"].unique().tolist()),
            default=sorted(df["status"].unique().tolist()),
        )
        courier_filter = st.multiselect(
            "Courier",
            options=sorted(df["courier_name"].unique().tolist()),
        )

    with col2:
        origin_filter = st.multiselect(
            "Origin",
            options=sorted(df["origin"].unique().tolist()),
        )
        dest_filter = st.multiselect(
            "Destination",
            options=sorted(df["destination"].unique().tolist()),
        )
        min_date = df["order_date"].min().date()
        max_date = df["order_date"].max().date()
        date_range = st.date_input(
            "Order Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )

    filtered = df.copy()

    if search_id:
        filtered = filtered[
            filtered["shipment_id"].str.contains(search_id, case=False, na=False)
        ]
    if status_filter:
        filtered = filtered[filtered["status"].isin(status_filter)]
    if courier_filter:
        filtered = filtered[filtered["courier_name"].isin(courier_filter)]
    if origin_filter:
        filtered = filtered[filtered["origin"].isin(origin_filter)]
    if dest_filter:
        filtered = filtered[filtered["destination"].isin(dest_filter)]
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start, end = date_range
        filtered = filtered[
            (filtered["order_date"].dt.date >= start) &
            (filtered["order_date"].dt.date <= end)
        ]

    st.caption(f"Showing {len(filtered):,} of {len(df):,} shipments")
    st.dataframe(filtered.reset_index(drop=True), use_container_width=True)


# ─────────────────────────────────────────────
# Delivery Performance
# ─────────────────────────────────────────────

def _delivery_performance_section():
    route_perf = run_query("""
        SELECT origin, destination,
               COUNT(*)  AS shipments,
               ROUND(AVG(DATEDIFF(delivery_date, order_date)), 1)     AS avg_days
        FROM shipment
        WHERE delivery_date IS NOT NULL AND status = 'Delivered'
        GROUP BY origin, destination
        ORDER BY avg_days DESC
    """)
    route_perf["route"] = route_perf["origin"] + " → " + route_perf["destination"]

    st.subheader("Average Delivery Time per Route")
    fig = px.bar(
        route_perf.head(15), x="avg_days", y="route", orientation="h",
        color="avg_days", color_continuous_scale="Reds",
        title="Top 15 Routes by Avg Delivery Time (days)",
        labels={"avg_days": "Avg Days", "route": ""},
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Most Delayed Routes")
    st.dataframe(
        route_perf[["route", "shipments", "avg_days"]].head(10),
        use_container_width=True,
    )

    dist_perf = run_query("""
        SELECT s.origin, s.destination,
               ROUND(AVG(DATEDIFF(s.delivery_date, s.order_date)), 1) AS avg_days,
               r.distance_km
        FROM shipment s
        JOIN routes r ON s.origin = r.origin AND s.destination = r.destination
        WHERE s.delivery_date IS NOT NULL AND s.status = 'Delivered'
        GROUP BY s.origin, s.destination, r.distance_km
    """)

    if not dist_perf.empty:
        st.subheader("Delivery Time vs Distance")
        dist_perf["route"] = dist_perf["origin"] + " → " + dist_perf["destination"]
        fig2 = px.scatter(
            dist_perf, x="distance_km", y="avg_days",
            hover_name="route", size="avg_days",
            title="Delivery Time (days) vs Route Distance (km)",
            labels={"distance_km": "Distance (km)", "avg_days": "Avg Days"},
        )
        st.plotly_chart(fig2, use_container_width=True)


# ─────────────────────────────────────────────
# Cancellation Analysis
# ─────────────────────────────────────────────

def _cancellation_section():
    cancel_origin = run_query("""
        SELECT origin,
               COUNT(*)                                                            AS total,
               SUM(status = 'Cancelled')                                           AS cancelled,
               ROUND(SUM(status = 'Cancelled') * 100.0 / COUNT(*), 1)             AS cancel_rate
        FROM shipment
        GROUP BY origin
        ORDER BY cancel_rate DESC
    """)

    st.subheader("Cancellation Rate by Origin")
    fig = px.bar(
        cancel_origin.head(15), x="cancel_rate", y="origin", orientation="h",
        color="cancel_rate", color_continuous_scale="Oranges",
        title="Top 15 Origins by Cancellation Rate (%)",
        labels={"cancel_rate": "Cancel Rate (%)", "origin": ""},
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        cancel_courier = run_query("""
            SELECT c.name AS courier,
                   COUNT(s.shipment_id)                                              AS total,
                   SUM(s.status = 'Cancelled')                                       AS cancelled,
                   ROUND(SUM(s.status = 'Cancelled') * 100.0 / COUNT(s.shipment_id), 1) AS cancel_rate
            FROM courier_staff c
            LEFT JOIN shipment s ON c.courier_id = s.courier_id
            GROUP BY c.courier_id, c.name
            ORDER BY cancel_rate DESC
        """)
        st.subheader("Cancellation Rate by Courier")
        fig2 = px.bar(
            cancel_courier, x="cancel_rate", y="courier", orientation="h",
            color="cancel_rate", color_continuous_scale="Purples",
            title="Cancellation Rate by Courier (%)",
            labels={"cancel_rate": "Cancel Rate (%)", "courier": ""},
        )
        fig2.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        monthly_cancel = run_query("""
            SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
                   COUNT(*)                         AS total,
                   SUM(status = 'Cancelled')        AS cancelled
            FROM shipment
            GROUP BY month
            ORDER BY month
        """)
        monthly_cancel["cancel_rate"] = (
            monthly_cancel["cancelled"] / monthly_cancel["total"] * 100
        ).round(1)

        st.subheader("Monthly Cancellation Trend")
        fig3 = px.line(
            monthly_cancel, x="month", y="cancel_rate",
            title="Monthly Cancellation Rate (%)", markers=True,
        )
        st.plotly_chart(fig3, use_container_width=True)
