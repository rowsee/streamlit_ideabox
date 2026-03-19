import streamlit as st
from database import get_stats, get_user_ideas, get_top_contributors_per_bu

st.markdown(
    """
<style>
    .stat-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 25px 30px;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
    }
    .stat-card.green {
        background: linear-gradient(135deg, #00b894, #00a085);
        box-shadow: 0 6px 20px rgba(0, 184, 148, 0.3);
    }
    .stat-card.pink {
        background: linear-gradient(135deg, #fd79a8, #e84393);
        box-shadow: 0 6px 20px rgba(253, 121, 168, 0.3);
    }
    .stat-number {
        font-size: 52px;
        font-weight: 700;
        margin-bottom: 8px;
        line-height: 1;
    }
    .stat-label {
        font-size: 15px;
        opacity: 0.95;
        font-weight: 600;
    }
    .stat-sub {
        font-size: 12px;
        opacity: 0.8;
        margin-top: 5px;
    }
    .top-bu-card {
        background: linear-gradient(135deg, #FF6B35, #FF8F5E);
        padding: 18px 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.25);
    }
    .top-bu-label {
        font-size: 13px;
        opacity: 0.9;
        font-weight: 500;
        margin-bottom: 5px;
    }
    .top-bu-name {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 3px;
    }
    .top-bu-count {
        font-size: 14px;
        opacity: 0.95;
    }
    .motivation-banner {
        background: linear-gradient(135deg, #1E3A5F, #2D5A87);
        padding: 16px 24px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 15px 0;
    }
    .motivation-banner p {
        font-size: 16px;
        margin: 0;
        font-weight: 500;
    }
    .feature-card {
        background: #ffffff;
        padding: 18px 20px;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
        border: 1px solid #e8e8e8;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .feature-icon {
        font-size: 28px;
    }
    .feature-title {
        font-size: 16px;
        margin-bottom: 3px;
        color: #2d3436;
        font-weight: 600;
    }
    .feature-desc {
        font-size: 13px;
        line-height: 1.4;
        color: #636e72;
        margin: 0;
    }
    .highlight-box {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 18px 22px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .highlight-box p {
        font-size: 15px;
        line-height: 1.5;
        margin: 0;
        font-weight: 400;
    }
    .check-item {
        display: flex;
        align-items: center;
        gap: 5px;
        color: #636e72;
        font-size: 13px;
    }
    .check-item span {
        color: #00b894;
        font-weight: 700;
    }
    .tag {
        background: #FFD700;
        color: #2d3436;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 15px;
    }
    .small-feature-card {
        background: #ffffff;
        padding: 14px 16px;
        border-radius: 10px;
        box-shadow: 0 1px 8px rgba(0, 0, 0, 0.05);
        border: 1px solid #e8e8e8;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .small-feature-icon {
        font-size: 24px;
    }
    .small-feature-title {
        font-size: 14px;
        margin-bottom: 2px;
        color: #2d3436;
        font-weight: 600;
    }
    .small-feature-desc {
        font-size: 12px;
        line-height: 1.3;
        color: #636e72;
        margin: 0;
    }
</style>
""",
    unsafe_allow_html=True,
)


def render():
    stats = get_stats()
    user_ideas = get_user_ideas(st.session_state.user_id)
    user_idea_count = len(user_ideas) if user_ideas else 0
    top_bu = get_top_contributors_per_bu()

    st.markdown('<div class="tag">✨ TEOA Initiative</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
    <h1 style="font-size: 38px; font-weight: 700; margin-bottom: 10px; line-height: 1.2; color: #2d3436;">
        Welcome to TEOA Ideabox,<br>
        <span style="color: #667eea;">{st.session_state.full_name or st.session_state.username} 👋</span>
    </h1>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Stats Section - Larger cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-number">{stats["total"]}</div>
            <div class="stat-label">📊 Total Ideas</div>
            <div class="stat-sub">All time</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="stat-card green">
            <div class="stat-number">{stats["this_month"]}</div>
            <div class="stat-label">📅 This Month</div>
            <div class="stat-sub">Keep it up!</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="stat-card pink">
            <div class="stat-number">{user_idea_count}</div>
            <div class="stat-label">🏆 Your Ideas</div>
            <div class="stat-sub">Great job!</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Motivation Banner - "Ideas reviewed weekly"
    st.markdown(
        f"""
    <div class="motivation-banner">
        <p>⭐ Your ideas are reviewed weekly — your thoughts matter and are valued!</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Top BU Section
    if top_bu:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            pass
        with col2:
            st.markdown(
                f"""
            <div class="top-bu-card">
                <div class="top-bu-label">🏆 Top BU This Month</div>
                <div class="top-bu-name">{top_bu["bu_cl_site"]}</div>
                <div class="top-bu-count">{top_bu["count"]} ideas submitted</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with col3:
            pass

    st.markdown("---")

    # Why Share Your Ideas - Smaller section at bottom
    st.markdown("### Why Share Your Ideas?", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
        <div class="small-feature-card">
            <div class="small-feature-icon">💡</div>
            <div>
                <div class="small-feature-title">Share Your Ideas</div>
                <div class="small-feature-desc">Every idea matters and can make a difference.</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="small-feature-card">
            <div class="small-feature-icon">🚀</div>
            <div>
                <div class="small-feature-title">Drive Excellence</div>
                <div class="small-feature-desc">Help enhance operations through your perspective.</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div class="small-feature-card">
            <div class="small-feature-icon">🎯</div>
            <div>
                <div class="small-feature-title">Make Impact</div>
                <div class="small-feature-desc">See your ideas come to life and create change.</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
