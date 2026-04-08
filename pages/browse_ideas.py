import streamlit as st
import pandas as pd
import io
import json
import os
from datetime import datetime
from database import get_all_ideas, vote_idea, has_voted, ideas_to_dataframe

st.markdown(
    """
<style>
    .idea-card {
        background: #FFFFFF;
        padding: 20px 25px;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
        border: 1px solid #E2E8F0;
        margin-bottom: 15px;
    }
    .idea-title {
        font-size: 20px;
        font-weight: 600;
        color: #1E3A5F;
        margin-bottom: 8px;
    }
    .idea-meta {
        display: flex;
        gap: 12px;
        margin-bottom: 12px;
        flex-wrap: wrap;
    }
    .meta-item {
        font-size: 13px;
        color: #64748B;
    }
    .category-tag {
        background: #FF6B35;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    .status-pending { background: #FEF3C7; color: #D97706; }
    .status-reviewed { background: #DBEAFE; color: #2563EB; }
    .status-implemented { background: #DCFCE7; color: #16A34A; }
    .implemented-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    .implemented-yes { background: #DCFCE7; color: #16A34A; }
    .implemented-no { background: #F3F4F6; color: #6B7280; }
    .detail-label {
        font-weight: 600;
        color: #1E3A5F;
        font-size: 13px;
    }
    .detail-value {
        color: #64748B;
        font-size: 13px;
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
    .vote-button {
        background: transparent !important;
        border: 2px solid #FF6B35 !important;
        color: #FF6B35 !important;
        border-radius: 20px !important;
        padding: 8px 16px !important;
    }
    .vote-button:hover {
        background: #FF6B35 !important;
        color: white !important;
    }
    .voted {
        background: #FF6B35 !important;
        color: white !important;
    }
    .search-filter-bar {
        background: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
</style>
""",
    unsafe_allow_html=True,
)

REGION_OPTIONS = ["All", "EMEA", "NA", "AP", "Global"]

BU_CL_SITE_OPTIONS = [
    "All",
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


def render():
    st.markdown("## 📋 Browse All Ideas")
    st.markdown("Explore ideas from across the organization and like your favorites.")

    ideas = get_all_ideas()

    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])

    with col1:
        search = st.text_input(
            "🔍 Search ideas...", placeholder="Search by title or description"
        )

    with col2:
        region_filter = st.selectbox("Region", REGION_OPTIONS)

    with col3:
        bu_filter = st.selectbox("BU", BU_CL_SITE_OPTIONS)

    with col4:
        implemented_filter = st.selectbox("Implemented", ["All", "Yes", "No"])

    with col5:
        sort_by = st.selectbox("Sort by", ["Newest", "Most Liked", "Oldest"])

    if ideas:
        filtered_ideas = ideas

        if search:
            search_lower = search.lower()
            filtered_ideas = [
                i
                for i in filtered_ideas
                if search_lower in (i["title"] or "").lower()
                or search_lower in (i["proposed_change"] or "").lower()
                or search_lower in (i["problem_statements"] or "").lower()
            ]

        if region_filter != "All":
            filtered_ideas = [i for i in filtered_ideas if i["region"] == region_filter]

        if bu_filter != "All":
            filtered_ideas = [i for i in filtered_ideas if i["bu_cl_site"] == bu_filter]

        if implemented_filter != "All":
            filtered_ideas = [
                i for i in filtered_ideas if i["is_implemented"] == implemented_filter
            ]

        if sort_by == "Most Liked":
            filtered_ideas = sorted(
                filtered_ideas, key=lambda x: x["votes"], reverse=True
            )
        elif sort_by == "Oldest":
            filtered_ideas = sorted(filtered_ideas, key=lambda x: x["submitted_at"])

        st.markdown(f"### Showing {len(filtered_ideas)} idea(s)")

        col_export, _ = st.columns([1, 4])
        with col_export:
            if filtered_ideas:
                df = ideas_to_dataframe(filtered_ideas)
                export_date = datetime.now().strftime("%Y-%m-%d")
                buffer = io.BytesIO()
                df.to_excel(buffer, index=False, engine="openpyxl")
                buffer.seek(0)
                st.download_button(
                    label="📥 Export to Excel",
                    data=buffer,
                    file_name=f"ideabox_ideas_{export_date}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )

        st.markdown("---")

        for idea in filtered_ideas:
            voted = has_voted(idea["id"], st.session_state.user_id)

            implemented_class = (
                "implemented-yes"
                if idea["is_implemented"] == "Yes"
                else "implemented-no"
            )

            with st.container():
                st.markdown(
                    f"""
                <div class="idea-card">
                    <div class="idea-title">{idea["title"]}</div>
                    <div class="idea-meta">
                        <span class="meta-item">📍 {idea["region"] or "N/A"}</span>
                        <span class="meta-item">🏢 {idea["bu_cl_site"] or "N/A"}</span>
                        <span class="meta-item">👤 {idea["full_name"] or idea["username"]}</span>
                        <span class="meta-item">📅 {idea["submitted_at"][:10]}</span>
                        <span class="implemented-badge {implemented_class}">{"✅ Implemented" if idea["is_implemented"] == "Yes" else "⏳ Not Implemented"}</span>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

            with st.expander("📝 View Details"):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"**Project Lead:** {idea['project_lead'] or 'N/A'}")
                    st.markdown(f"**BU/CL Site:** {idea['bu_cl_site'] or 'N/A'}")
                    st.markdown(f"**Is Implemented:** {idea['is_implemented'] or 'No'}")
                    if idea["is_implemented"] == "Yes":
                        if idea.get("solution_implemented"):
                            st.markdown(
                                f"**Solution Implemented:** {idea['solution_implemented']}"
                            )
                        if idea.get("date_implemented"):
                            st.markdown(
                                f"**Date Implemented:** {idea['date_implemented']}"
                            )
                        if idea.get("effective_date"):
                            st.markdown(f"**Effective Date:** {idea['effective_date']}")

                with col2:
                    st.markdown(f"**Likes:** {idea['votes']}")
                    if idea["hours_saved"]:
                        st.markdown(f"**Hours Saved Annually:** {idea['hours_saved']}")
                    if idea["impact_group"]:
                        st.markdown(f"**Impact Group:** {idea['impact_group']}")

                st.markdown("---")

                # Submitter and Leader info
                col1, col2 = st.columns(2)
                with col1:
                    submitter_name = (
                        idea["full_name"]
                        if idea["full_name"]
                        else (idea["username"] if idea["username"] else "Unknown")
                    )
                    st.markdown(f"**Submitted By:** {submitter_name}")
                    if idea["email"]:
                        st.markdown(f"**Submitter Email:** {idea['email']}")
                with col2:
                    if idea["site_leader"]:
                        st.markdown(f"**Site Leader:** {idea['site_leader']}")
                    if idea["teoa_leader"]:
                        st.markdown(
                            f"**TEOA Functional Leader:** {idea['teoa_leader']}"
                        )

                st.markdown("---")

                st.markdown(f"**Proposed Change:**")
                st.write(idea["proposed_change"] or "No proposed change specified")

                st.markdown(f"**Problem Statements:**")
                st.write(idea["problem_statements"] or "No problem statements")

                st.markdown(f"**Expected Benefits:**")
                st.write(idea["benefits"] or "No benefits specified")

                if idea["drivers"]:
                    import json

                    try:
                        drivers = json.loads(idea["drivers"])
                        st.markdown(f"**Drivers:** {', '.join(drivers)}")
                    except:
                        st.markdown(f"**Drivers:** {idea['drivers']}")

                if idea["planned_use"]:
                    st.markdown(f"**Planned Use:** {idea['planned_use']}")

                col1, col2, col3 = st.columns(3)
                with col1:
                    # Handle both single file (old) and multiple files (new)
                    capacity_files = idea.get("capacity_files")
                    if capacity_files:
                        try:
                            files_list = json.loads(capacity_files)
                        except:
                            files_list = [
                                capacity_files
                            ]  # Single file (backward compat)

                        for idx, file_path in enumerate(files_list):
                            if file_path and os.path.exists(file_path):
                                with open(file_path, "rb") as f:
                                    file_name = file_path.split("/")[-1]
                                    label = f"📎 Download Capacity File {idx + 1}"
                                    if len(files_list) == 1:
                                        label = "📎 Download Capacity File"
                                    st.download_button(
                                        label=label,
                                        data=f,
                                        file_name=file_name,
                                        use_container_width=True,
                                        key=f"capacity_{idea['id']}_{idx}",
                                    )
                with col2:
                    # Before Implementation files
                    before_files = idea.get("before_implementation_files")
                    if before_files:
                        try:
                            files_list = json.loads(before_files)
                        except:
                            files_list = [before_files]

                        for idx, file_path in enumerate(files_list):
                            if file_path and os.path.exists(file_path):
                                with open(file_path, "rb") as f:
                                    file_name = file_path.split("/")[-1]
                                    label = (
                                        f"📎 Download Before Implementation {idx + 1}"
                                    )
                                    if len(files_list) == 1:
                                        label = "📎 Download Before Implementation"
                                    st.download_button(
                                        label=label,
                                        data=f,
                                        file_name=file_name,
                                        use_container_width=True,
                                        key=f"before_{idea['id']}_{idx}",
                                    )
                with col3:
                    # After Implementation files
                    after_files = idea.get("after_implementation_files")
                    if after_files:
                        try:
                            files_list = json.loads(after_files)
                        except:
                            files_list = [after_files]

                        for idx, file_path in enumerate(files_list):
                            if file_path and os.path.exists(file_path):
                                with open(file_path, "rb") as f:
                                    file_name = file_path.split("/")[-1]
                                    label = (
                                        f"📎 Download After Implementation {idx + 1}"
                                    )
                                    if len(files_list) == 1:
                                        label = "📎 Download After Implementation"
                                    st.download_button(
                                        label=label,
                                        data=f,
                                        file_name=file_name,
                                        use_container_width=True,
                                        key=f"after_{idea['id']}_{idx}",
                                    )

            col1, col2 = st.columns([6, 1])

            with col2:
                if voted:
                    st.markdown(f"👍 {idea['votes']}")
                else:
                    if st.button(f"👍 Like", key=f"vote_{idea['id']}"):
                        vote_idea(idea["id"], st.session_state.user_id)
                        st.rerun()

            st.markdown("---")
    else:
        st.info("No ideas have been submitted yet. Be the first to share an idea!")
        if st.button("Submit the First Idea", type="primary"):
            st.session_state.current_page = "submit_idea"
            st.rerun()
