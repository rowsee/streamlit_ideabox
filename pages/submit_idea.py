import streamlit as st
from database import add_idea

st.markdown("""
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
        background: #FF6B35;
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
    
    /* Guidelines section */
    .guidelines-section {
        background: #F9FAFB;
        border-radius: 12px;
        padding: 24px;
        margin-top: 32px;
    }
    
    .guidelines-section h3 {
        font-size: 16px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 16px;
    }
    
    .guideline-item {
        display: flex;
        gap: 12px;
        margin-bottom: 12px;
    }
    
    .guideline-item .num {
        background: #FF6B35;
        color: white;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 600;
        flex-shrink: 0;
    }
    
    .guideline-item p {
        font-size: 13px;
        color: #4B5563;
        margin: 0;
        line-height: 1.5;
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
</style>
""", unsafe_allow_html=True)

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

DRIVERS_OPTIONS = [
    "Automation of Process",
    "Use of AI tool",
    "Automation of Reports",
    "Creation of Standard Process, templates or any other resources",
    "Elimination of Rework loop",
    "Reduction of Steps in Process",
    "Empower team on self-service tools",
    "Other"
]

IMPACT_GROUP_OPTIONS = ["", "Within the site", "Cross Function", "Both"]

PROJECT_TYPE_OPTIONS = ["", "Low", "Medium", "High"]

def render():
    # Page header
    st.markdown("""
    <div class="page-header">
        <h1>💡 Submit Your Idea</h1>
        <p>Share your innovative ideas to help improve our organization.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for form values
    if "idea_form" not in st.session_state:
        st.session_state.idea_form = {
            "title": "",
            "description": "",
            "project_lead": "",
            "region": "",
            "bu_cl_site": "",
            "project_type": "",
            "problem_statements": "",
            "benefits": "",
            "is_implemented": False,
            "effective_date": None,
            "impact_group": "",
            "drivers": [],
            "drivers_other": "",
            "hours_saved": 0,
            "planned_use": "",
        }
    
    # Section 1: Basic Information
    st.markdown("""
    <div class="form-section">
        <div class="section-title">
            <span class="number">1</span>
            Project Details
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Row 1: Title + Project Type
    col1, col2 = st.columns([2, 1])
    with col1:
        title = st.text_input(
            "Project Title", 
            placeholder="Enter a clear, descriptive title",
            value=st.session_state.idea_form["title"],
            key="title_input"
        )
    with col2:
        project_type = st.selectbox(
            "Project Type", 
            PROJECT_TYPE_OPTIONS,
            index=None,
            placeholder="Select",
            key="project_type_select"
        )
    
    # Row 2: Description
    description = st.text_area(
        "Project Description",
        placeholder="Describe your idea in detail. What is the problem? What is your solution?",
        height=120,
        value=st.session_state.idea_form["description"],
        key="desc_input"
    )
    
    # Row 3: Project Lead + Region
    col1, col2 = st.columns(2)
    with col1:
        project_lead = st.text_input(
            "Project Lead", 
            placeholder="Name of person responsible",
            value=st.session_state.idea_form["project_lead"],
            key="lead_input"
        )
    with col2:
        region = st.selectbox(
            "Region", 
            REGION_OPTIONS,
            index=None,
            placeholder="Select",
            key="region_select"
        )
    
    # Row 4: BU/CL Site
    bu_cl_site = st.selectbox(
        "BU/CL Site", 
        BU_CL_SITE_OPTIONS,
        index=None,
        placeholder="Select",
        key="site_select"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Section 2: Problem & Benefits
    st.markdown("""
    <div class="form-section">
        <div class="section-title">
            <span class="number">2</span>
            Problem & Benefits
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    problem_statements = st.text_area(
        "Problem Statements",
        placeholder="What specific problem does this idea address? Describe the current state and pain points.",
        height=100,
        value=st.session_state.idea_form["problem_statements"],
        key="problem_input"
    )
    
    benefits = st.text_area(
        "Expected Benefits",
        placeholder="How will this idea benefit the organization? (e.g., cost savings, efficiency, customer satisfaction)",
        height=100,
        value=st.session_state.idea_form["benefits"],
        key="benefits_input"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Toggle Section
    is_implemented = st.toggle(
        "Is this already implemented?", 
        value=st.session_state.idea_form["is_implemented"],
        key="toggle_is_implemented"
    )
    
    st.session_state.idea_form["is_implemented"] = is_implemented
    
    # Implementation Details (conditional)
    if is_implemented:
        st.markdown("""
        <div class="implementation-card">
            <div class="section-title">
                <span class="number">3</span>
                Implementation Details
            </div>
        """, unsafe_allow_html=True)
        
        # Row 1: Effective Date + Impact Group
        col1, col2 = st.columns(2)
        with col1:
            effective_date = st.date_input(
                "Effective Date",
                value=st.session_state.idea_form["effective_date"] if st.session_state.idea_form["effective_date"] else None,
                key="effective_date_input"
            )
        with col2:
            impact_group = st.selectbox(
                "Impact Group", 
                IMPACT_GROUP_OPTIONS,
                index=None,
                placeholder="Select",
                key="impact_select"
            )
        
        st.markdown('<div class="subsection-title">Capacity Impact</div>', unsafe_allow_html=True)
        
        # Row 2: Drivers for Capacity Creation
        drivers = st.multiselect(
            "Drivers for Capacity Creation",
            DRIVERS_OPTIONS,
            default=st.session_state.idea_form["drivers"],
            key="drivers_multiselect"
        )
        
        # If "Other" is selected, show text input
        drivers_other = ""
        if "Other" in drivers:
            drivers_other = st.text_input(
                "Other - Please Specify",
                placeholder="Please describe other driver(s)",
                value=st.session_state.idea_form.get("drivers_other", ""),
                key="drivers_other_input"
            )
        
        # Row 3: Hours Saved + Planned Use
        col1, col2 = st.columns(2)
        with col1:
            hours_saved = st.number_input(
                "Projected Hours Saved Annually",
                min_value=0,
                step=1,
                value=st.session_state.idea_form["hours_saved"],
                key="hours_input"
            )
        with col2:
            planned_use = st.text_area(
                "Planned Use for Capacity Created",
                placeholder="How will the created capacity be used?",
                height=80,
                value=st.session_state.idea_form["planned_use"],
                key="planned_use_input"
            )
        
        st.markdown('<div class="subsection-title">Attachments</div>', unsafe_allow_html=True)
        
        # Row 4: File uploads
        col1, col2 = st.columns(2)
        with col1:
            capacity_file = st.file_uploader(
                "Capacity Calculation File",
                type=["xlsx", "xls", "pdf", "doc", "docx"],
                key="capacity_file_input"
            )
        with col2:
            email_approval = st.file_uploader(
                "Email Approval Attachment",
                type=["pdf", "doc", "docx", "eml", "msg"],
                key="email_approval_input"
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        effective_date = None
        impact_group = None
        drivers = []
        drivers_other = ""
        hours_saved = 0
        planned_use = None
        capacity_file = None
        email_approval = None
    
    # Submit Button
    st.markdown('<div class="submit-container">', unsafe_allow_html=True)
    submitted = st.button("Submit Idea", type="primary", use_container_width=False)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if submitted:
        errors = []
        
        if not title:
            errors.append("Project Title")
        if not description:
            errors.append("Project Description")
        if not problem_statements:
            errors.append("Problem Statements")
        if not benefits:
            errors.append("Expected Benefits")
        if not project_type:
            errors.append("Project Type")
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
            
            final_drivers = drivers.copy()
            if "Other" in drivers and drivers_other:
                final_drivers.remove("Other")
                final_drivers.append(f"Other: {drivers_other}")
            
            add_idea(
                title=title,
                description=description,
                project_lead=project_lead,
                region=region,
                bu_cl_site=bu_cl_site,
                project_type=project_type,
                problem_statements=problem_statements,
                benefits=benefits,
                is_implemented="Yes" if is_implemented else "No",
                effective_date=effective_date_str,
                drivers=final_drivers,
                impact_group=impact_group if is_implemented else None,
                hours_saved=hours_saved if is_implemented else None,
                capacity_file=capacity_file if is_implemented else None,
                planned_use=planned_use if is_implemented else None,
                email_approval=email_approval if is_implemented else None,
                submitted_by=st.session_state.user_id
            )
            
            # Clear form after successful submission
            st.session_state.idea_form = {
                "title": "",
                "description": "",
                "project_lead": "",
                "region": "",
                "bu_cl_site": "",
                "project_type": "",
                "problem_statements": "",
                "benefits": "",
                "is_implemented": False,
                "effective_date": None,
                "impact_group": "",
                "drivers": [],
                "drivers_other": "",
                "hours_saved": 0,
                "planned_use": "",
            }
            
            st.markdown("""
            <div class="success-box">
                <span class="icon">✅</span>
                <div>
                    <strong>Success!</strong> Your idea has been submitted successfully. Thank you for contributing!
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Update session state
    st.session_state.idea_form["title"] = title if 'title' in locals() else ""
    st.session_state.idea_form["description"] = description if 'description' in locals() else ""
    st.session_state.idea_form["project_lead"] = project_lead if 'project_lead' in locals() else ""
    st.session_state.idea_form["region"] = region if 'region' in locals() else ""
    st.session_state.idea_form["bu_cl_site"] = bu_cl_site if 'bu_cl_site' in locals() else ""
    st.session_state.idea_form["project_type"] = project_type if 'project_type' in locals() else ""
    st.session_state.idea_form["problem_statements"] = problem_statements if 'problem_statements' in locals() else ""
    st.session_state.idea_form["benefits"] = benefits if 'benefits' in locals() else ""
    st.session_state.idea_form["is_implemented"] = is_implemented
    st.session_state.idea_form["effective_date"] = effective_date if 'effective_date' in locals() and effective_date else None
    st.session_state.idea_form["impact_group"] = impact_group if 'impact_group' in locals() else ""
    st.session_state.idea_form["drivers"] = drivers if 'drivers' in locals() else []
    st.session_state.idea_form["drivers_other"] = drivers_other if 'drivers_other' in locals() else ""
    st.session_state.idea_form["hours_saved"] = hours_saved if 'hours_saved' in locals() else 0
    st.session_state.idea_form["planned_use"] = planned_use if 'planned_use' in locals() else ""
    
    # Guidelines section
    st.markdown("""
    <div class="guidelines-section">
        <h3>📝 Guidelines for a Great Idea Submission</h3>
        
        <div class="guideline-item">
            <span class="num">1</span>
            <p><strong>Be Specific</strong> - Clear title that summarizes the idea, detailed description of what you're proposing, specific use cases or scenarios</p>
        </div>
        
        <div class="guideline-item">
            <span class="num">2</span>
            <p><strong>Focus on Value</strong> - Explain the problem you're solving, quantify potential benefits, consider impact on different stakeholders</p>
        </div>
        
        <div class="guideline-item">
            <span class="num">3</span>
            <p><strong>Be Practical</strong> - Consider implementation feasibility, think about resources needed, note any potential challenges</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
