import streamlit as st
from database import get_stats, get_user_ideas, get_top_contributors_per_bu

# Page config
st.set_page_config(layout="wide", page_icon="💡")

# Custom CSS for styling (NOT layout)
st.markdown(
    """
<style>
    /* ============================================
       ROOT VARIABLES
       ============================================ */
    :root {
        --bg-main: #f8fafc;
        --bg-card: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --purple-start: #667eea;
        --purple-end: #764ba2;
        --orange-start: #f97316;
        --orange-end: #f59e0b;
        --green-start: #11998e;
        --green-end: #38ef7d;
        --pink-start: #ec008c;
        --pink-end: #fc6767;
        --blue-start: #3b82f6;
        --blue-end: #1e3a5f;
    }
    
    /* ============================================
       MAIN BACKGROUND
       ============================================ */
    .stApp {
        background-color: var(--bg-main);
    }
    
    /* ============================================
       HEADER SECTION
       ============================================ */
    .header-tag {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #1a1a2e;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    
    .header-title {
        font-size: 32px;
        font-weight: 800;
        color: var(--text-primary);
        margin: 0 0 8px 0;
        line-height: 1.2;
    }
    
    .header-subtitle {
        font-size: 16px;
        color: var(--text-secondary);
        margin: 0;
    }
    
    .header-name {
        color: var(--purple-start);
        font-weight: 600;
    }
    
    /* ============================================
       KPI CARDS
       ============================================ */
    .kpi-card {
        background: white;
        border-radius: 16px;
        padding: 20px 16px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    .kpi-card.purple {
        background: linear-gradient(135deg, var(--purple-start), var(--purple-end));
        color: white;
    }
    
    .kpi-card.green {
        background: linear-gradient(135deg, var(--green-start), var(--green-end));
        color: white;
    }
    
    .kpi-card.orange {
        background: linear-gradient(135deg, var(--orange-start), var(--orange-end));
        color: white;
    }
    
    .kpi-card.pink {
        background: linear-gradient(135deg, var(--pink-start), var(--pink-end));
        color: white;
    }
    
    .kpi-number {
        font-size: 42px;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 6px;
    }
    
    .kpi-label {
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 3px;
    }
    
    .kpi-sub {
        font-size: 11px;
        opacity: 0.85;
    }
    
    /* ============================================
       CONTENT CARDS
       ============================================ */
    .content-card {
        background: white;
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(0, 0, 0, 0.04);
        height: 100%;
    }
    
    .card-title {
        font-size: 16px;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* ============================================
       WHY SHARE ITEMS
       ============================================ */
    .why-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .why-item:last-child {
        border-bottom: none;
    }
    
    .why-icon {
        font-size: 22px;
    }
    
    .why-text {
        font-size: 14px;
        color: var(--text-secondary);
    }
    
    /* ============================================
       CTA CARD (PURPLE GRADIENT)
       ============================================ */
    .cta-card {
        background: linear-gradient(135deg, var(--purple-start), var(--purple-end));
        border-radius: 16px;
        padding: 24px;
        color: white;
        text-align: center;
        margin-top: 16px;
    }
    
    .cta-title {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .cta-text {
        font-size: 13px;
        opacity: 0.95;
        line-height: 1.5;
    }
    
    /* ============================================
       TOP BU CARD (ORANGE HIGHLIGHT)
       ============================================ */
    .topbu-card {
        background: linear-gradient(135deg, var(--orange-start), var(--orange-end));
        border-radius: 20px;
        padding: 32px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 30px rgba(249, 115, 22, 0.35);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .topbu-label {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        opacity: 0.95;
        margin-bottom: 12px;
    }
    
    .topbu-name {
        font-size: 26px;
        font-weight: 800;
        margin-bottom: 8px;
    }
    
    .topbu-count {
        font-size: 56px;
        font-weight: 800;
        line-height: 1;
    }
    
    .topbu-text {
        font-size: 14px;
        opacity: 0.9;
        margin-top: 6px;
    }
    
    /* ============================================
       MOTIVATION BANNER
       ============================================ */
    .motivation-banner {
        background: linear-gradient(135deg, var(--blue-start), var(--blue-end));
        border-radius: 12px;
        padding: 18px 24px;
        color: white;
        text-align: center;
    }
    
    .motivation-text {
        font-size: 15px;
        margin: 0;
        font-weight: 500;
    }
    
    /* ============================================
       BENEFITS SECTION
       ============================================ */
    .benefits-card {
        background: white;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(0, 0, 0, 0.04);
        height: 100%;
    }
    
    .benefits-title {
        font-size: 16px;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 14px;
    }
    
    .benefit-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 0;
    }
    
    .benefit-check {
        color: #10b981;
        font-size: 18px;
        font-weight: 700;
    }
    
    .benefit-text {
        font-size: 13px;
        color: var(--text-secondary);
    }
    
    /* ============================================
       SECTION TITLE
       ============================================ */
    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 16px;
    }
    
    /* ============================================
       RESPONSIVE
       ============================================ */
    @media (max-width: 768px) {
        .header-title {
            font-size: 24px;
        }
        
        .kpi-number {
            font-size: 32px;
        }
        
        .topbu-name {
            font-size: 20px;
        }
        
        .topbu-count {
            font-size: 42px;
        }
    }
    
    /* ============================================
       DIVIDER STYLING
       ============================================ */
    .stDivider {
        margin: 24px 0;
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
            '<h1 class="header-title">TEOA Procurement Idea Hub</h1>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<p class="header-subtitle">Welcome back, <span class="header-name">{st.session_state.full_name or st.session_state.username}</span> 👋</p>',
            unsafe_allow_html=True,
        )

    st.divider()

    # ============================================
    # KPI SECTION - 4 cards in a row
    # ============================================
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

    # ============================================
    # MAIN CONTENT - 2 columns
    # ============================================
    left_col, right_col = st.columns([1, 1], gap="medium")

    # LEFT COLUMN
    with left_col:
        # Why Share Card
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-title">💡 Why Share Ideas?</div>', unsafe_allow_html=True
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

    # RIGHT COLUMN - Top BU
    with right_col:
        if top_bu:
            st.markdown('<div class="topbu-card">', unsafe_allow_html=True)
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
                '<div class="topbu-name">🥇 No data yet</div>', unsafe_allow_html=True
            )
            st.markdown('<div class="topbu-count">—</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="topbu-text">Start submitting ideas!</div>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

    # ============================================
    # MOTIVATION BANNER
    # ============================================
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
    # BENEFITS SECTION
    # ============================================
    st.markdown('<div class="section-title">✨ Benefits</div>', unsafe_allow_html=True)

    benefit_cols = st.columns(3, gap="medium")

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
