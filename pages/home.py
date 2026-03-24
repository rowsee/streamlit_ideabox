import streamlit as st
from database import get_stats, get_user_ideas, get_top_contributors_per_bu

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Idea Hub Dashboard", layout="wide")


# -------------------------
# SAFE HELPERS
# -------------------------
def safe_get_session():
    return {
        "user_id": st.session_state.get("user_id"),
        "full_name": st.session_state.get("full_name"),
        "username": st.session_state.get("username", "User"),
    }


def safe_stats():
    stats = get_stats() or {}
    return {
        "total": stats.get("total", 0),
        "this_month": stats.get("this_month", 0),
        "this_year": stats.get("this_year", 0),
    }


def safe_top_bu():
    top_bu = get_top_contributors_per_bu()
    if not top_bu:
        return None
    return {
        "name": top_bu.get("bu_cl_site", "N/A"),
        "count": top_bu.get("count", 0),
    }


# -------------------------
# PREMIUM STYLES
# -------------------------
st.markdown("""
<style>

/* GLOBAL FIX */
section.main > div {
    padding-top: 1rem;
}

/* REMOVE STREAMLIT PADDING */
.block-container {
    padding-top: 1rem !important;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* HEADER */
.header {
    padding: 30px;
    border-radius: 20px;
    background: linear-gradient(135deg, #0f172a, #4338ca);
    color: white;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}

/* KPI CARDS */
.kpi-card {
    padding: 25px;
    border-radius: 20px;
    background: linear-gradient(145deg, #ffffff, #f1f5f9);
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    text-align: center;
    transition: all 0.3s ease;
}

.kpi-card:hover {
    transform: translateY(-6px) scale(1.02);
}

/* TEXT */
.kpi-number {
    font-size: 42px;
    font-weight: 900;
    color: #111827;
}

.kpi-label {
    font-size: 16px;
    color: #6b7280;
}

/* FEATURE */
.feature-card {
    padding: 30px;
    border-radius: 20px;
    background: white;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

/* TOP BU */
.top-bu {
    padding: 30px;
    border-radius: 20px;
    background: linear-gradient(135deg, #f59e0b, #f97316);
    color: white;
    text-align: center;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}

/* CTA */
.cta {
    padding: 30px;
    border-radius: 20px;
    background: linear-gradient(135deg, #10b981, #22c55e);
    color: white;
    text-align: center;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}

</style>
""", unsafe_allow_html=True)


# -------------------------
# MAIN
# -------------------------
def render():
    session = safe_get_session()
    stats = safe_stats()
    top_bu = safe_top_bu()

    user_ideas = get_user_ideas(session["user_id"]) or []
    user_count = len(user_ideas)

    # HEADER
    st.markdown(f"""
    <div class="header">
        <h1>🚀 TEOA Procurement Idea Hub</h1>
        <p>Welcome back, <b>{session['full_name'] or session['username']}</b></p>
    </div>
    """, unsafe_allow_html=True)

    # KPI ROW
    col1, col2, col3, col4 = st.columns(4)

    def kpi(col, value, label):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-number">{value}</div>
                <div class="kpi-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    kpi(col1, stats['total'], "Total Ideas")
    kpi(col2, stats['this_month'], "This Month")
    kpi(col3, stats['this_year'], "This Year")
    kpi(col4, user_count, "Your Ideas")

    st.markdown("<br>", unsafe_allow_html=True)

    # SECOND ROW (2-COLUMN LAYOUT)
    left, right = st.columns([2, 1])

    with left:
        st.markdown("""
        <div class="feature-card">
            <h3>💡 Why Share Ideas?</h3>
            <ul>
                <li>Drive operational excellence</li>
                <li>Make real business impact</li>
                <li>Collaborate across teams</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="cta">
            <h2>✨ Have an idea?</h2>
            <h3>Submit your idea and help shape the future!</h3>
            <p>Ideas reviewed weekly.</p>
        </div>
        """, unsafe_allow_html=True)

    with right:
        if top_bu:
            st.markdown(f"""
            <div class="top-bu">
                <h3>🏆 Top BU</h3>
                <h2>{top_bu['name']}</h2>
                <h1>{top_bu['count']}</h1>
                <p>ideas this month</p>
            </div>
            """, unsafe_allow_html=True)


# -------------------------
# RUN
# -------------------------
render()
