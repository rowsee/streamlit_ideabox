import streamlit as st
from database import get_stats, get_user_ideas, get_top_contributors_per_bu

st.set_page_config(layout="wide", page_icon="💡")

st.markdown(
    """
<style>
    :root {
        --bg-white: #ffffff;
        --bg-light: #f8fafc;
        --text-primary: #1e293b;
        --text-muted: #64748b;
        --border-light: #e2e8f0;
        --indigo: #6366f1;
        --orange: #f97316;
        --green: #10b981;
        --pink: #ec4899;
        --purple-start: #6366f1;
        --purple-end: #8b5cf6;
        --orange-start: #f97316;
        --orange-end: #fb923c;
    }

    .stApp { background-color: var(--bg-white); }

    .header-card {
        background: white;
        border-radius: 16px;
        padding: 24px 28px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    }

    .header-badge {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #1a1a2e;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        display: inline-block;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .header-title {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 8px 0;
        line-height: 1.2;
    }

    .header-subtitle {
        font-size: 15px;
        color: #64748b;
        margin: 0;
    }

    .header-name {
        color: #6366f1;
        font-weight: 600;
    }

    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 18px 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border-left: 4px solid;
        height: 100%;
        transition: all 0.3s ease;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    .kpi-card.purple { border-left-color: #8b5cf6; }
    .kpi-card.green { border-left-color: #10b981; }
    .kpi-card.orange { border-left-color: #f97316; }
    .kpi-card.pink { border-left-color: #ec4899; }

    .kpi-number {
        font-size: 38px;
        font-weight: 800;
        color: #1e293b;
        line-height: 1;
        margin-bottom: 6px;
    }

    .kpi-label {
        font-size: 13px;
        font-weight: 600;
        color: #475569;
        margin-bottom: 4px;
    }

    .kpi-sub {
        font-size: 11px;
        color: #94a3b8;
    }

    .quick-stats {
        background: #f8fafc;
        border-radius: 10px;
        padding: 14px 20px;
        margin: 20px 0;
    }

    .quick-stats .stat-item {
        text-align: center;
    }

    .quick-stats .stat-value {
        font-size: 20px;
        font-weight: 700;
        color: #1e293b;
    }

    .quick-stats .stat-label {
        font-size: 11px;
        color: #64748b;
        margin-top: 2px;
    }

    .card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #f1f5f9;
        height: 100%;
    }

    .card-title {
        font-size: 16px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .why-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .why-list li {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 0;
        border-bottom: 1px solid #f1f5f9;
        font-size: 14px;
        color: #475569;
    }

    .why-list li:last-child {
        border-bottom: none;
    }

    .why-icon {
        font-size: 18px;
    }

    .benefits-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 10px;
        margin-top: 16px;
    }

    .benefit-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 12px;
        background: #f8fafc;
        border-radius: 8px;
        font-size: 13px;
        color: #475569;
    }

    .benefit-check {
        color: #10b981;
        font-weight: 700;
        font-size: 16px;
    }

    .topbu-card {
        background: linear-gradient(135deg, #f97316, #fb923c);
        border-radius: 20px;
        padding: 32px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 30px rgba(249, 115, 22, 0.25);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .topbu-label {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        opacity: 0.95;
        margin-bottom: 12px;
    }

    .topbu-name {
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .topbu-count {
        font-size: 60px;
        font-weight: 800;
        line-height: 1;
    }

    .topbu-text {
        font-size: 13px;
        opacity: 0.9;
        margin-top: 6px;
    }

    .cta-card {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-radius: 14px;
        padding: 20px;
        color: white;
        text-align: center;
        margin-top: 16px;
    }

    .cta-title {
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .cta-text {
        font-size: 12px;
        opacity: 0.95;
    }

    .stDivider { margin: 20px 0; }
</style>
""",
    unsafe_allow_html=True,
)


def render():
    stats = get_stats() or {}
    top_bu = get_top_contributors_per_bu() or {}
    user_ideas = get_user_ideas(st.session_state.user_id) or []
    user_idea_count = len(user_ideas)

    user_name = st.session_state.get("full_name") or st.session_state.get(
        "username", "User"
    )

    # HEADER
    st.markdown('<div class="header-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="header-badge">✨ TEOA Initiative</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<h1 class="header-title">TEOA Procurement Idea Hub</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p class="header-subtitle">Welcome back, <span class="header-name">{user_name}</span> 👋</p>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # KPI CARDS
    kpi_cols = st.columns(4, gap="medium")

    with kpi_cols[0]:
        st.markdown('<div class="kpi-card purple">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="kpi-number">{stats.get("total", 0)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="kpi-label">📊 Total Ideas</div>', unsafe_allow_html=True
        )
        st.markdown('<div class="kpi-sub">All time</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with kpi_cols[1]:
        st.markdown('<div class="kpi-card green">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="kpi-number">{stats.get("this_month", 0)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="kpi-label">📅 This Month</div>', unsafe_allow_html=True
        )
        st.markdown('<div class="kpi-sub">Keep it up!</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with kpi_cols[2]:
        st.markdown('<div class="kpi-card orange">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="kpi-number">{stats.get("this_year", 0)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="kpi-label">📆 This Year</div>', unsafe_allow_html=True)
        st.markdown('<div class="kpi-sub">Happy year!</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with kpi_cols[3]:
        st.markdown('<div class="kpi-card pink">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="kpi-number">{user_idea_count}</div>', unsafe_allow_html=True
        )
        st.markdown(
            '<div class="kpi-label">🏆 Your Ideas</div>', unsafe_allow_html=True
        )
        st.markdown('<div class="kpi-sub">Great job!</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # QUICK STATS ROW
    st.markdown('<div class="quick-stats">', unsafe_allow_html=True)
    q_cols = st.columns([1, 1, 1], gap="medium")

    with q_cols[0]:
        st.markdown(
            f"""
            <div style="text-align:center;">
                <div class="stat-value">{stats.get("this_week", 0)}</div>
                <div class="stat-label">📅 This Week</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with q_cols[1]:
        st.markdown(
            f"""
            <div style="text-align:center;">
                <div class="stat-value">{stats.get("pending", 0)}</div>
                <div class="stat-label">⏳ Pending Review</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with q_cols[2]:
        st.markdown(
            f"""
            <div style="text-align:center;">
                <div class="stat-value">{stats.get("implemented", 0)}</div>
                <div class="stat-label">✅ Implemented</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # MAIN CONTENT - 2 columns
    left_col, right_col = st.columns([1, 1], gap="medium")

    with left_col:
        # WHY SHARE CARD
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-title">💡 Why Share Ideas?</div>', unsafe_allow_html=True
        )
        st.markdown(
            """
            <ul class="why-list">
                <li><span class="why-icon">🚀</span> Drive operational excellence</li>
                <li><span class="why-icon">🎯</span> Make meaningful impact</li>
                <li><span class="why-icon">🤝</span> Collaborate with teams</li>
                <li><span class="why-icon">💡</span> Every idea matters</li>
            </ul>
        """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # BENEFITS CARD
        st.markdown(
            '<div class="card" style="margin-top:16px;">', unsafe_allow_html=True
        )
        st.markdown('<div class="card-title">✨ Benefits</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="benefits-grid">
                <div class="benefit-item"><span class="benefit-check">✓</span> Quick and easy submission</div>
                <div class="benefit-item"><span class="benefit-check">✓</span> Track your idea's progress</div>
                <div class="benefit-item"><span class="benefit-check">✓</span> Collaborate with teams</div>
            </div>
        """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        # TOP BU CARD
        if top_bu:
            st.markdown('<div class="topbu-card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="topbu-label">🏆 TOP BU THIS MONTH</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="topbu-name">{top_bu.get("bu_cl_site", "N/A")}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="topbu-count">{top_bu.get("count", 0)}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="topbu-text">ideas submitted</div>', unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="topbu-card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="topbu-label">🏆 TOP BU THIS MONTH</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="topbu-name">No data yet</div>', unsafe_allow_html=True
            )
            st.markdown('<div class="topbu-count">—</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="topbu-text">Start submitting ideas!</div>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # CTA CARD
        st.markdown(
            """
            <div class="cta-card">
                <div class="cta-title">💬 Have an idea?</div>
                <div class="cta-text">Submit your idea and shape the future!</div>
            </div>
        """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    render()
