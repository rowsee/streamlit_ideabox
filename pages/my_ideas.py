import streamlit as st
import json
import io
import pandas as pd
from database import get_user_ideas, update_idea, delete_idea, ideas_to_dataframe, get_audit_log, log_idea_changes, get_idea_by_id

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
    .edit-btn button {
        background: #EFF6FF !important;
        color: #2563EB !important;
        border: none !important;
        border-radius: 8px !important;
    }
    .edit-btn button:hover {
        background: #DBEAFE !important;
    }
    .audit-entry {
        background: #F8FAFC;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 8px;
        border-left: 3px solid #FF6B35;
    }
    .audit-field {
        font-weight: 600;
        color: #1E3A5F;
        font-size: 13px;
    }
    .audit-old {
        color: #DC2626;
        font-size: 12px;
    }
    .audit-new {
        color: #16A34A;
        font-size: 12px;
    }
    .audit-date {
        color: #9CA3AF;
        font-size: 11px;
        margin-top: 4px;
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

REGION_OPTIONS = ["", "EMEA", "NA", "AP", "Global"]

BU_CL_SITE_OPTIONS = [
    "",
    "ACL(CLS/PTS)",
    "ACL(IND)",
    "ADM",
    "ENG",
    "DDN",
    "MED",
    "ASG",
    "AUT-AMER",
    "AUT-EMIA",
    "AUT-AP",
    "ICT",
    "SEN",
    "ELECs",
    "INDIRECT",
    "METALs",
    "RESINs"
]

def render_edit_form(idea):
    """Render edit form for an idea"""
    st.markdown("### ✏️ Edit Idea")
    
    with st.form("edit_idea_form"):
        col1, col2 = st.columns([2, 1])
        with col1:
            new_title = st.text_input("Project Title", value=idea["title"] or "")
        with col2:
            new_project_type = st.selectbox(
                "Project Type",
                PROJECT_TYPE_OPTIONS,
                index=PROJECT_TYPE_OPTIONS.index(idea["project_type"]) if idea["project_type"] in PROJECT_TYPE_OPTIONS else 0
            )
        
        new_description = st.text_area(
            "Project Description",
            value=idea["description"] or "",
            height=100
        )
        
        col1, col2 = st.columns(2)
        with col1:
            new_project_lead = st.text_input(
                "Project Lead",
                value=idea["project_lead"] or ""
            )
        with col2:
            new_region = st.selectbox(
                "Region",
                REGION_OPTIONS,
                index=REGION_OPTIONS.index(idea["region"]) if idea["region"] in REGION_OPTIONS else 0
            )
        
        new_bu_cl_site = st.selectbox(
            "BU/CL Site",
            BU_CL_SITE_OPTIONS,
            index=BU_CL_SITE_OPTIONS.index(idea["bu_cl_site"]) if idea["bu_cl_site"] in BU_CL_SITE_OPTIONS else 0
        )
        
        new_problem_statements = st.text_area(
            "Problem Statements",
            value=idea["problem_statements"] or "",
            height=80
        )
        
        new_benefits = st.text_area(
            "Expected Benefits",
            value=idea["benefits"] or "",
            height=80
        )
        
        new_is_implemented = st.toggle(
            "Is this already implemented?",
            value=idea["is_implemented"] == "Yes"
        )
        
        new_effective_date = None
        new_impact_group = None
        new_drivers = []
        new_drivers_other = ""
        new_hours_saved = 0
        new_planned_use = ""
        
        if new_is_implemented:
            st.markdown("#### Implementation Details")
            
            col1, col2 = st.columns(2)
            with col1:
                if idea["effective_date"]:
                    effective_date_obj = idea["effective_date"].split("-")
                    new_effective_date = st.date_input(
                        "Effective Date",
                        value=(
                            int(effective_date_obj[0]),
                            int(effective_date_obj[1]),
                            int(effective_date_obj[2])
                        ) if len(effective_date_obj) == 3 else None
                    )
                else:
                    new_effective_date = st.date_input("Effective Date", value=None)
            with col2:
                new_impact_group = st.selectbox(
                    "Impact Group",
                    IMPACT_GROUP_OPTIONS,
                    index=IMPACT_GROUP_OPTIONS.index(idea["impact_group"]) if idea["impact_group"] in IMPACT_GROUP_OPTIONS else 0
                )
            
            current_drivers = []
            if idea["drivers"]:
                try:
                    current_drivers = json.loads(idea["drivers"])
                except:
                    current_drivers = [idea["drivers"]] if idea["drivers"] else []
            
            new_drivers = st.multiselect(
                "Drivers for Capacity Creation",
                DRIVERS_OPTIONS,
                default=current_drivers
            )
            
            new_drivers_other = ""
            if "Other" in new_drivers or "Other - specify in open box" in new_drivers:
                new_drivers_other = st.text_input(
                    "Other - Please Specify",
                    value=""
                )
            
            col1, col2 = st.columns(2)
            with col1:
                new_hours_saved = st.number_input(
                    "Projected Hours Saved Annually",
                    min_value=0,
                    step=1,
                    value=int(idea["hours_saved"]) if idea["hours_saved"] else 0
                )
            with col2:
                new_planned_use = st.text_area(
                    "Planned Use for Capacity Created",
                    value=idea["planned_use"] or "",
                    height=60
                )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            submitted = st.form_submit_button("Save Changes", type="primary")
        with col2:
            cancel = st.form_submit_button("Cancel")
        
        if submitted:
            effective_date_str = new_effective_date.isoformat() if new_effective_date else None
            
            final_drivers = new_drivers.copy()
            if new_drivers_other:
                if "Other" in final_drivers:
                    final_drivers.remove("Other")
                if "Other - specify in open box" in final_drivers:
                    final_drivers.remove("Other - specify in open box")
                final_drivers = [d for d in final_drivers if d != "Other"]
                final_drivers.append(f"Other: {new_drivers_other}")
            
            old_idea = get_idea_by_id(idea["id"])
            
            update_idea(
                idea_id=idea["id"],
                title=new_title,
                description=new_description,
                project_lead=new_project_lead,
                bu_cl_site=new_bu_cl_site,
                project_type=new_project_type,
                problem_statements=new_problem_statements,
                benefits=new_benefits,
                is_implemented="Yes" if new_is_implemented else "No",
                effective_date=effective_date_str,
                drivers=final_drivers,
                impact_group=new_impact_group if new_is_implemented else None,
                hours_saved=new_hours_saved if new_is_implemented else None,
                capacity_file=None,
                planned_use=new_planned_use if new_is_implemented else None,
                email_approval=None
            )
            
            new_idea_data = {
                "title": new_title,
                "description": new_description,
                "project_lead": new_project_lead,
                "bu_cl_site": new_bu_cl_site,
                "project_type": new_project_type,
                "problem_statements": new_problem_statements,
                "benefits": new_benefits,
                "is_implemented": "Yes" if new_is_implemented else "No",
                "effective_date": effective_date_str,
                "drivers": json.dumps(final_drivers) if final_drivers else None,
                "impact_group": new_impact_group,
                "hours_saved": new_hours_saved,
                "planned_use": new_planned_use
            }
            
            log_idea_changes(idea["id"], old_idea, new_idea_data)
            
            st.success("Idea updated successfully!")
            st.rerun()
        
        if cancel:
            st.rerun()
    
    if st.button("← Back to My Ideas"):
        st.rerun()

def render():
    if "edit_idea_id" not in st.session_state:
        st.session_state.edit_idea_id = None
    
    if st.session_state.edit_idea_id:
        idea = get_idea_by_id(st.session_state.edit_idea_id)
        if idea:
            render_edit_form(idea)
        return
    
    st.markdown("## 🏆 My Ideas")
    st.markdown("View and manage your submitted ideas.")
    
    ideas = get_user_ideas(st.session_state.user_id)
    
    if ideas:
        total_votes = sum(idea["votes"] for idea in ideas)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Ideas", len(ideas))
        with col2:
            st.metric("Total Likes", total_votes)
        with col3:
            avg_votes = total_votes / len(ideas) if ideas else 0
            st.metric("Avg Likes", f"{avg_votes:.1f}")
        
        # Export button
        col_export, _ = st.columns([1, 4])
        with col_export:
            df = ideas_to_dataframe(ideas)
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            st.download_button(
                label="📥 Export My Ideas to Excel",
                data=buffer,
                file_name="my_ideabox_ideas.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
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
                        <span class="stat-pill votes">👍 {idea["votes"]} likes</span>
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
                    if idea["site_leader"]:
                        st.markdown(f"**Site Leader:** {idea['site_leader']}")
                    if idea["teoa_leader"]:
                        st.markdown(f"**TEOA Functional Leader:** {idea['teoa_leader']}")
                with col2:
                    st.markdown(f"**Expected Benefits:** {idea['benefits'] or 'N/A'}")
                    if idea['hours_saved']:
                        st.markdown(f"**Hours Saved:** {idea['hours_saved']}")
                    if drivers_list:
                        st.markdown(f"**Drivers:** {', '.join(drivers_list)}")
            
            col1, col2, col3 = st.columns([5, 1, 1])
            
            with col1:
                with st.expander("📋 View Audit Trail"):
                    audit_logs = get_audit_log(idea["id"])
                    if audit_logs:
                        for log in audit_logs:
                            st.markdown(f"""
                            <div class="audit-entry">
                                <div class="audit-field">Field: {log['field_name']}</div>
                                <div class="audit-old">Old: {log['old_value'] or '(empty)'}</div>
                                <div class="audit-new">New: {log['new_value'] or '(empty)'}</div>
                                <div class="audit-date">{log['changed_at']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No changes recorded yet.")
            
            with col2:
                st.markdown("<div class='edit-btn'>", unsafe_allow_html=True)
                if st.button(f"✏️ Edit", key=f"edit_{idea['id']}"):
                    st.session_state.edit_idea_id = idea["id"]
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col3:
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
