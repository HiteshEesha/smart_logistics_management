import plotly.express as px
import streamlit as st

from db import run_query


def courier_dashboard():
    st.header("Courier Performance")

    tab_volume, tab_rating = st.tabs([
        "📦 Shipment Volume",
        "⭐ Ratings & On-Time Delivery",
    ])

    with tab_volume:
        _volume_section()

    with tab_rating:
        _rating_section()


# ─────────────────────────────────────────────
# Shipment Volume per Courier
# ─────────────────────────────────────────────

def _volume_section():
    df = run_query("""
        SELECT c.name          AS courier,
               c.vehicle_type,
               COUNT(s.shipment_id)                  AS total_shipments,
               SUM(s.status = 'Delivered')            AS delivered,
               SUM(s.status = 'Cancelled')            AS cancelled,
               SUM(s.status = 'In Transit')           AS in_transit
        FROM courier_staff c
        LEFT JOIN shipment s ON c.courier_id = s.courier_id
        GROUP BY c.courier_id, c.name, c.vehicle_type
        ORDER BY total_shipments DESC
    """)

    st.subheader("Shipments Handled per Courier")
    fig = px.bar(
        df, x="courier", y="total_shipments",
        color="vehicle_type",
        title="Total Shipments per Courier",
        labels={"total_shipments": "Shipments", "courier": "Courier"},
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Delivery Outcome Breakdown")
    outcome = df.melt(
        id_vars="courier",
        value_vars=["delivered", "cancelled", "in_transit"],
        var_name="outcome",
        value_name="count",
    )
    fig2 = px.bar(
        outcome, x="courier", y="count", color="outcome", barmode="stack",
        title="Delivered / Cancelled / In Transit per Courier",
        labels={"count": "Shipments", "courier": "Courier", "outcome": "Status"},
        color_discrete_map={
            "delivered":  "#2ECC71",
            "cancelled":  "#E74C3C",
            "in_transit": "#3498DB",
        },
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(df, use_container_width=True)


# ─────────────────────────────────────────────
# On-Time Delivery % & Ratings
# ─────────────────────────────────────────────

def _rating_section():
    # On-time: delivered within the route's avg_time_hours (converted to days)
    df = run_query("""
        SELECT c.name   AS courier,
               c.rating,
               COUNT(s.shipment_id) AS total,
               SUM(CASE
                       WHEN s.status = 'Delivered'
                        AND r.avg_time_hours IS NOT NULL
                        AND DATEDIFF(s.delivery_date, s.order_date) <= CEIL(r.avg_time_hours / 24)
                       THEN 1 ELSE 0
                   END) AS on_time_count
        FROM courier_staff c
        LEFT JOIN shipment s   ON c.courier_id = s.courier_id
        LEFT JOIN routes r     ON s.origin = r.origin AND s.destination = r.destination
        GROUP BY c.courier_id, c.name, c.rating
    """)

    df["on_time_pct"] = (
        df["on_time_count"] / df["total"].replace(0, 1) * 100
    ).round(1)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("On-Time Delivery %")
        fig = px.bar(
            df.sort_values("on_time_pct", ascending=False),
            x="courier", y="on_time_pct",
            color="on_time_pct", color_continuous_scale="Greens",
            title="On-Time Delivery % per Courier",
            labels={"on_time_pct": "On-Time %", "courier": "Courier"},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Average Rating Comparison")
        avg_rating = df["rating"].mean()
        fig2 = px.bar(
            df.sort_values("rating", ascending=False),
            x="courier", y="rating",
            color="rating", color_continuous_scale="Blues",
            title="Courier Rating Comparison",
            labels={"rating": "Rating (out of 5)", "courier": "Courier"},
            range_y=[0, 5],
        )
        fig2.add_hline(
            y=avg_rating, line_dash="dash",
            annotation_text=f"Avg: {avg_rating:.2f}",
            line_color="orange",
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Courier Summary Table")
    st.dataframe(
        df[["courier", "rating", "total", "on_time_count", "on_time_pct"]].rename(
            columns={"on_time_count": "on_time", "on_time_pct": "on_time_%"}
        ),
        use_container_width=True,
    )
