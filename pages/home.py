import streamlit as st
from database import get_stats, get_user_ideas, get_top_contributors_per_bu

st.markdown(
    """
<style>
    /* ============================================
       HOME PAGE CONTAINER
       ============================================ */
    .home-page {
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px 15px;
    }
    
    /* ============================================
       GLASS CARD BASE CLASS
       With fallbacks for unsupported browsers
       ============================================ */
    .home-glass {
        background: rgba(255, 255, 255, 0.85);
        -webkit-backdrop-filter: blur(10px);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    @supports not (backdrop-filter: blur(10px)) {
        .home-glass {
            background: rgba(255, 255, 255, 0.98);
        }
    }
    
    /* ============================================
       HEADER SECTION
       ============================================ */
    .home-tag {
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
    
    .home-header-title {
        font-size: 36px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb, #667eea);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 12px;
        line-height: 1.3;
        animation: home-gradient 8s ease infinite;
    }
    
    @keyframes home-gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .home-header-subtitle {
        font-size: 20px;
        color: #64748b;
        font-weight: 500;
        margin-bottom: 25px;
    }
    
    .home-header-name {
        color: #667eea;
        font-weight: 700;
    }
    
    /* ============================================
       CTA CARD (Glassmorphism)
       ============================================ */
    .home-cta-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9), rgba(118, 75, 162, 0.9));
        -webkit-backdrop-filter: blur(10px);
        backdrop-filter: blur(10px);
        padding: 30px 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 25px auto;
        max-width: 800px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 
            0 4px 6px rgba(0, 0, 0, 0.05),
            0 10px 20px rgba(102, 126, 234, 0.2),
            0 20px 40px rgba(102, 126, 234, 0.15);
    }
    
    .home-cta-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .home-cta-text {
        font-size: 16px;
        line-height: 1.6;
        opacity: 0.95;
    }
    
    /* ============================================
       KPI SECTION
       ============================================ */
    .home-kpi-section {
        display: flex;
        justify-content: center;
        gap: 18px;
        margin: 30px auto;
        flex-wrap: wrap;
        max-width: 900px;
    }
    
    .home-kpi-card {
        flex: 1;
        min-width: 160px;
        max-width: 210px;
        padding: 25px 15px;
        border-radius: 16px;
        color: white;
        text-align: center;
        position: relative;
        transition: all 0.3s ease;
        box-shadow: 
            0 4px 6px rgba(0, 0, 0, 0.05),
            0 10px 20px rgba(0, 0, 0, 0.1);
    }
    
    .home-kpi-card:hover {
        transform: translateY(-5px);
    }
    
    .home-kpi-card.purple {
        background: linear-gradient(135deg, #667eea, #764ba2);
        box-shadow: 
            0 4px 6px rgba(0, 0, 0, 0.05),
            0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    .home-kpi-card.purple:hover {
        box-shadow: 
            0 8px 15px rgba(0, 0, 0, 0.1),
            0 20px 40px rgba(102, 126, 234, 0.4);
    }
    
    .home-kpi-card.green {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        box-shadow: 
            0 4px 6px rgba(0, 0, 0, 0.05),
            0 10px 20px rgba(17, 153, 142, 0.3);
    }
    
    .home-kpi-card.green:hover {
        box-shadow: 
            0 8px 15px rgba(0, 0, 0, 0.1),
            0 20px 40px rgba(17, 153, 142, 0.4);
    }
    
    .home-kpi-card.orange {
        background: linear-gradient(135deg, #f97316, #fbbf24);
        box-shadow: 
            0 4px 6px rgba(0, 0, 0, 0.05),
            0 10px 20px rgba(249, 115, 22, 0.3);
    }
    
    .home-kpi-card.orange:hover {
        box-shadow: 
            0 8px 15px rgba(0, 0, 0, 0.1),
            0 20px 40px rgba(249, 115, 22, 0.4);
    }
    
    .home-kpi-card.pink {
        background: linear-gradient(135deg, #ec008c, #fc6767);
        box-shadow: 
            0 4px 6px rgba(0, 0, 0, 0.05),
            0 10px 20px rgba(236, 0, 140, 0.3);
    }
    
    .home-kpi-card.pink:hover {
        box-shadow: 
            0 8px 15px rgba(0, 0, 0, 0.1),
            0 20px 40px rgba(236, 0, 140, 0.4);
    }
    
    .home-kpi-number {
        font-size: 48px;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 8px;
        text-shadow: 1px 2px 4px rgba(0, 0, 0, 0.15);
    }
    
    .home-kpi-label {
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 4px;
    }
    
    .home-kpi-sub {
        font-size: 12px;
        opacity: 0.85;
    }
    
    /* ============================================
       TOP BU SECTION
       ============================================ */
    .home-topbu-section {
        margin: 40px auto;
    }
    
    .home-topbu-card {
        background: linear-gradient(135deg, #FF6B35, #FFA07A, #FF8C00);
        padding: 35px 50px;
        border-radius: 24px;
        color: white;
        text-align: center;
        max-width: 500px;
        margin: 0 auto;
        border: 2px solid rgba(255, 255, 255, 0.4);
        box-shadow: 
            0 4px 6px rgba(0, 0, 0, 0.05),
            0 15px 30px rgba(255, 107, 53, 0.3),
            0 30px 60px rgba(255, 107, 53, 0.2);
        animation: home-glow 3s ease-in-out infinite;
    }
    
    @keyframes home-glow {
        0%, 100% { 
            box-shadow: 
                0 4px 6px rgba(0, 0, 0, 0.05),
                0 15px 30px rgba(255, 107, 53, 0.3),
                0 30px 60px rgba(255, 107, 53, 0.2);
        }
        50% { 
            box-shadow: 
                0 4px 6px rgba(0, 0, 0, 0.05),
                0 20px 40px rgba(255, 107, 53, 0.4),
                0 40px 80px rgba(255, 107, 53, 0.3);
        }
    }
    
    .home-topbu-label {
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        opacity: 0.9;
        margin-bottom: 15px;
    }
    
    .home-topbu-name {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 10px;
        text-shadow: 2px 3px 6px rgba(0, 0, 0, 0.2);
    }
    
    .home-topbu-number {
        font-size: 56px;
        font-weight: 800;
        line-height: 1;
        text-shadow: 2px 3px 6px rgba(0, 0, 0, 0.2);
    }
    
    .home-topbu-text {
        font-size: 18px;
        font-weight: 500;
        margin-top: 5px;
        opacity: 0.95;
    }
    
    /* ============================================
       MOTIVATION BANNER (Glassmorphism)
       ============================================ */
    .home-motivation-banner {
        background: linear-gradient(135deg, rgba(30, 58, 95, 0.9), rgba(59, 130, 246, 0.9), rgba(99, 102, 241, 0.9));
        -webkit-backdrop-filter: blur(10px);
        backdrop-filter: blur(10px);
        padding: 22px 30px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin: 35px auto;
        max-width: 700px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 
            0 4px 6px rgba(0, 0, 0, 0.05),
            0 10px 20px rgba(59, 130, 246, 0.2);
    }
    
    @supports not (backdrop-filter: blur(10px)) {
        .home-motivation-banner {
            background: linear-gradient(135deg, #1e3a5f, #3b82f6, #6366f1);
        }
    }
    
    .home-motivation-banner p {
        font-size: 18px;
        margin: 0;
        font-weight: 500;
        line-height: 1.5;
    }
    
    /* ============================================
       WHY SHARE CARD (Glassmorphism)
       ============================================ */
    .home-whyshare-card {
        background: rgba(255, 255, 255, 0.85);
        -webkit-backdrop-filter: blur(10px);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        margin: 30px auto;
        max-width: 900px;
        box-shadow: 
            0 4px 6px rgba(0, 0, 0, 0.05),
            0 10px 30px rgba(0, 0, 0, 0.08);
    }
    
    @supports not (backdrop-filter: blur(10px)) {
        .home-whyshare-card {
            background: rgba(255, 255, 255, 0.98);
        }
    }
    
    .home-whyshare-title {
        font-size: 26px;
        font-weight: 700;
        color: #2d3436;
        margin-bottom: 25px;
        text-align: center;
    }
    
    .home-whyshare-cards {
        display: flex;
        justify-content: center;
        gap: 18px;
        flex-wrap: wrap;
    }
    
    .home-why-card {
        flex: 1;
        min-width: 180px;
        max-width: 250px;
        padding: 28px 18px;
        border-radius: 16px;
        color: white;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .home-why-card:hover {
        transform: translateY(-8px);
    }
    
    .home-why-card.blue {
        background: linear-gradient(135deg, #3b82f6, #60a5fa);
        box-shadow: 
            0 4px 6px rgba(0, 0, 0, 0.05),
            0 10px 20px rgba(59, 130, 246, 0.3);
    }
    
    .home-why-card.blue:hover {
        box-shadow: 
            0 8px 15px rgba(0, 0, 0, 0.1),
            0 20px 40px rgba(59, 130, 246, 0.4);
    }
    
    .home-why-card.red {
        background: linear-gradient(135deg, #ef4444, #f87171);
        box-shadow: 
            0 4px 6px rgba(0, 0, 0, 0.05),
            0 10px 20px rgba(239, 68, 68, 0.3);
    }
    
    .home-why-card.red:hover {
        box-shadow: 
            0 8px 15px rgba(0, 0, 0, 0.1),
            0 20px 40px rgba(239, 68, 68, 0.4);
    }
    
    .home-why-card.green {
        background: linear-gradient(135deg, #22c55e, #4ade80);
        box-shadow: 
            0 4px 6px rgba(0, 0, 0, 0.05),
            0 10px 20px rgba(34, 197, 94, 0.3);
    }
    
    .home-why-card.green:hover {
        box-shadow: 
            0 8px 15px rgba(0, 0, 0, 0.1),
            0 20px 40px rgba(34, 197, 94, 0.4);
    }
    
    .home-why-icon {
        font-size: 45px;
        margin-bottom: 12px;
        animation: home-bounce 2s ease-in-out infinite;
    }
    
    @keyframes home-bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    .home-why-card:nth-child(2) .home-why-icon { animation-delay: 0.2s; }
    .home-why-card:nth-child(3) .home-why-icon { animation-delay: 0.4s; }
    
    .home-why-card-title {
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 6px;
    }
    
    .home-why-card-desc {
        font-size: 13px;
        opacity: 0.9;
        line-height: 1.5;
    }
    
    /* ============================================
       BENEFITS CARD (Glassmorphism)
       ============================================ */
    .home-benefits-card {
        background: rgba(255, 255, 255, 0.85);
        -webkit-backdrop-filter: blur(10px);
        backdrop-filter: blur(10px);
        padding: 28px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        margin: 30px auto;
        max-width: 550px;
        box-shadow: 
            0 4px 6px rgba(0, 0, 0, 0.05),
            0 10px 30px rgba(0, 0, 0, 0.08);
    }
    
    @supports not (backdrop-filter: blur(10px)) {
        .home-benefits-card {
            background: rgba(255, 255, 255, 0.98);
        }
    }
    
    .home-benefits-title {
        font-size: 22px;
        font-weight: 700;
        color: #2d3436;
        margin-bottom: 18px;
        text-align: center;
    }
    
    .home-benefit-item {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 12px 0;
        border-bottom: 1px solid rgba(241, 245, 249, 0.8);
    }
    
    .home-benefit-item:last-child {
        border-bottom: none;
    }
    
    .home-benefit-check {
        color: #10b981;
        font-size: 22px;
        font-weight: 800;
    }
    
    .home-benefit-text {
        font-size: 15px;
        color: #475569;
    }
    
    /* ============================================
       DIVIDER
       ============================================ */
    .home-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(226, 232, 240, 0.6), transparent);
        margin: 30px auto;
        max-width: 800px;
    }
    
    /* ============================================
       RESPONSIVE
       ============================================ */
    @media (max-width: 768px) {
        .home-header-title {
            font-size: 28px;
        }
        
        .home-kpi-section {
            gap: 12px;
        }
        
        .home-kpi-card {
            min-width: 140px;
            padding: 18px 10px;
        }
        
        .home-kpi-number {
            font-size: 38px;
        }
        
        .home-topbu-card {
            padding: 25px 30px;
        }
        
        .home-topbu-name {
            font-size: 32px;
        }
        
        .home-topbu-number {
            font-size: 44px;
        }
        
        .home-why-card {
            min-width: 100%;
        }
        
        /* Reduce blur on mobile for performance */
        .home-glass,
        .home-whyshare-card,
        .home-benefits-card {
            -webkit-backdrop-filter: blur(5px);
            backdrop-filter: blur(5px);
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
    st.markdown('<div class="home-page">', unsafe_allow_html=True)

    # Header Section
    st.markdown(
        '<div class="home-tag">✨ TEOA Initiative</div>', unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <h1 class="home-header-title">Welcome to TEOA Procurement Idea Hub</h1>
        <p class="home-header-subtitle">
            Hello <span class="home-header-name">{st.session_state.full_name or st.session_state.username}</span> 👋
        </p>
        """,
        unsafe_allow_html=True,
    )

    # CTA Card
    st.markdown(
        """
        <div class="home-cta-card">
            <div class="home-cta-title">💬 Have an idea?</div>
            <div class="home-cta-text">This is the place to share it. Great ideas can come from anywhere — and so can you!</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # KPI Section - 4 Stats
    st.markdown('<div class="home-kpi-section">', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="home-kpi-card purple">
            <div class="home-kpi-number">{stats["total"]}</div>
            <div class="home-kpi-label">📊 Total Ideas</div>
            <div class="home-kpi-sub">All time</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="home-kpi-card green">
            <div class="home-kpi-number">{stats["this_month"]}</div>
            <div class="home-kpi-label">📅 This Month</div>
            <div class="home-kpi-sub">Keep it up!</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="home-kpi-card orange">
            <div class="home-kpi-number">{stats["this_year"]}</div>
            <div class="home-kpi-label">📆 This Year</div>
            <div class="home-kpi-sub">Happy year!</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="home-kpi-card pink">
            <div class="home-kpi-number">{user_idea_count}</div>
            <div class="home-kpi-label">🏆 Your Ideas</div>
            <div class="home-kpi-sub">Great job!</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Top BU Section
    if top_bu:
        st.markdown('<div class="home-topbu-section">', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="home-topbu-card">
                <div class="home-topbu-label">🏆 TOP BU THIS MONTH</div>
                <div class="home-topbu-name">🥇 {top_bu["bu_cl_site"]}</div>
                <div class="home-topbu-number">{top_bu["count"]}</div>
                <div class="home-topbu-text">ideas submitted</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="home-divider"></div>', unsafe_allow_html=True)

    # Motivation Banner
    st.markdown(
        """
        <div class="home-motivation-banner">
            <p>⭐ Your ideas are reviewed weekly — your thoughts matter and are valued!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="home-divider"></div>', unsafe_allow_html=True)

    # Why Share Card
    st.markdown(
        """
        <div class="home-whyshare-card">
            <div class="home-whyshare-title">Why Share Your Ideas?</div>
            <div class="home-whyshare-cards">
                <div class="home-why-card blue">
                    <div class="home-why-icon">💡</div>
                    <div class="home-why-card-title">Share Your Ideas</div>
                    <div class="home-why-card-desc">Every idea matters and can make a real difference.</div>
                </div>
                <div class="home-why-card red">
                    <div class="home-why-icon">🚀</div>
                    <div class="home-why-card-title">Drive Excellence</div>
                    <div class="home-why-card-desc">Help enhance operations through your perspective.</div>
                </div>
                <div class="home-why-card green">
                    <div class="home-why-icon">🎯</div>
                    <div class="home-why-card-title">Make Impact</div>
                    <div class="home-why-card-desc">See your ideas come to life and create change.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Benefits Card
    st.markdown(
        """
        <div class="home-benefits-card">
            <div class="home-benefits-title">✨ Benefits</div>
            <div class="home-benefit-item">
                <span class="home-benefit-check">✓</span>
                <span class="home-benefit-text">Quick and easy submission process</span>
            </div>
            <div class="home-benefit-item">
                <span class="home-benefit-check">✓</span>
                <span class="home-benefit-text">Track your idea's progress</span>
            </div>
            <div class="home-benefit-item">
                <span class="home-benefit-check">✓</span>
                <span class="home-benefit-text">Collaborate and engage with teams</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Close Container
    st.markdown("</div>", unsafe_allow_html=True)
