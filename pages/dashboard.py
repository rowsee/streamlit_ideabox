import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_all_ideas
from datetime import datetime, timedelta

st.markdown(
    """
<style>
    .dashboard-header {
        font-size: 28px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 24px;
    }
    
    .chart-container {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .chart-title {
        font-size: 16px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 16px;
    }
    
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #ff6b36;
    }
    
    .metric-label {
        font-size: 14px;
        color: #6B7280;
        margin-top: 8px;
    }
</style>
""",
    unsafe_allow_html=True,
)


def render():
    st.markdown(
        '<div class="dashboard-header">📊 Dashboard</div>', unsafe_allow_html=True
    )

    ideas = get_all_ideas()

    if not ideas:
        st.info("No ideas submitted yet. Start by submitting an idea!")
        return

    df = pd.DataFrame([dict(row) for row in ideas])

    df["submitted_at"] = pd.to_datetime(df["submitted_at"])

    st.markdown("### 🔍 Filters")

    # Date range filter (default: This Month)
    from datetime import datetime, timedelta

    col_date1, col_date2 = st.columns([1, 3])

    with col_date1:
        date_preset = st.selectbox(
            "Date Range",
            options=["This Month", "Last 30 Days", "This Year", "All Time", "Custom"],
            index=0,
            key="date_preset",
        )

    # Calculate date range based on preset
    today = datetime.now().date()
    if date_preset == "This Month":
        default_start = today.replace(day=1)
        default_end = today
    elif date_preset == "Last 30 Days":
        default_start = today - timedelta(days=30)
        default_end = today
    elif date_preset == "This Year":
        default_start = today.replace(month=1, day=1)
        default_end = today
    elif date_preset == "All Time":
        default_start = df["submitted_at"].min().date()
        default_end = today
    else:  # Custom
        default_start = today.replace(day=1)
        default_end = today

    with col_date2:
        if date_preset == "Custom":
            date_range = st.date_input(
                "Select Date Range",
                value=[default_start, default_end],
                key="dashboard_date_range",
            )
        else:
            date_range = [default_start, default_end]
            st.markdown(
                f"**{default_start.strftime('%b %d, %Y')} - {default_end.strftime('%b %d, %Y')}**"
            )

    col1, col2, col3 = st.columns(3)

    with col1:
        region_filter = st.multiselect(
            "Region",
            options=["All"] + list(df["region"].dropna().unique()),
            default="All",
        )

    with col2:
        bu_filter = st.multiselect(
            "BU/CL Site",
            options=["All"] + list(df["bu_cl_site"].dropna().unique()),
            default="All",
        )

    with col3:
        implemented_filter = st.multiselect(
            "Implemented", options=["All", "Yes", "No"], default="All"
        )

    filtered_df = df.copy()

    # Apply date filter
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df["submitted_at"].dt.date >= start_date)
            & (filtered_df["submitted_at"].dt.date <= end_date)
        ]

    if region_filter and "All" not in region_filter:
        filtered_df = filtered_df[filtered_df["region"].isin(region_filter)]

    if bu_filter and "All" not in bu_filter:
        filtered_df = filtered_df[filtered_df["bu_cl_site"].isin(bu_filter)]

    if implemented_filter and "All" not in implemented_filter:
        filtered_df = filtered_df[
            filtered_df["is_implemented"].isin(implemented_filter)
        ]

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="metric-value">{len(filtered_df)}</div>
            <div class="metric-label">Total Ideas</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        implemented_count = len(filtered_df[filtered_df["is_implemented"] == "Yes"])
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="metric-value">{implemented_count}</div>
            <div class="metric-label">Implemented</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        total_hours = filtered_df["hours_saved"].sum()
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="metric-value">{total_hours:,.0f}</div>
            <div class="metric-label">Hours Saved</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        avg_hours = filtered_df["hours_saved"].mean()
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="metric-value">{avg_hours:,.0f}</div>
            <div class="metric-label">Avg Hours Saved</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="chart-container"><div class="chart-title">📊 Submitted Projects per Site Leader</div>',
            unsafe_allow_html=True,
        )

        if (
            "site_leader" in filtered_df.columns
            and filtered_df["site_leader"].notna().any()
        ):
            site_leader_counts = (
                filtered_df.groupby("site_leader").size().reset_index(name="Count")
            )
            fig = px.bar(
                site_leader_counts,
                x="site_leader",
                y="Count",
                color="Count",
                color_continuous_scale=["#ff6b36", "#FFA500", "#FFB088"],
            )
            fig.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(color="#111827"),
                xaxis=dict(title="Site Leader"),
                yaxis=dict(title="Number of Projects"),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No site leader data available")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            '<div class="chart-container"><div class="chart-title">📊 Implemented Projects per Site Leader</div>',
            unsafe_allow_html=True,
        )

        implemented_df = filtered_df[filtered_df["is_implemented"] == "Yes"]
        if (
            "site_leader" in implemented_df.columns
            and implemented_df["site_leader"].notna().any()
        ):
            implemented_counts = (
                implemented_df.groupby("site_leader").size().reset_index(name="Count")
            )
            fig = px.bar(
                implemented_counts,
                x="site_leader",
                y="Count",
                color="Count",
                color_continuous_scale=["#10B981", "#34D399", "#6EE7B7"],
            )
            fig.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(color="#111827"),
                xaxis=dict(title="Site Leader"),
                yaxis=dict(title="Number of Implemented Projects"),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No implemented projects data available")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="chart-container"><div class="chart-title">📊 Hours Saved per BU/CL Site</div>',
            unsafe_allow_html=True,
        )

        hours_per_bu = (
            filtered_df.groupby("bu_cl_site")["hours_saved"].sum().reset_index()
        )
        hours_per_bu = hours_per_bu[hours_per_bu["hours_saved"] > 0]

        if len(hours_per_bu) > 0:
            fig = px.bar(
                hours_per_bu,
                x="bu_cl_site",
                y="hours_saved",
                color="hours_saved",
                color_continuous_scale=["#ff6b36", "#FFA500", "#FFB088"],
            )
            fig.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(color="#111827"),
                xaxis=dict(title="BU/CL Site"),
                yaxis=dict(title="Hours Saved"),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hours saved data available")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            '<div class="chart-container"><div class="chart-title">🥧 Total Project Ideas per BU</div>',
            unsafe_allow_html=True,
        )

        bu_counts = filtered_df.groupby("bu_cl_site").size().reset_index(name="Count")

        if len(bu_counts) > 0:
            fig = px.pie(
                bu_counts,
                values="Count",
                names="bu_cl_site",
                color_discrete_sequence=px.colors.sequential.Oranges,
            )
            fig.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(color="#111827"),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No BU data available")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="chart-container"><div class="chart-title">🥧 Hours Saved by Impact Group</div>',
            unsafe_allow_html=True,
        )

        hours_by_impact = (
            filtered_df.groupby("impact_group")["hours_saved"].sum().reset_index()
        )
        hours_by_impact = hours_by_impact[hours_by_impact["hours_saved"] > 0]

        if len(hours_by_impact) > 0:
            fig = px.pie(
                hours_by_impact,
                values="hours_saved",
                names="impact_group",
                color_discrete_sequence=px.colors.sequential.Blues,
            )
            fig.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(color="#111827"),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No impact group data available")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(
        '<div class="chart-container"><div class="chart-title">📈 Projects Submitted Over Time</div>',
        unsafe_allow_html=True,
    )

    time_filter = st.radio(
        "Select Time Period:", ["Daily", "Monthly", "Yearly"], horizontal=True
    )

    if time_filter == "Daily":
        filtered_df["date"] = filtered_df["submitted_at"].dt.date
        date_counts = filtered_df.groupby("date").size().reset_index(name="Count")
        date_counts = date_counts.sort_values("date")
        fig = px.line(date_counts, x="date", y="Count", markers=True)
    elif time_filter == "Monthly":
        filtered_df["month"] = filtered_df["submitted_at"].dt.to_period("M").astype(str)
        date_counts = filtered_df.groupby("month").size().reset_index(name="Count")
        date_counts = date_counts.sort_values("month")
        fig = px.line(date_counts, x="month", y="Count", markers=True)
    else:
        filtered_df["year"] = filtered_df["submitted_at"].dt.year
        date_counts = filtered_df.groupby("year").size().reset_index(name="Count")
        date_counts = date_counts.sort_values("year")
        fig = px.line(date_counts, x="year", y="Count", markers=True)

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111827"),
        xaxis=dict(title=time_filter),
        yaxis=dict(title="Number of Projects"),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
