import streamlit as st
from database import get_stats, get_user_ideas, get_top_contributors_per_bu

st.markdown(
    """
<style>
    /* Reset and Base Styles */
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }
    
    /* Centered Page Container */
    .page-wrapper {
        max-width: 950px;
        margin: 0 auto;
        padding: 30px 20px;
    }
    
    /* Futuristic Glow Animation */
    @keyframes glow-pulse {
        0%, 100% { box-shadow: 0 0 25px rgba(255, 107, 53, 0.5), 0 0 50px rgba(255, 107, 53, 0.25); }
        50% { box-shadow: 0 0 35px rgba(255, 107, 53, 0.7), 0 0 70px rgba(255, 107, 53, 0.35); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Tag Badge */
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
    
    /* Header Section */
    .header-section {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .header-title {
        font-size: 38px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
        line-height: 1.2;
    }
    
    .header-subtitle {
        font-size: 20px;
        color: #64748b;
        font-weight: 400;
    }
    
    .header-name {
        color: #667eea;
        font-weight: 600;
    }
    
    /* Top BU Card - Centered */
    .top-bu-wrapper {
        display: flex;
        justify-content: center;
        margin: 30px 0;
    }
    
    .top-bu-card {
        background: linear-gradient(135deg, #FF6B35, #FFA07A, #FF8C00);
        padding: 30px 60px;
        border-radius: 20px;
        color: white;
        text-align: center;
        animation: glow-pulse 3s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    .top-bu-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 3s infinite;
    }
    
    .top-bu-label {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        opacity: 0.95;
        margin-bottom: 12px;
    }
    
    .top-bu-name {
        font-size: 44px;
        font-weight: 800;
        margin-bottom: 8px;
        text-shadow: 2px 3px 6px rgba(0,0,0,0.2);
    }
    
    .top-bu-count {
        font-size: 18px;
        font-weight: 600;
        opacity: 0.95;
    }
    
    /* KPI Cards Section */
    .kpi-section {
        display: flex;
        justify-content: center;
        gap: 25px;
        margin: 35px 0;
    }
    
    .kpi-card {
        flex: 1;
        max-width: 280px;
        padding: 35px 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px) scale(1.02);
    }
    
    .kpi-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shimmer 4s infinite;
    }
    
    .kpi-card.purple {
        background: linear-gradient(135deg, #667eea, #764ba2);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    .kpi-card.green {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        box-shadow: 0 10px 30px rgba(17, 153, 142, 0.4);
    }
    
    .kpi-card.pink {
        background: linear-gradient(135deg, #ec008c, #fc6767);
        box-shadow: 0 10px 30px rgba(236, 0, 140, 0.4);
    }
    
    .kpi-number {
        font-size: 58px;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 12px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.15);
        position: relative;
        z-index: 1;
    }
    
    .kpi-label {
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 6px;
        position: relative;
        z-index: 1;
    }
    
    .kpi-sub {
        font-size: 13px;
        opacity: 0.85;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    /* Info Banner - Centered */
    .banner-wrapper {
        display: flex;
        justify-content: center;
        margin: 30px 0;
    }
    
    .info-banner {
        background: linear-gradient(135deg, #1e3a5f, #3b82f6, #6366f1);
        padding: 20px 40px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.35);
        max-width: 700px;
    }
    
    .info-banner p {
        font-size: 18px;
        margin: 0;
        font-weight: 500;
    }
    
    /* Why Share Section */
    .why-section-title {
        text-align: center;
        font-size: 26px;
        font-weight: 700;
        color: #2d3436;
        margin: 40px 0 25px 0;
    }
    
    .why-section {
        display: flex;
        justify-content: center;
        gap: 25px;
        margin-bottom: 40px;
    }
    
    .why-card {
        flex: 1;
        max-width: 280px;
        padding: 40px 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        transition: all 0.4s ease;
        cursor: pointer;
    }
    
    .why-card:hover {
        transform: translateY(-10px);
    }
    
    .why-card.blue {
        background: linear-gradient(135deg, #667eea, #764ba2);
        box-shadow: 0 10px 35px rgba(102, 126, 234, 0.4);
    }
    
    .why-card.blue:hover {
        box-shadow: 0 15px 45px rgba(102, 126, 234, 0.5);
    }
    
    .why-card.orange {
        background: linear-gradient(135deg, #f97316, #fb923c);
        box-shadow: 0 10px 35px rgba(249, 115, 22, 0.4);
    }
    
    .why-card.orange:hover {
        box-shadow: 0 15px 45px rgba(249, 115, 22, 0.5);
    }
    
    .why-card.teal {
        background: linear-gradient(135deg, #14b8a6, #2dd4bf);
        box-shadow: 0 10px 35px rgba(20, 184, 166, 0.4);
    }
    
    .why-card.teal:hover {
        box-shadow: 0 15px 45px rgba(20, 184, 166, 0.5);
    }
    
    .why-icon {
        font-size: 50px;
        margin-bottom: 18px;
        animation: float 3s ease-in-out infinite;
    }
    
    .why-card:nth-child(2) .why-icon { animation-delay: 0.3s; }
    .why-card:nth-child(3) .why-icon { animation-delay: 0.6s; }
    
    .why-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .why-desc {
        font-size: 14px;
        opacity: 0.9;
        line-height: 1.6;
    }
    
    /* Bottom Section - Benefits & Encouragement */
    .bottom-section {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin: 30px 0;
    }
    
    .benefits-card {
        flex: 1;
        max-width: 420px;
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
        border: 1px solid #f1f5f9;
    }
    
    .benefits-title {
        font-size: 22px;
        font-weight: 700;
        color: #2d3436;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .benefit-item {
        display: flex;
        align-items: center;
        gap: 14px;
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
        font-size: 16px;
        color: #475569;
    }
    
    .encouragement-card {
        flex: 1;
        max-width: 420px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 30px;
        border-radius: 20px;
        color: white;
        box-shadow: 0 10px 35px rgba(102, 126, 234, 0.4);
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .encouragement-icon {
        font-size: 45px;
        margin-bottom: 15px;
    }
    
    .encouragement-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 12px;
    }
    
    .encouragement-text {
        font-size: 16px;
        line-height: 1.7;
        opacity: 0.95;
    }
    
    /* Divider */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 40px 0;
    }
    
    /* Responsive */
    @media (max-width: 900px) {
        .kpi-section, .why-section, .bottom-section {
            flex-direction: column;
            align-items: center;
        }
        
        .kpi-card, .why-card, .benefits-card, .encouragement-card {
            max-width: 100%;
            width: 100%;
        }
        
        .top-bu-card {
            padding: 25px 40px;
        }
        
        .top-bu-name {
            font-size: 36px;
        }
        
        .kpi-number {
            font-size: 48px;
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
    st.markdown('<div class="header-section">', unsafe_allow_html=True)
    st.markdown('<div class="tag">✨ TEOA Initiative</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <h1 class="header-title">Welcome to TEOA Procurement Idea Hub</h1>
        <p class="header-subtitle">
            Hello <span class="header-name">{st.session_state.full_name or st.session_state.username}</span> 👋
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Top BU Section - Centered
    if top_bu:
        st.markdown('<div class="top-bu-wrapper">', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="top-bu-card">
                <div class="top-bu-label">🏆 TOP BU THIS MONTH</div>
                <div class="top-bu-name">{top_bu["bu_cl_site"]}</div>
                <div class="top-bu-count">{top_bu["count"]} ideas submitted</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # KPI Cards - Centered
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
        <div class="kpi-card pink">
            <div class="kpi-number">{user_idea_count}</div>
            <div class="kpi-label">🏆 Your Ideas</div>
            <div class="kpi-sub">Great job!</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Info Banner - Centered
    st.markdown('<div class="banner-wrapper">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="info-banner">
            <p>⭐ Your ideas are reviewed weekly — your thoughts matter and are valued!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Why Share Your Ideas - Centered
    st.markdown(
        '<div class="why-section-title">Why Share Your Ideas?</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="why-section">', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="why-card blue">
            <div class="why-icon">💡</div>
            <div class="why-title">Share Your Ideas</div>
            <div class="why-desc">Every idea matters and can make a real difference in how we work together.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="why-card orange">
            <div class="why-icon">🚀</div>
            <div class="why-title">Drive Excellence</div>
            <div class="why-desc">Help enhance operational excellence through your unique perspective.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="why-card teal">
            <div class="why-icon">🎯</div>
            <div class="why-title">Make Impact</div>
            <div class="why-desc">See your ideas come to life and create meaningful change for everyone.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Bottom Section - Centered
    st.markdown('<div class="bottom-section">', unsafe_allow_html=True)

    # Benefits
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

    # Encouragement
    st.markdown(
        """
        <div class="encouragement-card">
            <div class="encouragement-icon">💬</div>
            <div class="encouragement-title">Have an idea?</div>
            <div class="encouragement-text">This is the place to share it. Great ideas can come from anywhere — and so can you!</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Close Container
    st.markdown("</div>", unsafe_allow_html=True)
