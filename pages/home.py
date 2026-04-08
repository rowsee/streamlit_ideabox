import streamlit as st
from database import (
    get_stats,
    get_user_ideas,
    get_top_contributors_per_bu,
    get_top_contributor,
    get_recent_ideas,
    get_trending_ideas,
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

    /* STAT CARDS */
    .stat-card {
        background: white !important;
        border-radius: 12px !important;
        padding: 28px 24px !important;
        text-align: center;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        transition: all 0.2s ease;
        cursor: default;
    }

    .stat-card:hover {
        border-color: #6366f1 !important;
        box-shadow: 0 4px 12px rgba(99,102,241,0.15) !important;
        transform: translateY(-2px);
    }

    .stat-value { 
        font-size: 48px !important; 
        font-weight: 900 !important; 
        color: #1e293b;
        line-height: 1;
        margin: 0;
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

    /* IDEA CARDS - Responsive 2-line format */
    .idea-cards-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 16px;
        margin-top: 16px;
    }

    .idea-card {
        background: white !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        padding: 16px 20px !important;
        transition: all 0.2s ease;
    }

    .idea-card:hover {
        border-color: #6366f1 !important;
        box-shadow: 0 4px 12px rgba(99,102,241,0.15) !important;
        transform: translateY(-2px);
    }

    /* LINE 1: Title | Submitter */
    .idea-card-line1 {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }

    .idea-card-title {
        font-weight: 600;
        color: #1e293b;
        font-size: 15px;
        flex: 1;
        padding-right: 12px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .idea-card-submitter {
        font-size: 12px;
        color: #64748b;
        white-space: nowrap;
    }

    /* LINE 2: Likes | Date */
    .idea-card-line2 {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .idea-card-likes {
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

    .idea-card-date {
        font-size: 12px;
        color: #94a3b8;
    }

    /* IDEAL LIST STYLES (replacing cards) */
    .idea-list {
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        overflow: hidden;
    }

    .idea-list-item {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        padding: 16px 20px;
        border-bottom: 1px solid #e2e8f0;
        background: white;
        transition: background 0.2s ease;
    }

    .idea-list-item:hover {
        background: #f8fafc;
    }

    .idea-list-item:last-child {
        border-bottom: none;
    }

    .idea-list-main {
        flex: 1;
        min-width: 0;
    }

    .idea-list-title {
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 6px;
        font-size: 15px;
        line-height: 1.4;
    }

    .idea-list-meta {
        font-size: 13px;
        color: #64748b;
        display: flex;
        gap: 12px;
        align-items: center;
    }

    .idea-list-stats {
        display: flex;
        gap: 16px;
        align-items: center;
        flex-shrink: 0;
    }

    .idea-list-votes {
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

    .idea-list-date {
        font-size: 12px;
        color: #94a3b8;
        white-space: nowrap;
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

    /* HIGHLIGHT CARDS - Top BU & Contributor */
    .highlight-card {
        background: white;
        border-radius: 16px;
        padding: 32px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1) !important;
        border: 1px solid #e2e8f0 !important;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .highlight-card.orange {
        background: linear-gradient(135deg, #f97316, #fb923c) !important;
        border: none !important;
    }

    .highlight-card.purple {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        border: none !important;
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

    .highlight-name {
        font-size: 32px !important;
        font-weight: 700 !important;
        margin-bottom: 12px;
        color: white;
        line-height: 1.2;
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


def render_idea_cards(ideas, show_date=False):
    """Render responsive cards for ideas - 2-line format"""
    if not ideas:
        return

    html_parts = ['<div class="idea-cards-container">']

    for idea in ideas[:5]:
        votes = idea.get("votes", 0)
        title = idea.get("title", "Untitled")
        if len(title) > 50:
            title = title[:47] + "..."
        submitter = idea.get("submitter_name") or idea.get("username", "Anonymous")

        date_str = ""
        if show_date and idea.get("submitted_at"):
            from datetime import datetime

            try:
                date_obj = datetime.strptime(str(idea["submitted_at"])[:10], "%Y-%m-%d")
                date_str = date_obj.strftime("%b %d, %Y")
            except:
                pass

        # LINE 1: Title | Submitter
        # LINE 2: Likes | Date
        html_parts.append('<div class="idea-card">')
        html_parts.append('  <div class="idea-card-line1">')
        html_parts.append(f'    <span class="idea-card-title">{title}</span>')
        html_parts.append(
            f'    <span class="idea-card-submitter">by {submitter}</span>'
        )
        html_parts.append("  </div>")
        html_parts.append('  <div class="idea-card-line2">')
        html_parts.append(f'    <span class="idea-card-likes">👍 {votes}</span>')
        if date_str:
            html_parts.append(f'    <span class="idea-card-date">📅 {date_str}</span>')
        html_parts.append("  </div>")
        html_parts.append("</div>")

    html_parts.append("</div>")

    full_html = "\n".join(html_parts)
    st.markdown(full_html, unsafe_allow_html=True)


def render():
    stats = get_stats() or {}
    top_bu = get_top_contributors_per_bu() or {}
    top_contributor = get_top_contributor() or {}
    user_ideas = get_user_ideas(st.session_state.user_id) or []
    user_idea_count = len(user_ideas)

    # Get new data
    recent_ideas = get_recent_ideas(5) or []
    trending_ideas = get_trending_ideas(5) or []

    # HIGHLIGHTS ROW - Top BU and Top Contributor (MOVED TO TOP)
    highlights_cols = st.columns(2, gap="medium")

    with highlights_cols[0]:
        if top_bu:
            st.markdown(
                f"""
            <div class="highlight-card orange">
                <div class="highlight-label">TOP BU THIS MONTH</div>
                <h2 class="highlight-name">{top_bu.get("bu_cl_site", "N/A")}</h2>
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
                <div class="highlight-label">TOP BU THIS MONTH</div>
                <div class="highlight-name">Be the First!</div>
                <div class="highlight-count">—</div>
                <div class="highlight-text">Submit ideas from your BU to see it here!</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with highlights_cols[1]:
        if top_contributor:
            st.markdown(
                f"""
            <div class="highlight-card purple">
                <div class="highlight-label">TOP CONTRIBUTOR</div>
                <h2 class="highlight-name">{top_contributor.get("name", "N/A")}</h2>
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
                <div class="highlight-label">TOP CONTRIBUTOR</div>
                <div class="highlight-name">Start Your Journey!</div>
                <div class="highlight-count">—</div>
                <div class="highlight-text">Submit your first idea to become a top contributor!</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    st.divider()

    # STATS ROW - KPI Cards
    st.markdown(
        """
    <div class="section-header">
        <h2 class="section-title">Overview</h2>
    </div>
    """,
        unsafe_allow_html=True,
    )

    stat_cols = st.columns(4)

    with stat_cols[0]:
        st.markdown(
            f"""
        <div class="stat-card">
            <h2 class="stat-value">{stats.get("total", 0)}</h2>
            <div class="stat-label">Total Ideas</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with stat_cols[1]:
        st.markdown(
            f"""
        <div class="stat-card">
            <h2 class="stat-value">{stats.get("this_month", 0)}</h2>
            <div class="stat-label">This Month</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with stat_cols[2]:
        st.markdown(
            f"""
        <div class="stat-card">
            <h2 class="stat-value">{stats.get("this_year", 0)}</h2>
            <div class="stat-label">This Year</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with stat_cols[3]:
        st.markdown(
            f"""
        <div class="stat-card">
            <h2 class="stat-value">{user_idea_count}</h2>
            <div class="stat-label">Your Ideas</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.divider()

    # TRENDING IDEAS & RECENTLY SUBMITTED - Side by Side
    idea_cols = st.columns(2, gap="medium")

    with idea_cols[0]:
        st.markdown(
            """
        <div class="section-header" style="margin-top: 0 !important;">
            <h2 class="section-title">Trending Ideas</h2>
        </div>
        """,
            unsafe_allow_html=True,
        )
        if trending_ideas:
            render_idea_cards(trending_ideas, show_date=False)
        else:
            render_empty_state(
                "🔥",
                "No trending ideas yet",
                "Be the first to submit an idea and start the conversation!",
                "Submit Your First Idea",
            )

    with idea_cols[1]:
        st.markdown(
            """
        <div class="section-header" style="margin-top: 0 !important;">
            <h2 class="section-title">Recently Submitted</h2>
        </div>
        """,
            unsafe_allow_html=True,
        )
        if recent_ideas:
            render_idea_cards(recent_ideas, show_date=True)
        else:
            render_empty_state(
                "🆕",
                "No recent submissions",
                "Fresh ideas fuel innovation. Share yours today!",
                "Submit an Idea",
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
