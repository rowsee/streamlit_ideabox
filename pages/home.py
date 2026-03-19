import streamlit as st
from database import get_stats, get_user_ideas, get_top_contributors_per_bu

st.markdown(
    """
<style>
    /* Main container */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Tag badge */
    .tag {
        background: #FFD700;
        color: #2d3436;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 15px;
    }
    
    /* Top BU Card - Centered & Highlighted */
    .top-bu-container {
        display: flex;
        justify-content: center;
        margin: 25px 0;
    }
    .top-bu-card {
        background: linear-gradient(135deg, #FF6B35, #FF8F5E);
        padding: 25px 50px;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(255, 107, 53, 0.4);
        position: relative;
        overflow: hidden;
    }
    .top-bu-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 3s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    .top-bu-label {
        font-size: 14px;
        opacity: 0.95;
        font-weight: 600;
        margin-bottom: 10px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .top-bu-name {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .top-bu-count {
        font-size: 18px;
        opacity: 0.95;
        font-weight: 500;
    }
    
    /* KPI Cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin: 20px 0;
    }
    .kpi-card {
        padding: 30px 20px;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    .kpi-card.purple { background: linear-gradient(135deg, #667eea, #764ba2); }
    .kpi-card.green { background: linear-gradient(135deg, #00b894, #00a085); }
    .kpi-card.pink { background: linear-gradient(135deg, #fd79a8, #e84393); }
    
    .kpi-number {
        font-size: 56px;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.15);
    }
    .kpi-label {
        font-size: 16px;
        font-weight: 600;
        opacity: 0.95;
        margin-bottom: 5px;
    }
    .kpi-sub {
        font-size: 13px;
        opacity: 0.8;
    }
    
    /* Info Banner */
    .info-banner {
        background: linear-gradient(135deg, #1E3A5F, #2D5A87);
        padding: 18px 30px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 25px 0;
        box-shadow: 0 4px 15px rgba(30, 58, 95, 0.3);
    }
    .info-banner p {
        font-size: 17px;
        margin: 0;
        font-weight: 500;
    }
    
    /* Why Share Cards */
    .why-share-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin: 25px 0;
    }
    .why-card {
        padding: 35px 25px;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .why-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.2);
    }
    .why-card.blue { background: linear-gradient(135deg, #4F46E5, #7C3AED); }
    .why-card.red { background: linear-gradient(135deg, #DC2626, #B91C1C); }
    .why-card.green { background: linear-gradient(135deg, #059669, #047857); }
    
    .why-icon {
        font-size: 48px;
        margin-bottom: 15px;
    }
    .why-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .why-desc {
        font-size: 14px;
        opacity: 0.9;
        line-height: 1.5;
    }
    
    /* Bottom Section */
    .bottom-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 25px;
        margin: 25px 0;
    }
    .benefits-card {
        background: #ffffff;
        padding: 25px 30px;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #e8e8e8;
    }
    .benefits-title {
        font-size: 20px;
        font-weight: 700;
        color: #2d3436;
        margin-bottom: 20px;
    }
    .benefit-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0;
        border-bottom: 1px solid #f0f0f0;
    }
    .benefit-item:last-child {
        border-bottom: none;
    }
    .benefit-check {
        color: #00b894;
        font-size: 20px;
        font-weight: 700;
    }
    .benefit-text {
        font-size: 15px;
        color: #636e72;
    }
    
    .encouragement-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 30px;
        border-radius: 16px;
        color: white;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .encouragement-icon {
        font-size: 40px;
        margin-bottom: 15px;
    }
    .encouragement-title {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .encouragement-text {
        font-size: 15px;
        line-height: 1.6;
        opacity: 0.95;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .kpi-grid, .why-share-grid, .bottom-grid {
            grid-template-columns: 1fr;
        }
        .top-bu-name {
            font-size: 32px;
        }
        .kpi-number {
            font-size: 42px;
        }
    }
    
    /* Hide scrollbar */
    .stApp > div > div > div > div {
        overflow: visible !important;
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

    # Header
    st.markdown('<div class="tag">✨ TEOA Initiative</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <h1 style="font-size: 36px; font-weight: 700; margin-bottom: 8px; line-height: 1.2; color: #2d3436;">
            Welcome to TEOA Procurement Idea Hub,<br>
            <span style="color: #667eea;">{st.session_state.full_name or st.session_state.username} 👋</span>
        </h1>
        """,
        unsafe_allow_html=True,
    )

    # Top BU Section - Centered & Highlighted
    if top_bu:
        st.markdown('<div class="top-bu-container">', unsafe_allow_html=True)
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

    # KPI Cards
    st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)

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

    # Info Banner
    st.markdown(
        """
        <div class="info-banner">
            <p>⭐ Your ideas are reviewed weekly — your thoughts matter and are valued!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Why Share Your Ideas - Colorful Cards
    st.markdown('<div class="why-share-grid">', unsafe_allow_html=True)

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
        <div class="why-card red">
            <div class="why-icon">🚀</div>
            <div class="why-title">Drive Excellence</div>
            <div class="why-desc">Help enhance operational excellence through your unique perspective.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="why-card green">
            <div class="why-icon">🎯</div>
            <div class="why-title">Make Impact</div>
            <div class="why-desc">See your ideas come to life and create meaningful change for everyone.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Bottom Section - Benefits & Encouragement
    st.markdown('<div class="bottom-grid">', unsafe_allow_html=True)

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
