import streamlit as st
from database import get_stats, get_user_ideas, get_top_contributors_per_bu

# Page config
st.set_page_config(layout="wide")

# Custom CSS for card styling (NOT layout)
st.markdown(
    """
<style>
    /* Header styling */
    .header-tag {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #1a1a2e;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
        display: inline-block;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    .header-title {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 10px 0 5px 0;
        line-height: 1.3;
    }
    
    .header-subtitle {
        font-size: 18px;
        color: #64748b;
        margin: 0;
    }
    
    .header-name {
        color: #667eea;
        font-weight: 600;
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid #f1f5f9;
        height: 100%;
    }
    
    .card-highlight {
        background: linear-gradient(135deg, #FF6B35, #FFA07A, #FF8C00);
        border: none;
        box-shadow: 0 10px 30px rgba(255, 107, 53, 0.4);
    }
    
    .card-title {
        font-size: 18px;
        font-weight: 700;
        color: #2d3436;
        margin-bottom: 15px;
    }
    
    .card-highlight .card-title {
        color: white;
    }
    
    /* KPI styling */
    .kpi-card {
        background: white;
        border-radius: 16px;
        padding: 20px 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid #f1f5f9;
        text-align: center;
    }
    
    .kpi-number {
        font-size: 42px;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 5px;
    }
    
    .kpi-label {
        font-size: 14px;
        font-weight: 600;
        color: #64748b;
    }
    
    .kpi-sub {
        font-size: 12px;
        color: #94a3b8;
        margin-top: 3px;
    }
    
    /* Top BU styling */
    .topbu-label {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        opacity: 0.9;
        margin-bottom: 10px;
    }
    
    .topbu-name {
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 5px;
    }
    
    .topbu-count {
        font-size: 48px;
        font-weight: 800;
        line-height: 1;
    }
    
    .topbu-text {
        font-size: 14px;
        opacity: 0.9;
    }
    
    /* Why share items */
    .why-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 0;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .why-item:last-child {
        border-bottom: none;
    }
    
    .why-icon {
        font-size: 24px;
    }
    
    .why-text {
        font-size: 15px;
        color: #475569;
    }
    
    /* CTA styling */
    .cta-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 16px;
        padding: 25px;
        color: white;
        text-align: center;
        margin-top: 15px;
    }
    
    .cta-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .cta-text {
        font-size: 14px;
        opacity: 0.95;
        line-height: 1.5;
    }
    
    /* Benefits styling */
    .benefits-card {
        background: white;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid #f1f5f9;
    }
    
    .benefit-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 0;
    }
    
    .benefit-check {
        color: #10b981;
        font-size: 18px;
        font-weight: 700;
    }
    
    .benefit-text {
        font-size: 14px;
        color: #475569;
    }
    
    /* Motivation banner */
    .motivation-banner {
        background: linear-gradient(135deg, #1e3a5f, #3b82f6);
        border-radius: 12px;
        padding: 18px 25px;
        color: white;
        text-align: center;
        margin: 20px 0;
    }
    
    .motivation-text {
        font-size: 16px;
        margin: 0;
        font-weight: 500;
    }
    
    /* Section title */
    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #2d3436;
        margin-bottom: 15px;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .header-title {
            font-size: 24px;
        }
        
        .kpi-number {
            font-size: 32px;
        }
        
        .topbu-name {
            font-size: 22px;
        }
        
        .topbu-count {
            font-size: 38px;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)


def render():
    # Get data
    stats = get_stats()
    user_ideas = get_user_ideas(st.session_state.user_id)
    user_idea_count = len(user_ideas) if user_ideas else 0
    top_bu = get_top_contributors_per_bu()

    # ============================================
    # HEADER SECTION
    # ============================================
    with st.container():
        st.markdown(
            '<div class="header-tag">✨ TEOA Initiative</div>', unsafe_allow_html=True
        )
        st.markdown(
            f'<h1 class="header-title">Welcome to TEOA Procurement Idea Hub</h1>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<p class="header-subtitle">Hello <span class="header-name">{st.session_state.full_name or st.session_state.username}</span> 👋</p>',
            unsafe_allow_html=True,
        )

    st.divider()

    # ============================================
    # KPI SECTION - 4 cards in a row
    # ============================================
    with st.container():
        cols = st.columns(4)

        with cols[0]:
            st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="kpi-number" style="color: #667eea;">{stats.get("total", 0)}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="kpi-label">📊 Total Ideas</div>', unsafe_allow_html=True
            )
            st.markdown('<div class="kpi-sub">All time</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with cols[1]:
            st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="kpi-number" style="color: #11998e;">{stats.get("this_month", 0)}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="kpi-label">📅 This Month</div>', unsafe_allow_html=True
            )
            st.markdown(
                '<div class="kpi-sub">Keep it up!</div>', unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with cols[2]:
            st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="kpi-number" style="color: #f97316;">{stats.get("this_year", 0)}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="kpi-label">📆 This Year</div>', unsafe_allow_html=True
            )
            st.markdown(
                '<div class="kpi-sub">Happy year!</div>', unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with cols[3]:
            st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="kpi-number" style="color: #ec008c;">{user_idea_count}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="kpi-label">🏆 Your Ideas</div>', unsafe_allow_html=True
            )
            st.markdown('<div class="kpi-sub">Great job!</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # ============================================
    # MAIN CONTENT - 2 columns
    # ============================================
    with st.container():
        left_col, right_col = st.columns([1, 1], gap="medium")

        # LEFT COLUMN - Why Share + CTA
        with left_col:
            # Why Share Card
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="card-title">💡 Why Share Your Ideas?</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="why-item">
                    <span class="why-icon">🚀</span>
                    <span class="why-text">Drive operational excellence</span>
                </div>
                <div class="why-item">
                    <span class="why-icon">🎯</span>
                    <span class="why-text">Make meaningful impact</span>
                </div>
                <div class="why-item">
                    <span class="why-icon">🤝</span>
                    <span class="why-text">Collaborate with teams</span>
                </div>
                <div class="why-item">
                    <span class="why-icon">💡</span>
                    <span class="why-text">Every idea matters</span>
                </div>
            """,
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

            # CTA Card
            st.markdown(
                """
                <div class="cta-card">
                    <div class="cta-title">💬 Have an idea?</div>
                    <div class="cta-text">This is the place to share it. Great ideas can come from anywhere — and so can you!</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        # RIGHT COLUMN - Top BU (Highlighted)
        with right_col:
            if top_bu:
                st.markdown('<div class="card card-highlight">', unsafe_allow_html=True)
                st.markdown(
                    '<div class="topbu-label">🏆 TOP BU THIS MONTH</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="topbu-name">🥇 {top_bu.get("bu_cl_site", "N/A")}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="topbu-count">{top_bu.get("count", 0)}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<div class="topbu-text">ideas submitted</div>',
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown('<div class="card card-highlight">', unsafe_allow_html=True)
                st.markdown(
                    '<div class="topbu-label">🏆 TOP BU THIS MONTH</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<div class="topbu-name">🥇 No data yet</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<div class="topbu-text">Start submitting ideas!</div>',
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)

    # ============================================
    # MOTIVATION BANNER
    # ============================================
    with st.container():
        st.markdown(
            """
            <div class="motivation-banner">
                <p class="motivation-text">⭐ Your ideas are reviewed weekly — your thoughts matter and are valued!</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.divider()

    # ============================================
    # BENEFITS SECTION - 3 columns
    # ============================================
    with st.container():
        st.markdown(
            '<div class="section-title">✨ Benefits</div>', unsafe_allow_html=True
        )

        benefit_cols = st.columns(3)

        with benefit_cols[0]:
            st.markdown('<div class="benefits-card">', unsafe_allow_html=True)
            st.markdown(
                """
                <div class="benefit-item">
                    <span class="benefit-check">✓</span>
                    <span class="benefit-text">Quick and easy submission process</span>
                </div>
            """,
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with benefit_cols[1]:
            st.markdown('<div class="benefits-card">', unsafe_allow_html=True)
            st.markdown(
                """
                <div class="benefit-item">
                    <span class="benefit-check">✓</span>
                    <span class="benefit-text">Track your idea's progress</span>
                </div>
            """,
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with benefit_cols[2]:
            st.markdown('<div class="benefits-card">', unsafe_allow_html=True)
            st.markdown(
                """
                <div class="benefit-item">
                    <span class="benefit-check">✓</span>
                    <span class="benefit-text">Collaborate and engage with teams</span>
                </div>
            """,
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    render()
