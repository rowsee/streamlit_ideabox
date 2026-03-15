import streamlit as st
from database import get_stats, get_user_ideas

st.markdown("""
<style>
    .stat-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 20px 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.25);
    }
    .stat-card.green {
        background: linear-gradient(135deg, #00b894, #00a085);
        box-shadow: 0 4px 15px rgba(0, 184, 148, 0.25);
    }
    .stat-card.pink {
        background: linear-gradient(135deg, #fd79a8, #e84393);
        box-shadow: 0 4px 15px rgba(253, 121, 168, 0.25);
    }
    .stat-number {
        font-size: 40px;
        font-weight: 700;
        margin-bottom: 6px;
        line-height: 1;
    }
    .stat-label {
        font-size: 13px;
        opacity: 0.95;
        font-weight: 600;
    }
    .stat-sub {
        font-size: 11px;
        opacity: 0.8;
        margin-top: 3px;
    }
    .feature-card {
        background: #ffffff;
        padding: 20px 25px;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
        border: 1px solid #e8e8e8;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .feature-icon {
        font-size: 32px;
    }
    .feature-title {
        font-size: 18px;
        margin-bottom: 4px;
        color: #2d3436;
        font-weight: 600;
    }
    .feature-desc {
        font-size: 14px;
        line-height: 1.5;
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
        font-size: 16px;
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
</style>
""", unsafe_allow_html=True)

def render():
    stats = get_stats()
    user_ideas = get_user_ideas(st.session_state.user_id)
    user_idea_count = len(user_ideas) if user_ideas else 0
    
    st.markdown('<div class="tag">✨ TEOA Initiative</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <h1 style="font-size: 42px; font-weight: 700; margin-bottom: 12px; line-height: 1.2; color: #2d3436;">
        Welcome to TEOA Ideabox,<br>
        <span style="color: #667eea;">{st.session_state.full_name or st.session_state.username} 👋</span>
    </h1>
    """, unsafe_allow_html=True)
    
    st.markdown('<p style="font-size: 22px; margin-bottom: 35px; color: #636e72; font-weight: 300;">One idea. One improvement. One step better.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['total']}</div>
            <div class="stat-label">📊 Total Ideas</div>
            <div class="stat-sub">All time</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card green">
            <div class="stat-number">{stats['this_month']}</div>
            <div class="stat-label">📅 This Month</div>
            <div class="stat-sub">Keep it up!</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card pink">
            <div class="stat-number">{user_idea_count}</div>
            <div class="stat-label">🏆 Your Ideas</div>
            <div class="stat-sub">Great job!</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Why Share Your Ideas?")
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <div>
                <div class="feature-title">Share Your Ideas</div>
                <div class="feature-desc">From small everyday improvements to breakthrough innovations — every idea matters.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("###")
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <div>
                <div class="feature-title">Drive Excellence</div>
                <div class="feature-desc">Help us enhance operational excellence through your unique perspective.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("###")
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div>
                <div class="feature-title">Make Impact</div>
                <div class="feature-desc">See your ideas come to life and make a real difference in how we work.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="highlight-box">
            <p>💬 <strong>Have an idea?</strong> This is the place to share it. Great ideas can come from anywhere!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Benefits")
        
        st.markdown('<div class="check-item"><span>✓</span> Quick submission</div>', unsafe_allow_html=True)
        st.markdown("###")
        st.markdown('<div class="check-item"><span>✓</span> Track progress</div>', unsafe_allow_html=True)
        st.markdown("###")
        st.markdown('<div class="check-item"><span>✓</span> Collaborate with teams</div>', unsafe_allow_html=True)
