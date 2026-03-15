import streamlit as st
import json
from database import get_user_ideas, update_idea, delete_idea

st.markdown("""
<style>
    .my-idea-card {
        background: #FFFFFF;
        padding: 20px 25px;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
        border: 1px solid #E2E8F0;
        margin-bottom: 15px;
    }
    .idea-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 10px;
    }
    .idea-title {
        font-size: 20px;
        font-weight: 600;
        color: #1E3A5F;
    }
    .idea-stats {
        display: flex;
        gap: 12px;
        margin: 10px 0;
        flex-wrap: wrap;
    }
    .stat-pill {
        background: #F1F5F9;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 13px;
        color: #64748B;
    }
    .stat-pill.votes {
        background: #FF6B35;
        color: white;
    }
    .type-pill {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 13px;
    }
    .type-low { background: #DCFCE7; color: #16A34A; }
    .type-medium { background: #FEF3C7; color: #D97706; }
    .type-high { background: #FEE2E2; color: #DC2626; }
    .delete-btn button {
        background: #FEE2E2 !important;
        color: #DC2626 !important;
        border: none !important;
        border-radius: 8px !important;
    }
    .delete-btn button:hover {
        background: #DC2626 !important;
        color: white !important;
    }
    .stats-row {
        background: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        background: #FFFFFF;
        border-radius: 12px;
        border: 2px dashed #E2E8F0;
    }
    .empty-state-icon {
        font-size: 64px;
        margin-bottom: 20px;
    }
    .empty-state-title {
        font-size: 20px;
        font-weight: 600;
        color: #1E3A5F;
        margin-bottom: 10px;
    }
    .empty-state-text {
        color: #64748B;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

DRIVERS_OPTIONS = [
    "Automation of Process",
    "Use of AI tool",
    "Automation of Reports",
    "Creation of Standard Process, templates or any other resources",
    "Elimination of Rework loop",
    "Reduction of Steps in Process",
    "Empower team on self-service tools",
    "Other - specify in open box"
]

IMPACT_GROUP_OPTIONS = ["Within the site", "Cross Function", "Both"]
PROJECT_TYPE_OPTIONS = ["Low", "Medium", "High"]

def render():
    st.markdown("## 🏆 My Ideas")
    st.markdown("View and manage your submitted ideas.")
    
    ideas = get_user_ideas(st.session_state.user_id)
    
    if ideas:
        total_votes = sum(idea["votes"] for idea in ideas)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Ideas", len(ideas))
        with col2:
            st.metric("Total Votes", total_votes)
        with col3:
            avg_votes = total_votes / len(ideas) if ideas else 0
            st.metric("Avg Votes", f"{avg_votes:.1f}")
        
        st.markdown("---")
        
        for idea in ideas:
            type_class = f"type-{idea['project_type'].lower()}" if idea['project_type'] else ""
            
            drivers_list = []
            if idea["drivers"]:
                try:
                    drivers_list = json.loads(idea["drivers"])
                except:
                    drivers_list = [idea["drivers"]] if idea["drivers"] else []
            
            with st.container():
                st.markdown(f"""
                <div class="my-idea-card">
                    <div class="idea-header">
                        <div class="idea-title">{idea["title"]}</div>
                        <span class="type-pill {type_class}">{idea["project_type"] or "N/A"} Priority</span>
                    </div>
                    <div class="idea-stats">
                        <span class="stat-pill">📍 {idea["region"] or "N/A"}</span>
                        <span class="stat-pill">🏢 {idea["bu_cl_site"] or "N/A"}</span>
                        <span class="stat-pill">📅 {idea["submitted_at"][:10]}</span>
                        <span class="stat-pill votes">👍 {idea["votes"]} votes</span>
                        <span class="stat-pill">Status: {idea["status"] or "Pending"}</span>
                        <span class="stat-pill">Implemented: {idea["is_implemented"] or "No"}</span>
                    </div>
                    <p style="color: #636e72; font-size: 14px; margin-bottom: 10px;">{idea["description"]}</p>
                """, unsafe_allow_html=True)
            
            with st.expander("View Full Details"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Project Lead:** {idea['project_lead'] or 'N/A'}")
                    st.markdown(f"**BU/CL Site:** {idea['bu_cl_site'] or 'N/A'}")
                    st.markdown(f"**Problem Statements:** {idea['problem_statements'] or 'N/A'}")
                with col2:
                    st.markdown(f"**Expected Benefits:** {idea['benefits'] or 'N/A'}")
                    if idea['hours_saved']:
                        st.markdown(f"**Hours Saved:** {idea['hours_saved']}")
                    if drivers_list:
                        st.markdown(f"**Drivers:** {', '.join(drivers_list)}")
            
            col1, col2 = st.columns([6, 1])
            
            with col1:
                pass
            
            with col2:
                st.markdown("<div class='delete-btn'>", unsafe_allow_html=True)
                if st.button(f"🗑️ Delete", key=f"delete_{idea['id']}"):
                    delete_idea(idea["id"])
                    st.success("Idea deleted!")
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("---")
    else:
        st.info("You haven't submitted any ideas yet.")
        
        st.page_link("pages/submit_idea.py", label="💡 Submit Your First Idea", icon="💡")
