import streamlit as st
from database import (
    get_stats,
    get_user_ideas,
    get_top_contributors_per_bu,
    get_top_contributor,
)
from streamlit_extras.metric_cards import style_metric_cards

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
        padding: 28px 32px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        margin-bottom: 24px;
    }

    .header-badge {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #1a1a2e;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        display: inline-block;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 14px;
    }

    .header-title {
        font-size: 32px;
        font-weight: 900;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 10px 0;
        line-height: 1.2;
    }

    .header-subtitle {
        font-size: 22px;
        color: #64748b;
        margin: 0;
        line-height: 1.4;
    }

    .header-name {
        color: #f97316;
        font-weight: 700;
        font-size: 24px;
    }

    .highlight-card {
        background: white;
        border-radius: 16px;
        padding: 32px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .highlight-card.orange {
        background: linear-gradient(135deg, #f97316, #fb923c);
        border: none;
    }

    .highlight-card.purple {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border: none;
    }

    .highlight-label {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        opacity: 0.9;
        margin-bottom: 16px;
    }

    .highlight-icon {
        font-size: 36px;
        margin-bottom: 14px;
    }

    .highlight-name {
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 18px;
        background: rgba(255, 255, 255, 0.25);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
    }

    .highlight-count {
        font-size: 80px;
        font-weight: 800;
        line-height: 1;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.3));
    }

    .highlight-text {
        font-size: 15px;
        opacity: 0.9;
        margin-top: 10px;
        font-weight: 600;
    }

    .kpi-card {
        background: white;
        border-radius: 14px;
        padding: 20px 18px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.06);
        border: 1px solid #f1f5f9;
        border-left: 5px solid;
        height: 100%;
        transition: all 0.3s ease;
    }

    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.1);
    }

    .kpi-card.purple { border-left-color: #8b5cf6; }
    .kpi-card.green { border-left-color: #10b981; }
    .kpi-card.orange { border-left-color: #f97316; }
    .kpi-card.pink { border-left-color: #ec4899; }

    .kpi-number {
        font-size: 42px;
        font-weight: 800;
        color: #1e293b;
        line-height: 1;
        margin-bottom: 8px;
    }

    .kpi-label {
        font-size: 14px;
        font-weight: 700;
        color: #475569;
        margin-bottom: 6px;
    }

    .kpi-sub {
        font-size: 12px;
        color: #94a3b8;
    }

    .card {
        background: white;
        border-radius: 14px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
        height: 100%;
    }

    .card-title {
        font-size: 17px;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .why-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .why-list li {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 0;
        border-bottom: 1px solid #f1f5f9;
        font-size: 15px;
        color: #475569;
        line-height: 1.4;
    }

    .why-list li:last-child {
        border-bottom: none;
    }

    .why-icon {
        font-size: 20px;
    }

    .benefits-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 12px;
        margin-top: 18px;
    }

    .benefit-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 14px;
        background: #f8fafc;
        border-radius: 10px;
        font-size: 14px;
        color: #475569;
        line-height: 1.4;
    }

    .benefit-check {
        color: #10b981;
        font-weight: 700;
        font-size: 18px;
    }

    .cta-card {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-radius: 16px;
        padding: 28px;
        color: white;
        text-align: center;
        margin-top: 24px;
    }

    .cta-title {
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .cta-text {
        font-size: 14px;
        opacity: 0.95;
    }

    .cta-sub {
        font-size: 12px;
        opacity: 0.8;
        margin-top: 10px;
    }

    .stDivider { margin: 24px 0; }
</style>
""",
    unsafe_allow_html=True,
)


def render():
    stats = get_stats() or {}
    top_bu = get_top_contributors_per_bu() or {}
    top_contributor = get_top_contributor() or {}
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
        f'<p class="header-subtitle">Welcome, <span class="header-name">{user_name}</span> 👋</p>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # TOP BU + TOP CONTRIBUTOR ROW
    top_row_cols = st.columns(2, gap="medium")

    with top_row_cols[0]:
        if top_bu:
            st.markdown('<div class="highlight-card orange">', unsafe_allow_html=True)
            st.markdown('<div class="highlight-icon">🏆</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="highlight-label">TOP BU THIS MONTH</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="highlight-name">{top_bu.get("bu_cl_site", "N/A")}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="highlight-count">{top_bu.get("count", 0)}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="highlight-text">ideas submitted</div>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="highlight-card orange">', unsafe_allow_html=True)
            st.markdown('<div class="highlight-icon">🏆</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="highlight-label">TOP BU THIS MONTH</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="highlight-name">No data yet</div>', unsafe_allow_html=True
            )
            st.markdown('<div class="highlight-count">—</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="highlight-text">Start submitting ideas!</div>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

    with top_row_cols[1]:
        if top_contributor:
            st.markdown('<div class="highlight-card purple">', unsafe_allow_html=True)
            st.markdown('<div class="highlight-icon">👤</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="highlight-label">TOP CONTRIBUTOR THIS MONTH</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="highlight-name">{top_contributor.get("name", "N/A")}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="highlight-count">{top_contributor.get("count", 0)}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="highlight-text">ideas submitted</div>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="highlight-card purple">', unsafe_allow_html=True)
            st.markdown('<div class="highlight-icon">👤</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="highlight-label">TOP CONTRIBUTOR THIS MONTH</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="highlight-name">No data yet</div>', unsafe_allow_html=True
            )
            st.markdown('<div class="highlight-count">—</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="highlight-text">Be the first to contribute!</div>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # KPI CARDS (using st.metric with streamlit-extras styling)
    kpi_cols = st.columns(4, gap="medium")

    with kpi_cols[0]:
        st.metric(label="Total Ideas", value=stats.get("total", 0))

    with kpi_cols[1]:
        st.metric(label="This Month", value=stats.get("this_month", 0))

    with kpi_cols[2]:
        st.metric(label="This Year", value=stats.get("this_year", 0))

    with kpi_cols[3]:
        st.metric(label="Your Ideas", value=user_idea_count)

    # Apply styling to metric cards
    style_metric_cards(
        background_color="#ffffff",
        border_size_px=1,
        border_color="#e2e8f0",
        border_radius_px=14,
    )

    st.divider()

    # WHY SHARE + BENEFITS ROW
    bottom_cols = st.columns(2, gap="medium")

    with bottom_cols[0]:
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

    with bottom_cols[1]:
        # BENEFITS CARD
        st.markdown('<div class="card">', unsafe_allow_html=True)
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

    st.divider()

    # CTA CARD (FULL WIDTH AT BOTTOM) WITH "IDEAS REVIEWED WEEKLY"
    st.markdown(
        """
        <div class="cta-card" style="max-width:600px;margin:0 auto;">
            <div class="cta-title">💬 Have an idea?</div>
            <div class="cta-text">Submit your idea and shape the future!</div>
            <div class="cta-sub">📅 Ideas reviewed weekly</div>
        </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    render()
