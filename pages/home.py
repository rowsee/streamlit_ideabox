import streamlit as st
from database import (
    get_stats,
    get_user_ideas,
    get_top_contributors_per_bu,
    get_top_contributor,
    get_recent_ideas,
    get_trending_ideas,
    get_top_contributors_all,
)

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

    .stApp { background-color: var(--bg-light); }

    /* Remove focus/selection highlighting from all elements */
    * {
        -webkit-tap-highlight-color: transparent;
    }

    *:focus {
        outline: none !important;
    }

    h1, h2, h3, h4, h5, h6 {
        outline: none !important;
        user-select: none;
        -webkit-user-select: none;
    }

    h2::selection, h2::-moz-selection,
    .section-title::selection, .section-title::-moz-selection {
        background: transparent;
        color: inherit;
    }

    /* HERO SECTION - Enhanced */
    .hero-section {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-radius: 16px;
        padding: 48px 40px;
        text-align: center;
        margin-bottom: 40px;
        color: white;
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.25);
    }

    .hero-icon { 
        font-size: 64px; 
        margin-bottom: 20px; 
    }

    .hero-title { 
        font-size: 32px; 
        font-weight: 700; 
        margin-bottom: 16px; 
        color: white !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .hero-subtitle { 
        font-size: 18px; 
        opacity: 0.95; 
        margin-bottom: 28px;
        color: rgba(255,255,255,0.95) !important;
        font-weight: 400;
    }

    .hero-cta {
        background: white;
        color: #6366f1;
        padding: 14px 28px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 16px;
        border: none;
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-block;
        text-decoration: none;
    }

    .hero-cta:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    /* STAT CARDS - Enhanced */
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 28px 24px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
        cursor: default;
    }

    .stat-card:hover {
        border-color: #6366f1;
        box-shadow: 0 4px 12px rgba(99,102,241,0.15);
        transform: translateY(-2px);
    }

    .stat-icon { 
        font-size: 32px; 
        margin-bottom: 12px; 
    }

    .stat-value { 
        font-size: 40px; 
        font-weight: 800; 
        color: #1e293b;
        line-height: 1;
    }

    .stat-label { 
        font-size: 14px; 
        color: #64748b; 
        margin-top: 8px;
        font-weight: 500;
    }

    /* SECTION HEADERS - Enhanced with blue highlight fix */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 24px;
        margin-top: 40px;
        padding-bottom: 12px;
        border-bottom: 1px solid #e2e8f0;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #1e293b;
        margin: 0;
        user-select: none;
        -webkit-user-select: none;
        outline: none !important;
        background: transparent !important;
    }

    .section-title:focus,
    .section-title:active {
        outline: none !important;
        background: transparent !important;
    }

    .section-icon {
        font-size: 24px;
    }

    /* IDEA CARDS */
    .idea-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
        height: 100%;
    }

    .idea-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.08);
        border-color: #6366f1;
    }

    /* Ensure cards don't look clickable unless they are */
    .idea-card {
        cursor: default;
    }

    .idea-card-title {
        font-size: 16px;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 8px;
        line-height: 1.4;
    }

    .idea-card-meta {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        color: #64748b;
        margin-bottom: 12px;
    }

    .idea-card-votes {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: #f1f5f9;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        color: #6366f1;
    }

    /* EMPTY STATES */
    .empty-state {
        text-align: center;
        padding: 48px 24px;
        background: white;
        border-radius: 12px;
        border: 2px dashed #e2e8f0;
    }

    .empty-state-icon { 
        font-size: 48px; 
        margin-bottom: 16px; 
    }

    .empty-state-title { 
        font-size: 18px; 
        font-weight: 600; 
        color: #1e293b; 
        margin-bottom: 8px; 
    }

    .empty-state-message { 
        font-size: 14px; 
        color: #64748b; 
        margin-bottom: 20px; 
    }

    /* HIGHLIGHT CARDS */
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
        color: white;
    }

    .highlight-icon {
        font-size: 36px;
        margin-bottom: 14px;
    }

    .highlight-name {
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 12px;
        color: white;
    }

    .highlight-count {
        font-size: 64px;
        font-weight: 800;
        line-height: 1;
        color: white;
        text-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    .highlight-text {
        font-size: 15px;
        opacity: 0.9;
        margin-top: 10px;
        font-weight: 600;
        color: white;
    }

    /* INFO CARDS */
    .card {
        background: white;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
        height: auto;
        min-height: 200px;
        overflow: hidden;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }

    .card-title {
        font-size: 17px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 16px;
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
        align-items: flex-start;
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
        flex-shrink: 0;
    }

    .benefits-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 12px;
        margin-top: 8px;
    }

    .benefit-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 12px 16px;
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
        flex-shrink: 0;
    }

    /* CTA CARD */
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

    /* TOP CONTRIBUTORS */
    .contributor-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 16px;
        background: #f8fafc;
        border-radius: 10px;
        margin-bottom: 8px;
        transition: all 0.2s ease;
    }

    .contributor-item:hover {
        background: #f1f5f9;
    }

    .contributor-rank {
        font-size: 18px;
        font-weight: 700;
        color: #6366f1;
        width: 28px;
        text-align: center;
    }

    .contributor-name {
        flex: 1;
        font-size: 14px;
        font-weight: 500;
        color: #1e293b;
    }

    .contributor-count {
        font-size: 14px;
        font-weight: 600;
        color: #6366f1;
        background: white;
        padding: 4px 10px;
        border-radius: 20px;
    }

    .stDivider { 
        margin: 40px 0; 
        border-color: #e2e8f0;
    }

    /* Additional spacing and polish */
    .main > div {
        padding-top: 8px;
    }

    /* Remove default Streamlit focus styles on headings */
    h1:focus, h2:focus, h3:focus {
        outline: none !important;
        box-shadow: none !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


def render_empty_state(icon, title, message, cta_text=None):
    """Render an engaging empty state"""
    html = f"""
    <div class="empty-state">
        <div class="empty-state-icon">{icon}</div>
        <div class="empty-state-title">{title}</div>
        <div class="empty-state-message">{message}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

    if cta_text:
        if st.button(
            cta_text, key=f"empty_cta_{icon}", type="primary", use_container_width=True
        ):
            st.session_state.current_page = "submit_idea"
            st.rerun()


def render_idea_card(idea, compact=False):
    """Render a compact idea card"""
    votes = idea.get("votes", 0)
    title = (
        idea.get("title", "Untitled")[:60] + "..."
        if len(idea.get("title", "")) > 60
        else idea.get("title", "Untitled")
    )
    submitter = idea.get("submitter_name") or idea.get("username", "Anonymous")

    html = f"""
    <div class="idea-card">
        <div class="idea-card-title">{title}</div>
        <div class="idea-card-meta">
            <span>by {submitter}</span>
        </div>
        <div class="idea-card-votes">
            👍 {votes} likes
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render():
    stats = get_stats() or {}
    top_bu = get_top_contributors_per_bu() or {}
    top_contributor = get_top_contributor() or {}
    user_ideas = get_user_ideas(st.session_state.user_id) or []
    user_idea_count = len(user_ideas)

    # Get new data
    recent_ideas = get_recent_ideas(3) or []
    trending_ideas = get_trending_ideas(3) or []
    top_contributors = get_top_contributors_all(5) or []

    user_name = st.session_state.get("full_name") or st.session_state.get(
        "username", "User"
    )

    # HERO SECTION
    if user_idea_count == 0:
        # Show hero CTA for new users
        st.markdown(
            f"""
        <div class="hero-section">
            <div class="hero-icon">🚀</div>
            <div class="hero-title">Welcome to TEOA Idea Hub!</div>
            <div class="hero-subtitle">Turn your improvement ideas into impact. Share your suggestions and help drive operational excellence.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Submit Your First Idea ✨",
            key="hero_cta",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.current_page = "submit_idea"
            st.rerun()
    else:
        # Welcome back message for returning users
        st.markdown(
            f"""
        <div class="hero-section">
            <div class="hero-icon">👋</div>
            <div class="hero-title">Welcome back, {user_name}!</div>
            <div class="hero-subtitle">You've submitted {user_idea_count} idea{"s" if user_idea_count != 1 else ""}. Keep the momentum going!</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # STATS ROW
    stat_cols = st.columns(4)

    with stat_cols[0]:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">💡</div>
            <div class="stat-value">{stats.get("total", 0)}</div>
            <div class="stat-label">Total Ideas</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with stat_cols[1]:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">📅</div>
            <div class="stat-value">{stats.get("this_month", 0)}</div>
            <div class="stat-label">This Month</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with stat_cols[2]:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">🔥</div>
            <div class="stat-value">{stats.get("this_year", 0)}</div>
            <div class="stat-label">This Year</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with stat_cols[3]:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">✏️</div>
            <div class="stat-value">{user_idea_count}</div>
            <div class="stat-label">Your Ideas</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.divider()

    # TRENDING IDEAS SECTION
    st.markdown(
        """
    <div class="section-header">
        <span class="section-icon">🔥</span>
        <h2 class="section-title">Trending Ideas</h2>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if trending_ideas:
        trend_cols = st.columns(3)
        for idx, idea in enumerate(trending_ideas):
            with trend_cols[idx]:
                render_idea_card(idea)
    else:
        render_empty_state(
            "🔥",
            "No trending ideas yet",
            "Be the first to submit an idea and start the conversation!",
            "Submit Your First Idea",
        )

    # RECENTLY SUBMITTED SECTION
    st.markdown(
        """
    <div class="section-header">
        <span class="section-icon">🆕</span>
        <h2 class="section-title">Recently Submitted</h2>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if recent_ideas:
        recent_cols = st.columns(3)
        for idx, idea in enumerate(recent_ideas):
            with recent_cols[idx]:
                render_idea_card(idea)
    else:
        render_empty_state(
            "🆕",
            "No recent submissions",
            "Fresh ideas fuel innovation. Share yours today!",
            "Submit an Idea",
        )

    st.divider()

    # HIGHLIGHTS + TOP CONTRIBUTORS ROW
    highlights_cols = st.columns([1, 1, 1], gap="medium")

    with highlights_cols[0]:
        if top_bu:
            st.markdown(
                f"""
            <div class="highlight-card orange">
                <div class="highlight-icon">🏆</div>
                <div class="highlight-label">TOP BU THIS MONTH</div>
                <div class="highlight-name">{top_bu.get("bu_cl_site", "N/A")}</div>
                <div class="highlight-count">{top_bu.get("count", 0)}</div>
                <div class="highlight-text">ideas submitted</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
            <div class="highlight-card orange">
                <div class="highlight-icon">🏆</div>
                <div class="highlight-label">TOP BU THIS MONTH</div>
                <div class="highlight-name">No data yet</div>
                <div class="highlight-count">—</div>
                <div class="highlight-text">Start submitting ideas!</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with highlights_cols[1]:
        if top_contributor:
            st.markdown(
                f"""
            <div class="highlight-card purple">
                <div class="highlight-icon">👤</div>
                <div class="highlight-label">TOP CONTRIBUTOR</div>
                <div class="highlight-name">{top_contributor.get("name", "N/A")}</div>
                <div class="highlight-count">{top_contributor.get("count", 0)}</div>
                <div class="highlight-text">ideas submitted</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
            <div class="highlight-card purple">
                <div class="highlight-icon">👤</div>
                <div class="highlight-label">TOP CONTRIBUTOR</div>
                <div class="highlight-name">No data yet</div>
                <div class="highlight-count">—</div>
                <div class="highlight-text">Be the first!</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with highlights_cols[2]:
        st.markdown(
            """
        <div class="section-header" style="margin-top: 0;">
            <span class="section-icon">🏆</span>
            <h2 class="section-title" style="font-size: 17px;">Top Contributors</h2>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if top_contributors:
            for idx, contributor in enumerate(top_contributors[:3]):
                name = contributor.get("full_name") or contributor.get(
                    "username", "Anonymous"
                )
                count = contributor.get("idea_count", 0)
                st.markdown(
                    f"""
                <div class="contributor-item">
                    <div class="contributor-rank">#{idx + 1}</div>
                    <div class="contributor-name">{name}</div>
                    <div class="contributor-count">{count} ideas</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            render_empty_state(
                "🏆",
                "No contributors yet",
                "Join the leaderboard by submitting your ideas!",
            )

    st.divider()

    # WHY SHARE + BENEFITS ROW
    bottom_cols = st.columns(2, gap="medium")

    with bottom_cols[0]:
        st.markdown(
            """
        <div class="card">
            <div class="card-title">💡 Why Share Ideas?</div>
            <ul class="why-list">
                <li><span class="why-icon">🚀</span> Drive operational excellence and process improvements</li>
                <li><span class="why-icon">🎯</span> Make a meaningful impact across the organization</li>
                <li><span class="why-icon">🤝</span> Collaborate with teams and share best practices</li>
                <li><span class="why-icon">💡</span> Every idea matters - no suggestion is too small</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with bottom_cols[1]:
        st.markdown(
            """
        <div class="card">
            <div class="card-title">✨ Benefits</div>
            <div class="benefits-grid">
                <div class="benefit-item"><span class="benefit-check">✓</span> Quick and easy submission process</div>
                <div class="benefit-item"><span class="benefit-check">✓</span> Track your idea's progress and status</div>
                <div class="benefit-item"><span class="benefit-check">✓</span> Collaborate with teams and get feedback</div>
                <div class="benefit-item"><span class="benefit-check">✓</span> Get recognized for your contributions</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # CTA CARD (FULL WIDTH AT BOTTOM)
    st.markdown(
        """
    <div class="cta-card">
        <div class="cta-title">💬 Have an idea?</div>
        <div class="cta-text">Submit your idea and help shape the future of our operations!</div>
        <div class="cta-sub">📅 Ideas reviewed weekly by the leadership team</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    render()
