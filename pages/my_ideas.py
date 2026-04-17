import streamlit as st
import json
import io
import os
from datetime import datetime
import pandas as pd
from database import (
    get_user_ideas,
    update_idea,
    delete_idea,
    ideas_to_dataframe,
    get_audit_log,
    log_idea_changes,
    get_idea_by_id,
)

st.markdown(
    """
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
        background: #FF8C00;
        color: white;
    }
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
        border-left: 3px solid #FF8C00;
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
    
    /* Make checkbox check mark black */
    div[data-testid="stCheckbox"] svg path {
        fill: #000000 !important;
    }
    
    /* Form Section Cards - Matching submit_idea.py */
    .form-section {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
    }
    
    .section-title {
        font-size: 16px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .section-title .number {
        background: #FF8C00;
        color: white;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 600;
    }
    
    /* Toggle section */
    .toggle-section {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 20px 24px;
        margin: 24px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    /* Implementation details card */
    .implementation-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 24px;
        margin-top: 24px;
    }
    
    .subsection-title {
        font-size: 14px;
        font-weight: 600;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 24px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid #E5E7EB;
    }
    
    .subsection-title:first-child {
        margin-top: 0;
    }
    
    /* File attachment styling */
    .file-section {
        background: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
    }
    
    .file-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 0;
        border-bottom: 1px solid #E5E7EB;
    }
    
    .file-item:last-child {
        border-bottom: none;
    }
 </style>
""",
    unsafe_allow_html=True,
)

DRIVERS_OPTIONS = [
    "Automation of Process",
    "Use of AI tool",
    "Automation of Reports",
    "Creation of Standard Process, templates or any other resources",
    "Elimination of Rework loop",
    "Reduction of Steps in Process",
    "Empower team on self-service tools",
    "Other - specify in open box",
]

IMPACT_GROUP_OPTIONS = ["Within the site", "Cross Function", "Both"]

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
    "RESINs",
]


def render_edit_form(idea):
    """Render edit form for an idea"""
    st.markdown("### ✏️ Edit Idea")
    st.markdown(
        "Update your idea details below. All fields marked with * are required."
    )

    with st.form("edit_idea_form"):
        # Section 1: Basic Information
        st.markdown(
            """
        <div class="form-section">
            <div class="section-title">
                <span class="number">1</span>
                Project Details
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        new_title = st.text_input("Project Title *", value=idea["title"] or "")

        # Proposed Change - Full width for better paragraph input
        new_proposed_change = st.text_area(
            "Proposed Change *", value=idea["proposed_change"] or "", height=150
        )

        col1, col2 = st.columns(2)
        with col1:
            new_project_lead = st.text_input(
                "Project Lead *", value=idea["project_lead"] or ""
            )
        with col2:
            new_region = st.selectbox(
                "Region *",
                REGION_OPTIONS,
                index=REGION_OPTIONS.index(idea["region"])
                if idea["region"] in REGION_OPTIONS
                else 0,
            )

        new_bu_cl_site = st.selectbox(
            "BU/CL Site *",
            BU_CL_SITE_OPTIONS,
            index=BU_CL_SITE_OPTIONS.index(idea["bu_cl_site"])
            if idea["bu_cl_site"] in BU_CL_SITE_OPTIONS
            else 0,
        )

        # Section 2: Context & Impact
        st.markdown(
            """
        <div class="form-section">
            <div class="section-title">
                <span class="number">2</span>
                Context & Impact
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        new_problem_statements = st.text_area(
            "Problem Statements *", value=idea["problem_statements"] or "", height=80
        )

        new_benefits = st.text_area(
            "Expected Benefits *", value=idea["benefits"] or "", height=80
        )

        # Implementation Toggle
        st.markdown(
            """
        <div class="toggle-section">
            <div>
                <div style="font-size: 15px; font-weight: 500; color: #111827;">Is this already implemented?</div>
                <div style="font-size: 13px; color: #6B7280; margin-top: 4px;">Toggle if this idea has been put into practice</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        new_is_implemented = st.checkbox(
            "Yes, this idea is implemented",
            value=idea["is_implemented"] == "Yes",
            key="edit_is_implemented",
            label_visibility="collapsed",
        )

        # Section 3: Attachments
        st.markdown(
            """
        <div class="form-section">
            <div class="section-title">
                <span class="number">3</span>
                Attachments
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("**📎 Current Attachments**")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("*Capacity Files:*")
            existing_capacity = []
            if idea.get("capacity_files"):
                try:
                    existing_capacity = json.loads(idea["capacity_files"])
                except:
                    existing_capacity = [idea["capacity_files"]]

            if existing_capacity:
                for idx, fpath in enumerate(existing_capacity):
                    col_cb, col_name = st.columns([1, 5])
                    with col_cb:
                        st.checkbox("Remove", key=f"rem_cap_{idea['id']}_{idx}")
                    with col_name:
                        st.text(f"📄 {os.path.basename(fpath)}")
            else:
                st.caption("No capacity files attached")

        with col2:
            st.markdown("*Before Implementation:*")
            existing_before = []
            if idea.get("before_implementation_files"):
                try:
                    existing_before = json.loads(idea["before_implementation_files"])
                except:
                    existing_before = [idea["before_implementation_files"]]

            if existing_before:
                for idx, fpath in enumerate(existing_before):
                    col_cb, col_name = st.columns([1, 5])
                    with col_cb:
                        st.checkbox("Remove", key=f"rem_before_{idea['id']}_{idx}")
                    with col_name:
                        st.text(f"📄 {os.path.basename(fpath)}")
            else:
                st.caption("No before implementation files")

        with col3:
            st.markdown("*After Implementation:*")
            existing_after = []
            if idea.get("after_implementation_files"):
                try:
                    existing_after = json.loads(idea["after_implementation_files"])
                except:
                    existing_after = [idea["after_implementation_files"]]

            if existing_after:
                for idx, fpath in enumerate(existing_after):
                    col_cb, col_name = st.columns([1, 5])
                    with col_cb:
                        st.checkbox("Remove", key=f"rem_after_{idea['id']}_{idx}")
                    with col_name:
                        st.text(f"📄 {os.path.basename(fpath)}")
            else:
                st.caption("No after implementation files")

        st.markdown("---")
        st.markdown("**➕ Add New Attachments**")

        col_upload1, col_upload2, col_upload3 = st.columns(3)

        with col_upload1:
            st.markdown("**📎 Capacity Files**")
            st.markdown(
                "[📋 TEOA Capacity Calculation Template](https://te360.sharepoint.com/:x:/s/TEOAStandardDocumentation/IQCCGJzTZT9kQLvz0x0sRTReAf7WF6E7ThK_o_vWnUgIRFg?e=LOBGo7)"
            )
            new_capacity_files = st.file_uploader(
                "Add capacity files",
                type=None,
                accept_multiple_files=True,
            )

        with col_upload2:
            st.markdown("**Before Implementation**")
            new_before_files = st.file_uploader(
                "Add before implementation files",
                type=None,
                accept_multiple_files=True,
                key=f"edit_before_files_{idea['id']}",
            )

        with col_upload3:
            st.markdown("**After Implementation**")
            new_after_files = st.file_uploader(
                "Add after implementation files",
                type=None,
                accept_multiple_files=True,
                key=f"edit_after_files_{idea['id']}",
            )

        # Initialize with current values or defaults
        current_drivers = []
        if idea["drivers"]:
            try:
                current_drivers = json.loads(idea["drivers"])
            except:
                current_drivers = [idea["drivers"]] if idea["drivers"] else []

        # Extract existing "Other" value from drivers
        current_drivers_other = ""
        for d in current_drivers:
            if d and isinstance(d, str) and d.startswith("Other: "):
                current_drivers_other = d.replace("Other: ", "", 1)
                break

        current_effective_date = None
        if idea["effective_date"]:
            try:
                from datetime import datetime

                current_effective_date = datetime.strptime(
                    str(idea["effective_date"]), "%Y-%m-%d"
                ).date()
            except:
                current_effective_date = None

        # Section 4: Implementation Details
        st.markdown(
            """
        <div class="form-section">
            <div class="section-title">
                <span class="number">4</span>
                Implementation Details
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Drivers for Capacity Creation - Always visible (not conditional)
        new_drivers = st.multiselect(
            "Drivers for Capacity Creation",
            DRIVERS_OPTIONS,
            default=current_drivers,
            key=f"drivers_multiselect_{idea['id']}",
        )

        new_drivers_other = ""
        if "Other - specify in open box" in new_drivers:
            new_drivers_other = st.text_input(
                "Please specify",
                placeholder="Please specify...",
                value=current_drivers_other,
                key=f"drivers_other_{idea['id']}",
            )

        # Initialize optional fields
        new_effective_date = None
        new_impact_group = None
        new_hours_saved = 0
        new_planned_use = ""
        new_solution_implemented = ""
        new_date_implemented = None

        # All Implementation Details always visible (not conditional on is_implemented)
        col1, col2 = st.columns(2)
        with col1:
            new_effective_date = st.date_input(
                "Effective Date", value=current_effective_date
            )
        with col2:
            new_impact_group = st.selectbox(
                "Impact Group",
                IMPACT_GROUP_OPTIONS,
                index=IMPACT_GROUP_OPTIONS.index(idea["impact_group"])
                if idea["impact_group"] in IMPACT_GROUP_OPTIONS
                else 0,
            )

        col1, col2 = st.columns(2)
        with col1:
            new_hours_saved = st.number_input(
                "Projected Hours Saved Annually",
                min_value=0,
                step=1,
                value=int(idea["hours_saved"]) if idea["hours_saved"] else 0,
            )
        with col2:
            new_planned_use = st.text_area(
                "Planned Use for Capacity Created",
                value=idea["planned_use"] or "",
                height=60,
            )

        st.markdown("---")
        st.markdown("**Implementation Status**")

        col1, col2 = st.columns(2)
        with col1:
            new_solution_implemented = st.text_area(
                "Solution Implemented",
                value=idea.get("solution_implemented") or "",
                height=80,
            )
        with col2:
            current_date_implemented = None
            if idea.get("date_implemented"):
                try:
                    current_date_implemented = datetime.strptime(
                        str(idea["date_implemented"]), "%Y-%m-%d"
                    ).date()
                except:
                    current_date_implemented = None
            new_date_implemented = st.date_input(
                "Date Implemented",
                value=current_date_implemented if current_date_implemented else None,
                key=f"date_implemented_edit_{idea['id']}",
            )

        col_cancel, col_spacer, col_save = st.columns([1, 4, 1])
        with col_cancel:
            cancel = st.form_submit_button("Cancel")
        with col_spacer:
            st.empty()
        with col_save:
            submitted = st.form_submit_button("Save Changes", type="primary")

        if submitted:
            effective_date_str = (
                new_effective_date.isoformat() if new_effective_date else None
            )

            # Validate capacity files if any uploaded
            if new_capacity_files:
                if len(new_capacity_files) < 2:
                    st.error(
                        "⚠️ Please upload both 'Before Change' and 'After Change' capacity files (2 files required)"
                    )
                    return

            final_drivers = new_drivers.copy()
            if new_drivers_other:
                if "Other" in final_drivers:
                    final_drivers.remove("Other")
                if "Other - specify in open box" in final_drivers:
                    final_drivers.remove("Other - specify in open box")
                final_drivers = [d for d in final_drivers if d != "Other"]
                final_drivers.append(f"Other: {new_drivers_other}")

            # Handle file attachments
            files_to_remove_capacity = []
            files_to_remove_before = []
            files_to_remove_after = []

            # Build list of files to remove based on checkboxes
            for idx in range(len(existing_capacity)):
                if st.session_state.get(f"rem_cap_{idea['id']}_{idx}", False):
                    files_to_remove_capacity.append(existing_capacity[idx])

            for idx in range(len(existing_before)):
                if st.session_state.get(f"rem_before_{idea['id']}_{idx}", False):
                    files_to_remove_before.append(existing_before[idx])

            for idx in range(len(existing_after)):
                if st.session_state.get(f"rem_after_{idea['id']}_{idx}", False):
                    files_to_remove_after.append(existing_after[idx])

            # Delete removed files from filesystem
            for fpath in files_to_remove_capacity:
                if os.path.exists(fpath):
                    try:
                        os.remove(fpath)
                    except:
                        pass

            for fpath in files_to_remove_before:
                if os.path.exists(fpath):
                    try:
                        os.remove(fpath)
                    except:
                        pass

            for fpath in files_to_remove_after:
                if os.path.exists(fpath):
                    try:
                        os.remove(fpath)
                    except:
                        pass

            # Build final file lists (remove checked + add new)
            final_capacity = [
                f for f in existing_capacity if f not in files_to_remove_capacity
            ]
            final_before = [
                f for f in existing_before if f not in files_to_remove_before
            ]
            final_after = [f for f in existing_after if f not in files_to_remove_after]

            # Combine with new uploads
            combined_capacity = final_capacity.copy()
            if new_capacity_files:
                for uploaded_file in new_capacity_files:
                    combined_capacity.append(uploaded_file)

            combined_before = final_before.copy()
            if new_before_files:
                for uploaded_file in new_before_files:
                    combined_before.append(uploaded_file)

            combined_after = final_after.copy()
            if new_after_files:
                for uploaded_file in new_after_files:
                    combined_after.append(uploaded_file)

            old_idea = get_idea_by_id(idea["id"])

            update_idea(
                idea_id=idea["id"],
                title=new_title,
                proposed_change=new_proposed_change,
                project_lead=new_project_lead,
                bu_cl_site=new_bu_cl_site,
                problem_statements=new_problem_statements,
                benefits=new_benefits,
                is_implemented="Yes" if new_is_implemented else "No",
                effective_date=effective_date_str,
                drivers=final_drivers,
                impact_group=new_impact_group if new_is_implemented else None,
                hours_saved=new_hours_saved if new_is_implemented else None,
                capacity_files=combined_capacity if combined_capacity else None,
                planned_use=new_planned_use if new_is_implemented else None,
                before_implementation_files=combined_before
                if combined_before
                else None,
                after_implementation_files=combined_after if combined_after else None,
                solution_implemented=new_solution_implemented
                if new_is_implemented
                else None,
                date_implemented=new_date_implemented.isoformat()
                if new_date_implemented
                else None,
            )

            new_idea_data = {
                "title": new_title,
                "proposed_change": new_proposed_change,
                "project_lead": new_project_lead,
                "bu_cl_site": new_bu_cl_site,
                "problem_statements": new_problem_statements,
                "benefits": new_benefits,
                "is_implemented": "Yes" if new_is_implemented else "No",
                "effective_date": effective_date_str,
                "drivers": json.dumps(final_drivers) if final_drivers else None,
                "impact_group": new_impact_group,
                "hours_saved": new_hours_saved,
                "planned_use": new_planned_use,
            }

            log_idea_changes(idea["id"], old_idea, new_idea_data)

            st.success("✅ Changes have been saved.")
            st.session_state.edit_idea_id = None
            st.rerun()

        if cancel:
            st.rerun()

    if st.button("← Back to My Ideas"):
        st.session_state.edit_idea_id = None
        st.rerun()


def render():
    if "edit_idea_id" not in st.session_state:
        st.session_state.edit_idea_id = None

    if st.session_state.edit_idea_id:
        idea = get_idea_by_id(st.session_state.edit_idea_id)
        if idea:
            render_edit_form(idea)
        return

    st.markdown("### 📁 My Ideas")
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
            export_date = datetime.now().strftime("%Y-%m-%d")
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False, engine="openpyxl")
            buffer.seek(0)
            st.download_button(
                label="📥 Export",
                data=buffer,
                file_name=f"my_ideabox_ideas_{export_date}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        st.markdown("---")

        for idea in ideas:
            drivers_list = []
            if idea["drivers"]:
                try:
                    drivers_list = json.loads(idea["drivers"])
                except:
                    drivers_list = [idea["drivers"]] if idea["drivers"] else []

            with st.container():
                st.markdown(
                    f"""
                <div class="my-idea-card">
                    <div class="idea-header">
                        <div class="idea-title">{idea["title"]}</div>
                    </div>
                    <div class="idea-stats">
                        <span class="stat-pill">📍 {idea["region"] or "N/A"}</span>
                        <span class="stat-pill">🏢 {idea["bu_cl_site"] or "N/A"}</span>
                        <span class="stat-pill">📅 {idea["submitted_at"][:10]}</span>
                        <span class="stat-pill votes">👍 {idea["votes"]} likes</span>
                        <span class="stat-pill">Implemented: {idea["is_implemented"] or "No"}</span>
                    </div>
                    <p style="color: #636e72; font-size: 14px; margin-bottom: 10px;">{idea["proposed_change"] or ""}</p>
                """,
                    unsafe_allow_html=True,
                )

            with st.expander("View Full Details"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Project Lead:** {idea['project_lead'] or 'N/A'}")
                    st.markdown(f"**BU/CL Site:** {idea['bu_cl_site'] or 'N/A'}")
                    st.markdown(
                        f"**Problem Statements:** {idea['problem_statements'] or 'N/A'}"
                    )
                    if idea["site_leader"]:
                        st.markdown(f"**Site Leader:** {idea['site_leader']}")
                    if idea["teoa_leader"]:
                        st.markdown(
                            f"**TEOA Functional Leader:** {idea['teoa_leader']}"
                        )
                with col2:
                    st.markdown(f"**Expected Benefits:** {idea['benefits'] or 'N/A'}")
                    if idea["hours_saved"]:
                        st.markdown(f"**Hours Saved:** {idea['hours_saved']}")
                    if drivers_list:
                        st.markdown(f"**Drivers:** {', '.join(drivers_list)}")

            col1, col2, col3 = st.columns([5, 1, 1])

            with col1:
                with st.expander("📋 View Audit Trail"):
                    audit_logs = get_audit_log(idea["id"])
                    if audit_logs:
                        for log in audit_logs:
                            st.markdown(
                                f"""
                            <div class="audit-entry">
                                <div class="audit-field">Field: {log["field_name"]}</div>
                                <div class="audit-old">Old: {log["old_value"] or "(empty)"}</div>
                                <div class="audit-new">New: {log["new_value"] or "(empty)"}</div>
                                <div class="audit-date">{log["changed_at"]}</div>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )
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
        st.markdown(
            """
        <div style="text-align: center; padding: 60px 20px; background: #ffffff; border-radius: 12px; border: 2px dashed #e2e8f0;">
            <div style="font-size: 48px; margin-bottom: 16px;">📭</div>
            <h3 style="color: #1e293b; margin-bottom: 8px;">No ideas yet</h3>
            <p style="color: #64748b; margin-bottom: 20px;">You haven't submitted any ideas yet.<br>Start sharing your improvement suggestions!</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button("Submit Your First Idea", type="primary"):
            st.session_state.current_page = "submit_idea"
            st.rerun()
