import streamlit as st
from database import get_stats, get_user_ideas, get_top_contributors_per_bu

st.markdown(
    """
<style>
    /* Override Streamlit main container to center content */
    .stApp > div[data-testid="stMainBlockContainer"] {
        max-width: 1000px !important;
        margin: 0 auto !important;
        padding: 20px 20px !important;
    }
    
    /* Page wrapper */
    .page-wrapper {
        width: 100%;
        max-width: 1000px;
        margin: 0 auto;
        text-align: center;
    }
    
    /* Header Section */
    .tag {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #1a1a2e;
        padding: 8px 18px;
        border-radius: 25px;
        font-size: 14px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 20px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    .header-title {
        font-size: 36px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 15px;
        line-height: 1.3;
    }
    
    .header-subtitle {
        font-size: 20px;
        color: #475569;
        font-weight: 500;
        margin-bottom: 30px;
    }
    
    .header-name {
        color: #667eea;
        font-weight: 700;
    }
    
    /* CTA Card */
    .cta-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 30px 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 25px auto;
        max-width: 800px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.35);
    }
    
    .cta-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .cta-text {
        font-size: 16px;
        line-height: 1.6;
        opacity: 0.95;
    }
    
    /* KPI Section */
    .kpi-section {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 30px auto;
        flex-wrap: wrap;
        max-width: 900px;
    }
    
    .kpi-card {
        flex: 1;
        min-width: 180px;
        max-width: 220px;
        padding: 25px 15px;
        border-radius: 16px;
        color: white;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
    }
    
    .kpi-card.purple {
        background: linear-gradient(135deg, #667eea, #764ba2);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .kpi-card.green {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        box-shadow: 0 8px 25px rgba(17, 153, 142, 0.4);
    }
    
    .kpi-card.orange {
        background: linear-gradient(135deg, #f97316, #fbbf24);
        box-shadow: 0 8px 25px rgba(249, 115, 22, 0.4);
    }
    
    .kpi-card.pink {
        background: linear-gradient(135deg, #ec008c, #fc6767);
        box-shadow: 0 8px 25px rgba(236, 0, 140, 0.4);
    }
    
    .kpi-number {
        font-size: 48px;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 8px;
    }
    
    .kpi-label {
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 4px;
    }
    
    .kpi-sub {
        font-size: 12px;
        opacity: 0.85;
    }
    
    /* Top BU Section */
    .top-bu-section {
        margin: 40px auto;
    }
    
    .top-bu-card {
        background: linear-gradient(135deg, #FF6B35, #FFA07A, #FF8C00);
        padding: 35px 50px;
        border-radius: 24px;
        color: white;
        text-align: center;
        max-width: 500px;
        margin: 0 auto;
        box-shadow: 0 15px 50px rgba(255, 107, 53, 0.4);
        border: 3px solid rgba(255, 255, 255, 0.3);
        animation: glow-pulse 3s ease-in-out infinite;
    }
    
    @keyframes glow-pulse {
        0%, 100% { box-shadow: 0 0 30px rgba(255, 107, 53, 0.5), 0 0 60px rgba(255, 107, 53, 0.25); }
        50% { box-shadow: 0 0 40px rgba(255, 107, 53, 0.7), 0 0 80px rgba(255, 107, 53, 0.35); }
    }
    
    .top-bu-label {
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        opacity: 0.9;
        margin-bottom: 15px;
    }
    
    .top-bu-name {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 10px;
        text-shadow: 2px 3px 6px rgba(0, 0, 0, 0.2);
    }
    
    .top-bu-number {
        font-size: 56px;
        font-weight: 800;
        line-height: 1;
    }
    
    .top-bu-text {
        font-size: 18px;
        font-weight: 500;
        margin-top: 5px;
        opacity: 0.95;
    }
    
    /* Motivation Banner */
    .motivation-banner {
        background: linear-gradient(135deg, #1e3a5f, #3b82f6, #6366f1);
        padding: 22px 30px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin: 35px auto;
        max-width: 700px;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
    }
    
    .motivation-banner p {
        font-size: 18px;
        margin: 0;
        font-weight: 500;
        line-height: 1.5;
    }
    
    /* Why Share Card */
    .why-share-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
        border: 1px solid #f1f5f9;
        margin: 30px auto;
        max-width: 900px;
    }
    
    .why-share-title {
        font-size: 26px;
        font-weight: 700;
        color: #2d3436;
        margin-bottom: 25px;
        text-align: center;
    }
    
    .why-cards {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
    }
    
    .why-card {
        flex: 1;
        min-width: 200px;
        max-width: 260px;
        padding: 30px 20px;
        border-radius: 16px;
        color: white;
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .why-card:hover {
        transform: translateY(-8px);
    }
    
    .why-card.blue {
        background: linear-gradient(135deg, #3b82f6, #60a5fa);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
    }
    
    .why-card.red {
        background: linear-gradient(135deg, #ef4444, #f87171);
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.4);
    }
    
    .why-card.green {
        background: linear-gradient(135deg, #22c55e, #4ade80);
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.4);
    }
    
    .why-icon {
        font-size: 45px;
        margin-bottom: 15px;
    }
    
    .why-card-title {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .why-card-desc {
        font-size: 13px;
        opacity: 0.9;
        line-height: 1.5;
    }
    
    /* Benefits Card */
    .benefits-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
        border: 1px solid #f1f5f9;
        margin: 30px auto;
        max-width: 600px;
    }
    
    .benefits-title {
        font-size: 22px;
        font-weight: 700;
        color: #2d3436;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .benefit-item {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 14px 0;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .benefit-item:last-child {
        border-bottom: none;
    }
    
    .benefit-check {
        color: #10b981;
        font-size: 22px;
        font-weight: 800;
    }
    
    .benefit-text {
        font-size: 15px;
        color: #475569;
    }
    
    /* Divider */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 35px auto;
        max-width: 800px;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .kpi-section {
            gap: 15px;
        }
        
        .kpi-card {
            min-width: 140px;
            padding: 20px 10px;
        }
        
        .kpi-number {
            font-size: 38px;
        }
        
        .top-bu-card {
            padding: 25px 30px;
        }
        
        .top-bu-name {
            font-size: 32px;
        }
        
        .top-bu-number {
            font-size: 44px;
        }
        
        .header-title {
            font-size: 28px;
        }
        
        .why-card {
            min-width: 100%;
        }
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

    # Main Container
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)

    # Header Section
    st.markdown('<div class="tag">✨ TEOA Initiative</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <h1 class="header-title">Welcome to TEOA Procurement Idea Hub</h1>
        <p class="header-subtitle">
            Hello <span class="header-name">{st.session_state.full_name or st.session_state.username}</span> 👋👋
        </p>
        """,
        unsafe_allow_html=True,
    )

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

    # KPI Section - 4 Stats
    st.markdown('<div class="kpi-section">', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="kpi-card purple">
            <div class="kpi-number">{stats["total"]}</div>
            <div class="kpi-label">📊 Total Ideas</div>
            <div class="kpi-sub">All time</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="kpi-card green">
            <div class="kpi-number">{stats["this_month"]}</div>
            <div class="kpi-label">📅 This Month</div>
            <div class="kpi-sub">Keep it up!</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="kpi-card orange">
            <div class="kpi-number">{stats["this_year"]}</div>
            <div class="kpi-label">📆 This Year</div>
            <div class="kpi-sub">Happy year!</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="kpi-card pink">
            <div class="kpi-number">{user_idea_count}</div>
            <div class="kpi-label">🏆 Your Ideas</div>
            <div class="kpi-sub">Great job!</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Top BU Section
    if top_bu:
        st.markdown('<div class="top-bu-section">', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="top-bu-card">
                <div class="top-bu-label">🏆 TOP BU THIS MONTH</div>
                <div class="top-bu-name">🥇 {top_bu["bu_cl_site"]}</div>
                <div class="top-bu-number">{top_bu["count"]}</div>
                <div class="top-bu-text">ideas submitted</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Motivation Banner
    st.markdown(
        """
        <div class="motivation-banner">
            <p>⭐ Your ideas are reviewed weekly — your thoughts matter and are valued!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Why Share Your Ideas Card
    st.markdown(
        """
        <div class="why-share-card">
            <div class="why-share-title">Why Share Your Ideas?</div>
            <div class="why-cards">
                <div class="why-card blue">
                    <div class="why-icon">💡</div>
                    <div class="why-card-title">Share Your Ideas</div>
                    <div class="why-card-desc">Every idea matters and can make a real difference.</div>
                </div>
                <div class="why-card red">
                    <div class="why-icon">🚀</div>
                    <div class="why-card-title">Drive Excellence</div>
                    <div class="why-card-desc">Help enhance operations through your perspective.</div>
                </div>
                <div class="why-card green">
                    <div class="why-icon">🎯</div>
                    <div class="why-card-title">Make Impact</div>
                    <div class="why-card-desc">See your ideas come to life and create change.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Benefits Card
    st.markdown(
        """
        <div class="benefits-card">
            <div class="benefits-title">✨ Benefits</div>
            <div class="benefit-item">
                <span class="benefit-check">✓</span>
                <span class="benefit-text">Quick and easy submission process</span>
            </div>
            <div class="benefit-item">
                <span class="benefit-check">✓</span>
                <span class="benefit-text">Track your idea's progress</span>
            </div>
            <div class="benefit-item">
                <span class="benefit-check">✓</span>
                <span class="benefit-text">Collaborate and engage with teams</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Close Container
    st.markdown("</div>", unsafe_allow_html=True)
