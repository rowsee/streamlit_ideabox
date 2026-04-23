import streamlit as st
from database import add_idea
from assignment_matrix import get_assignment
from notifications import send_idea_submission_notification

st.markdown(
    """
<style>
    /* Page header */
    .page-header {
        margin-bottom: 32px;
    }
    
    .page-header h1 {
        font-size: 28px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 8px;
    }
    
    .page-header p {
        color: #6B7280;
        font-size: 15px;
    }
    
    /* Form Section Cards */
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
        background: #ff6b36;
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
    
    /* Field row styling */
    .field-row {
        display: flex;
        gap: 16px;
        margin-bottom: 16px;
    }
    
    .field-row > div {
        flex: 1;
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
    
    .toggle-section .toggle-label {
        font-size: 15px;
        font-weight: 500;
        color: #111827;
    }
    
    .toggle-section .toggle-desc {
        font-size: 13px;
        color: #6B7280;
        margin-top: 4px;
    }
    
    /* Implementation details card */
    .implementation-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 24px;
        margin-top: 24px;
        animation: slideDown 0.3s ease;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
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
    
    /* Success Message */
    .success-box {
        background: #ECFDF5;
        color: #065F46;
        padding: 20px 24px;
        border-radius: 10px;
        border: 1px solid #A7F3D0;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .success-box .icon {
        font-size: 24px;
    }
    
    /* Error styling */
    .stError {
        background: #FEF2F2 !important;
        color: #991B1B !important;
        border: 1px solid #FECACA !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
    }
    
    /* Submit button container */
    .submit-container {
        display: flex;
        justify-content: center;
        margin: 32px 0;
    }
    
    /* Helper text */
    .helper-text {
        font-size: 12px;
        color: #9CA3AF;
        margin-top: 4px;
    }
    
    /* Required star */
    .required {
        color: #EF4444;
    }
    
    /* Fix Streamlit Toggle Visibility - Orange when ON, Black when OFF */
    div[data-testid="stToggle"] label {
        color: #1E3A5F !important;
    }

    div[data-testid="stToggle"] div[role="switch"] {
        background-color: #000000 !important;
    }

    div[data-testid="stToggle"] div[role="switch"][aria-checked="true"] {
        background-color: #ff6b36 !important;
    }
    
    /* Leader fields styling */
    .leader-field {
        background: #F3F4F6 !important;
        padding: 10px 14px !important;
        border-radius: 8px !important;
        border: 1px solid #E5E7EB !important;
        color: #6B7280 !important;
        font-size: 13px !important;
    }
 </style>
""",
    unsafe_allow_html=True,
)


def clear_all_form_fields():
    """Clear all form fields and widget session state"""
    # Clear form data
    st.session_state.idea_form = {
        "title": "",
        "proposed_change": "",
        "project_lead": "",
        "region": "",
        "bu_cl_site": "",
        "problem_statements": "",
        "benefits": "",
        "is_implemented": False,
        "solution_implemented": "",
        "date_implemented": None,
        "effective_date": None,
        "impact_group": "",
        "drivers": [],
        "drivers_other": "",
        "hours_saved": 0,
        "planned_use": "",
        "site_leader": "",
        "teoa_leader": "",
    }

    # Clear all widget session state keys
    widget_keys = [
        "title_input",
        "proposed_change_input",
        "lead_input",
        "region_select",
        "site_select",
        "problem_input",
        "benefits_input",
        "toggle_is_implemented",
        "solution_implemented_input",
        "date_implemented_input",
        "effective_date_input",
        "impact_select",
        "drivers_multiselect",
        "drivers_other_input",
        "hours_input",
        "planned_use_input",
        "capacity_file_input",
        "email_approval_input",
    ]
    for key in widget_keys:
        if key in st.session_state:
            del st.session_state[key]

    st.session_state.form_just_cleared = True
    st.session_state.show_success_popup = False
    st.session_state.success_message = ""


def show_success_popup(message):
    """Show success modal popup with action buttons"""
    if "show_success_popup" not in st.session_state:
        st.session_state.show_success_popup = False
        st.session_state.success_message = ""

    if st.session_state.show_success_popup:
        # Custom CSS for the success message
        st.markdown(
            """
        <style>
        .success-box {
            background: #ECFDF5;
            border: 1px solid #A7F3D0;
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            margin-bottom: 24px;
        }
        .success-icon {
            font-size: 48px;
            margin-bottom: 12px;
        }
        .success-message {
            font-size: 16px;
            font-weight: 500;
            color: #065F46;
            margin-bottom: 8px;
        }
        </style>
        <div class="success-box">
            <div class="success-icon">✅</div>
            <div class="success-message">"""
            + message
            + """</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Action buttons
        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "Submit Another", use_container_width=True, key="btn_submit_another"
            ):
                st.session_state.show_success_popup = False
                st.session_state.success_message = ""
                st.rerun()

        with col2:
            if st.button(
                "View My Submitted Ideas",
                use_container_width=True,
                key="btn_view_ideas",
            ):
                st.session_state.current_page = "my_ideas"
                st.rerun()

        # Stop further rendering
        st.stop()


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

DRIVERS_OPTIONS = [
    "Automation of Process",
    "Use of AI tool",
    "Automation of Reports",
    "Creation of Standard Process, templates or any other resources",
    "Elimination of Rework loop",
    "Reduction of Steps in Process",
    "Empower team on self-service tools",
    "Other",
]

IMPACT_GROUP_OPTIONS = ["", "Within the site", "Cross Function", "Both"]


def render():
    # Check and show success popup if triggered
    show_success_popup(st.session_state.get("success_message", ""))

    # Page header
    st.markdown(
        """
    <div class="page-header">
        <h1>💡 Submit Your Idea</h1>
        <p>Share your innovative ideas to help improve our organization.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Initialize session state for form values
    if "idea_form" not in st.session_state:
        st.session_state.idea_form = {
            "title": "",
            "proposed_change": "",
            "project_lead": "",
            "region": "",
            "bu_cl_site": "",
            "problem_statements": "",
            "benefits": "",
            "is_implemented": False,
            "solution_implemented": "",
            "date_implemented": None,
            "effective_date": None,
            "impact_group": "",
            "drivers": [],
            "drivers_other": "",
            "hours_saved": 0,
            "planned_use": "",
            "site_leader": "",
            "teoa_leader": "",
        }

    # Check if form was just cleared (after submission) - reinitialize to ensure fresh state
    if st.session_state.get("form_just_cleared"):
        st.session_state.idea_form = {
            "title": "",
            "proposed_change": "",
            "project_lead": "",
            "region": "",
            "bu_cl_site": "",
            "problem_statements": "",
            "benefits": "",
            "is_implemented": False,
            "solution_implemented": "",
            "date_implemented": None,
            "effective_date": None,
            "impact_group": "",
            "drivers": [],
            "drivers_other": "",
            "hours_saved": 0,
            "planned_use": "",
            "site_leader": "",
            "teoa_leader": "",
        }
        st.session_state.form_just_cleared = False

    # Guidelines section - shown before the form
    st.markdown("### 📝 Guidelines for a Great Idea Submission")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**1. Be Specific**")
        st.markdown("- Clear title that summarizes the idea")
        st.markdown("- Detailed description of what you're proposing")
        st.markdown("- Specific use cases or scenarios")

    with col2:
        st.markdown("**2. Focus on Value**")
        st.markdown("- Explain the problem you're solving")
        st.markdown("- Quantify potential benefits")
        st.markdown("- Consider impact on different stakeholders")

    with col3:
        st.markdown("**3. Be Practical**")
        st.markdown("- Consider implementation feasibility")
        st.markdown("- Think about resources needed")
        st.markdown("- Note any potential challenges")

    st.markdown("---")

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

    # Row 1: Title
    title = st.text_input(
        "Project Title",
        placeholder="Enter a clear, descriptive title",
        value=st.session_state.idea_form["title"],
        key="title_input",
    )

    # Proposed Change - Full width for better paragraph input
    proposed_change = st.text_area(
        "Proposed Change",
        placeholder="Describe what change you are proposing...",
        height=150,
        value=st.session_state.idea_form["proposed_change"],
        key="proposed_change_input",
    )

    # Row 2: Project Lead + Region
    col1, col2 = st.columns(2)
    with col1:
        project_lead = st.text_input(
            "Project Lead",
            placeholder="Name of person responsible",
            value=st.session_state.idea_form["project_lead"],
            key="lead_input",
        )
    with col2:
        region = st.selectbox(
            "Region",
            REGION_OPTIONS,
            index=None,
            placeholder="Select",
            key="region_select",
        )

    # Row 4: BU/CL Site
    bu_cl_site = st.selectbox(
        "BU/CL Site",
        BU_CL_SITE_OPTIONS,
        index=None,
        placeholder="Select",
        key="site_select",
    )

    # Get assignment based on Region + BU
    selected_region = region if region else ""
    selected_bu = bu_cl_site if bu_cl_site else ""

    site_leader = ""
    teoa_leader = ""
    assignment_emails = []
    mapping_warning = ""

    if selected_region and selected_bu:
        assignment = get_assignment(selected_region, selected_bu)

        site_leader = assignment.get("site_leader_str", "")
        teoa_leader = assignment.get("teoa_leader_str", "")
        assignment_emails = assignment.get("emails", [])

        if site_leader == "No mapping found" or teoa_leader == "No mapping found":
            mapping_warning = (
                f"⚠️ No mapping found for Region: {selected_region}, BU: {selected_bu}"
            )
            site_leader = ""
            teoa_leader = ""

    # Store in session state for use in submission
    st.session_state.idea_form["site_leader"] = site_leader
    st.session_state.idea_form["teoa_leader"] = teoa_leader

    # Row 5: Site Leader + TEOA Functional Leader (read-only, auto-populated)
    if mapping_warning:
        st.warning(mapping_warning)

    # Use html div for read-only display to ensure it renders properly
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Site Leader**")
        site_leader_display = (
            site_leader if site_leader and site_leader != "No mapping found" else "-"
        )
        st.markdown(
            f"""
        <div style="
            background: #F3F4F6;
            padding: 10px 14px;
            border-radius: 8px;
            border: 1px solid #E5E7EB;
            color: #374151;
            font-size: 14px;
            min-height: 38px;
            display: flex;
            align-items: center;
        ">{site_leader_display}</div>
        """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown("**TEOA Functional Leader**")
        teoa_leader_display = (
            teoa_leader if teoa_leader and teoa_leader != "No mapping found" else "-"
        )
        st.markdown(
            f"""
        <div style="
            background: #F3F4F6;
            padding: 10px 14px;
            border-radius: 8px;
            border: 1px solid #E5E7EB;
            color: #374151;
            font-size: 14px;
            min-height: 38px;
            display: flex;
            align-items: center;
        ">{teoa_leader_display}</div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Section 2: Problem & Benefits
    st.markdown(
        """
    <div class="form-section">
        <div class="section-title">
            <span class="number">2</span>
            Problem & Benefits
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    problem_statements = st.text_area(
        "Problem Statements",
        placeholder="What specific problem does this idea address? Describe the current state and pain points.",
        height=100,
        value=st.session_state.idea_form["problem_statements"],
        key="problem_input",
    )

    benefits = st.text_area(
        "Expected Benefits",
        placeholder="How will this idea benefit the organization? (e.g., cost savings, efficiency, customer satisfaction)",
        height=100,
        value=st.session_state.idea_form["benefits"],
        key="benefits_input",
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Toggle Section
    is_implemented = st.checkbox(
        "Is this already implemented?",
        value=st.session_state.idea_form["is_implemented"],
        key="checkbox_is_implemented",
    )

    st.session_state.idea_form["is_implemented"] = is_implemented

    # Implementation Details (conditional)
    if is_implemented:
        st.markdown(
            """
        <div class="implementation-card">
            <div class="section-title">
                <span class="number">3</span>
                Implementation Details
            </div>
        """,
            unsafe_allow_html=True,
        )

        # Row 1: Solution + Date Implemented
        col1, col2 = st.columns(2)
        with col1:
            solution_implemented = st.text_area(
                "Solution Implemented",
                placeholder="Explain what solution was implemented",
                height=80,
                value=st.session_state.idea_form.get("solution_implemented", ""),
                key="solution_implemented_input",
            )
        with col2:
            date_implemented = st.date_input(
                "Date Implemented",
                value=st.session_state.idea_form.get("date_implemented")
                if st.session_state.idea_form.get("date_implemented")
                else None,
                key="date_implemented_input",
            )

        # Row 2: Effective Date + Impact Group
        col1, col2 = st.columns(2)
        with col1:
            effective_date = st.date_input(
                "Effective Date",
                value=st.session_state.idea_form["effective_date"]
                if st.session_state.idea_form["effective_date"]
                else None,
                key="effective_date_input",
            )
        with col2:
            impact_group = st.selectbox(
                "Impact Group",
                IMPACT_GROUP_OPTIONS,
                index=None,
                placeholder="Select",
                key="impact_select",
            )

        st.markdown(
            '<div class="subsection-title">Capacity Impact</div>',
            unsafe_allow_html=True,
        )

        # Row 3: Drivers for Capacity Creation
        drivers = st.multiselect(
            "Drivers for Capacity Creation",
            DRIVERS_OPTIONS,
            default=st.session_state.idea_form["drivers"],
            key="drivers_multiselect",
        )

        # If "Other - specify in open box" is selected, show text input
        drivers_other = ""
        if "Other - specify in open box" in drivers:
            drivers_other = st.text_input(
                "Please specify",
                placeholder="Please specify...",
                value=st.session_state.idea_form.get("drivers_other", ""),
                key="drivers_other_input",
            )

        # Row 4: Hours Saved + Planned Use
        col1, col2 = st.columns(2)
        with col1:
            hours_saved = st.number_input(
                "Projected Hours Saved Annually",
                min_value=0,
                step=1,
                value=st.session_state.idea_form["hours_saved"],
                key="hours_input",
            )
        with col2:
            planned_use = st.text_area(
                "Planned Use for Capacity Created",
                placeholder="How will the created capacity be used?",
                height=80,
                value=st.session_state.idea_form["planned_use"],
                key="planned_use_input",
            )

        st.markdown(
            '<div class="subsection-title">Attachments</div>', unsafe_allow_html=True
        )

        # Row 4: Capacity Calculation Files with SharePoint link
        st.markdown("**📎 Capacity Calculation File(s)**")
        st.markdown(
            "[📋 TEOA Capacity Calculation Template](https://te360.sharepoint.com/:x:/s/TEOAStandardDocumentation/IQCCGJzTZT9kQLvz0x0sRTReAf7WF6E7ThK_o_vWnUgIRFg?e=LOBGo7)"
        )
        capacity_files = st.file_uploader(
            "Upload capacity files",
            type=None,
            accept_multiple_files=True,
            key="capacity_file_input",
        )

        # Before and After Implementation Attachments
        st.markdown("---")
        st.markdown("**📎 Implementation Attachments**")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Before Implementation Attachments**")
            before_implementation_files = st.file_uploader(
                "Upload files (optional)",
                type=None,
                accept_multiple_files=True,
                key="before_implementation_input",
            )
        with col2:
            st.markdown("**After Implementation Attachments**")
            after_implementation_files = st.file_uploader(
                "Upload files (optional)",
                type=None,
                accept_multiple_files=True,
                key="after_implementation_input",
            )

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        effective_date = None
        impact_group = None
        drivers = []
        drivers_other = ""
        hours_saved = 0
        planned_use = None
        capacity_files = None
        before_implementation_files = None
        after_implementation_files = None
        solution_implemented = ""
        date_implemented = None

    # Submit Button
    st.markdown('<div class="submit-container">', unsafe_allow_html=True)
    submitted = st.button("Submit Idea", type="primary", use_container_width=False)
    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        errors = []

        if not title:
            errors.append("Project Title")
        if not proposed_change:
            errors.append("Proposed Change")
        if not problem_statements:
            errors.append("Problem Statements")
        if not benefits:
            errors.append("Expected Benefits")
        if not region:
            errors.append("Region")
        if not bu_cl_site:
            errors.append("BU/CL Site")
        if is_implemented and not impact_group:
            errors.append("Impact Group")

        if errors:
            st.error(f"Please fill in: {', '.join(errors)}")
        else:
            effective_date_str = effective_date.isoformat() if effective_date else None
            date_implemented_str = (
                date_implemented.isoformat() if date_implemented else None
            )

            final_drivers = drivers.copy()
            if "Other" in drivers and drivers_other:
                final_drivers.remove("Other")
                final_drivers.append(f"Other: {drivers_other}")

            # Get the site leader and teoa leader values (use session state as fallback)
            final_site_leader = (
                site_leader
                if site_leader
                else st.session_state.idea_form.get("site_leader", "")
            )
            final_teoa_leader = (
                teoa_leader
                if teoa_leader
                else st.session_state.idea_form.get("teoa_leader", "")
            )

            add_idea(
                title=title,
                proposed_change=proposed_change,
                project_lead=project_lead,
                region=region,
                bu_cl_site=bu_cl_site,
                problem_statements=problem_statements,
                benefits=benefits,
                is_implemented="Yes" if is_implemented else "No",
                effective_date=effective_date_str,
                drivers=final_drivers,
                impact_group=impact_group if is_implemented else None,
                hours_saved=hours_saved if is_implemented else None,
                capacity_files=capacity_files if is_implemented else None,
                planned_use=planned_use if is_implemented else None,
                before_implementation_files=before_implementation_files
                if is_implemented
                else None,
                after_implementation_files=after_implementation_files
                if is_implemented
                else None,
                submitted_by=st.session_state.user_id,
                site_leader=final_site_leader,
                teoa_leader=final_teoa_leader,
                solution_implemented=solution_implemented if is_implemented else None,
                date_implemented=date_implemented_str if is_implemented else None,
            )

            # Send notification
            user_name = st.session_state.get("full_name") or st.session_state.get(
                "username", "Unknown"
            )

            site_leaders_list = site_leader.split(", ") if site_leader else []
            teoa_leaders_list = teoa_leader.split(", ") if teoa_leader else []

            notification_data = {
                "title": title,
                "proposed_change": proposed_change,
                "region": region,
                "bu_cl_site": bu_cl_site,
                "project_lead": project_lead,
                "submitted_by_name": user_name,
                "emails": assignment_emails,
            }

            # Send notification (wrap in try-except to not block success message)
            try:
                send_idea_submission_notification(
                    notification_data,
                    site_leaders_list,
                    teoa_leaders_list,
                    is_implemented,
                )
            except Exception as e:
                st.error(f"Email notification failed: {e}")

            # Set success message based on implementation status
            if is_implemented:
                success_message = "Thanks! Your implemented improvement has been submitted. We greatly appreciate your commitment to improvement - it means a lot!"
            else:
                success_message = "Thanks! Your idea is logged. Your idea has been submitted to your TEOA site leader and your manager. Please check back and update your status when the idea is implemented."

            # Clear all form fields before showing popup
            clear_all_form_fields()

            # Store message and show popup
            st.session_state.success_message = success_message
            st.session_state.show_success_popup = True

            st.rerun()

    # Update session state
    st.session_state.idea_form["title"] = title if "title" in locals() else ""
    st.session_state.idea_form["proposed_change"] = (
        proposed_change if "proposed_change" in locals() else ""
    )
    st.session_state.idea_form["project_lead"] = (
        project_lead if "project_lead" in locals() else ""
    )
    st.session_state.idea_form["region"] = region if "region" in locals() else ""
    st.session_state.idea_form["bu_cl_site"] = (
        bu_cl_site if "bu_cl_site" in locals() else ""
    )
    st.session_state.idea_form["problem_statements"] = (
        problem_statements if "problem_statements" in locals() else ""
    )
    st.session_state.idea_form["benefits"] = benefits if "benefits" in locals() else ""
    st.session_state.idea_form["is_implemented"] = is_implemented
    st.session_state.idea_form["effective_date"] = (
        effective_date if "effective_date" in locals() and effective_date else None
    )
    st.session_state.idea_form["impact_group"] = (
        impact_group if "impact_group" in locals() else ""
    )
    st.session_state.idea_form["drivers"] = drivers if "drivers" in locals() else []
    st.session_state.idea_form["drivers_other"] = (
        drivers_other if "drivers_other" in locals() else ""
    )
    st.session_state.idea_form["hours_saved"] = (
        hours_saved if "hours_saved" in locals() else 0
    )
    st.session_state.idea_form["planned_use"] = (
        planned_use if "planned_use" in locals() else ""
    )
    st.session_state.idea_form["site_leader"] = (
        site_leader if "site_leader" in locals() else ""
    )
    st.session_state.idea_form["teoa_leader"] = (
        teoa_leader if "teoa_leader" in locals() else ""
    )
    st.session_state.idea_form["solution_implemented"] = (
        solution_implemented if "solution_implemented" in locals() else ""
    )
    st.session_state.idea_form["date_implemented"] = (
        date_implemented
        if "date_implemented" in locals() and date_implemented
        else None
    )
