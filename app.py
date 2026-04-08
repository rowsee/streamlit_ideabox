import streamlit as st
from database import (
    init_db,
    get_user_by_email,
    create_user,
    force_schema_update,
    get_all_user_emails,
)
from utils import validate_email_complete, normalize_email
import pages.home as home
import pages.submit_idea as submit_idea
import pages.browse_ideas as browse_ideas
import pages.my_ideas as my_ideas
import pages.about as about
import pages.dashboard as dashboard

st.set_page_config(
    page_title="Procurement Idea Hub",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)

# Modern color palette CSS
st.markdown(
    """
<style>
    /* ===== COLOR PALETTE ===== */
    :root {
        --primary: #6366f1;
        --primary-light: #818cf8;
        --primary-dark: #4f46e5;
        --secondary: #8b5cf6;
        --accent: #f97316;
        --accent-light: #fb923c;
        --bg-main: #f8fafc;
        --bg-surface: #ffffff;
        --bg-sidebar: #f1f5f9;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --text-muted: #94a3b8;
        --border: #e2e8f0;
        --border-light: #f1f5f9;
        --success: #10b981;
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
        --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
        --shadow-lg: 0 8px 24px rgba(0,0,0,0.12);
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
    }

    /* Hide dark mode toggle */
    [data-testid="stThemeSelector"] { display: none !important; }

    /* Main Background */
    .stApp { background: var(--bg-main) !important; }
    
    /* Text Styling */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }
    
    p, span, div, label { color: var(--text-secondary) !important; }

    /* ===== SIDEBAR - PURPLE BACKGROUND ===== */
    section[data-testid="stSidebar"] {
        background: #6366f1 !important;
        border-right: none !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* Hide default Streamlit sidebar navigation */
    [data-testid="stSidebarNavItems"],
    .st-emotion-cache-1gczx66,
    ul[data-testid="stSidebarNavItems"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Navigation Buttons */
    .nav-button {
        width: 100%;
        padding: 12px 16px;
        margin: 2px 8px;
        border: none;
        border-radius: var(--radius-sm);
        background: transparent;
        color: #FFFFFF !important;
        font-size: 14px;
        font-weight: 500;
        text-align: left;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .nav-button:hover {
        background: rgba(255,255,255,0.15) !important;
    }
    
    .nav-button.active {
        background: rgba(255,255,255,0.25) !important;
        border-left: 3px solid #FFFFFF;
    }

    /* Sidebar branding */
    .sidebar-brand {
        text-align: center;
        padding: 24px 16px;
        border-bottom: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 8px;
    }
    
    .sidebar-brand .logo {
        font-size: 32px;
        margin-bottom: 8px;
    }
    
    .sidebar-brand .brand-name {
        font-size: 16px;
        font-weight: 700;
        color: #FFFFFF !important;
    }
    
    .sidebar-brand .brand-tagline {
        font-size: 11px;
        color: rgba(255,255,255,0.7) !important;
        margin-top: 2px;
    }

    /* Sidebar user welcome */
    .sidebar-welcome {
        background: rgba(255,255,255,0.15);
        border-radius: var(--radius-md);
        padding: 16px;
        margin: 12px 16px;
        text-align: center;
    }
    
    .sidebar-welcome .greeting {
        font-size: 11px;
        color: rgba(255,255,255,0.7) !important;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .sidebar-welcome .user-name {
        font-size: 14px;
        color: #FFFFFF !important;
        margin-top: 4px;
        font-weight: 600;
    }

    /* Navigation Buttons */
    .nav-button {
        width: 100%;
        padding: 12px 16px;
        margin: 2px 8px;
        border: none;
        border-radius: var(--radius-sm);
        background: transparent;
        color: rgba(255,255,255,0.85) !important;
        font-size: 14px;
        font-weight: 500;
        text-align: left;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .nav-button:hover {
        background: rgba(255,255,255,0.15) !important;
        color: #FFFFFF !important;
    }
    
    .nav-button.active {
        background: rgba(255,255,255,0.25) !important;
        color: #FFFFFF !important;
        border-left: 3px solid #FFFFFF;
    }
    
    .nav-button.active:hover {
        background: rgba(255,255,255,0.3) !important;
    }

    /* Logout button */
    .logout-btn {
        margin: 8px 16px;
        padding: 10px 16px;
        border-radius: var(--radius-sm);
        border: 1px solid rgba(255,255,255,0.3);
        background: transparent;
        color: rgba(255,255,255,0.85) !important;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .logout-btn:hover {
        background: rgba(255,255,255,0.15) !important;
        color: #FFFFFF !important;
    }
        padding: 12px 16px;
        margin: 2px 8px;
        border: none;
        border-radius: var(--radius-sm);
        background: transparent;
        color: var(--text-secondary) !important;
        font-size: 14px;
        font-weight: 500;
        text-align: left;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .nav-button:hover {
        background: var(--bg-surface) !important;
        color: var(--text-primary) !important;
    }
    
    .nav-button.active {
        background: var(--primary) !important;
        color: white !important;
    }
    
    .nav-button.active:hover {
        background: var(--primary-dark) !important;
    }

    /* Logout button */
    .logout-btn {
        margin: 8px 16px;
        padding: 10px 16px;
        border-radius: var(--radius-sm);
        border: 1px solid var(--border);
        background: transparent;
        color: var(--text-secondary) !important;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .logout-btn:hover {
        background: #fee2e2 !important;
        color: #dc2626 !important;
        border-color: #fecaca !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Additional modern styles
st.markdown(
    """
<style>
    /* ===== GLOBAL BUTTONS ===== */
    .stButton > button {
        background: var(--primary) !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        color: white !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: var(--primary-dark) !important;
        transform: translateY(-1px);
        color: white !important;
    }

    /* Active/pressed state */
    .stButton > button:active {
        background: #4338ca !important;
        transform: translateY(0);
        color: white !important;
    }

    /* Disabled state */
    .stButton > button:disabled {
        background: #94a3b8 !important;
        color: white !important;
        opacity: 0.8;
        cursor: not-allowed;
    }

    /* Icons inside buttons - white */
    .stButton > button svg,
    .stButton > button span,
    .stButton > button p {
        color: white !important;
    }

    /* ===== FORM INPUTS ===== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        padding: 10px 12px !important;
        font-size: 14px !important;
        white-space: normal !important;
        overflow-wrap: break-word !important;
    }
    
    .stTextInput > div > div > input {
        min-height: 44px !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: var(--text-muted) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
        outline: none !important;
    }

    /* ===== SELECTBOX ===== */
    .stSelectbox > div > div > div {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        padding: 10px 12px !important;
        font-size: 14px !important;
        min-height: 44px !important;
    }

    /* ===== MULTISELECT ===== */
    .stMultiSelect > div > div > div {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        padding: 12px !important;
    }

    /* ===== DATE INPUT ===== */
    .stDateInput > div > div > div {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
    }

    /* ===== METRICS ===== */
    div[data-testid="stMetric"] {
        background: var(--bg-surface);
        border-radius: var(--radius-md);
        padding: 20px !important;
        border: 1px solid var(--border);
        box-shadow: var(--shadow-sm);
    }

    /* ===== SUCCESS/ERROR/INFO MESSAGES ===== */
    .stSuccess {
        background: #ecfdf5 !important;
        color: #065f46 !important;
        border: 1px solid #a7f3d0 !important;
        border-radius: var(--radius-sm) !important;
    }
    
    .stError {
        background: #fef2f2 !important;
        color: #991b1b !important;
        border: 1px solid #fecaca !important;
        border-radius: var(--radius-sm) !important;
    }
    
    .stInfo {
        background: #eff6ff !important;
        color: #1e40af !important;
        border: 1px solid #bfdbfe !important;
        border-radius: var(--radius-sm) !important;
    }

    /* ===== EXPANDER/CARD ===== */
    .stExpander {
        background: var(--bg-surface) !important;
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--border) !important;
        box-shadow: var(--shadow-sm) !important;
    }

    /* ===== DOWNLOAD BUTTON ===== */
    .stDownloadButton > button {
        background: var(--bg-surface) !important;
        color: var(--text-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
    }
    
    .stDownloadButton > button:hover {
        background: var(--border-light) !important;
    }

    /* ===== FORM SUBMIT BUTTON ===== */
    button[kind="primary"] {
        padding: 12px 24px !important;
        border-radius: var(--radius-sm) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


def init_session():
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "email" not in st.session_state:
        st.session_state.email = ""
    if "full_name" not in st.session_state:
        st.session_state.full_name = ""
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"


def login_user():
    # Hide sidebar on login page
    st.markdown(
        """
    <style>
        section[data-testid="stSidebar"] { display: none !important; }
        .block-container { max-width: 480px !important; margin: 0 auto; padding-top: 60px !important; }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Login page header with fixed title (no wrapping)
    st.markdown(
        """
    <div style="text-align: center; margin-bottom: 40px;">
        <div style="font-size: 56px; margin-bottom: 16px;">💡</div>
        <h1 style="color: #1e293b; margin-bottom: 8px; font-weight: 700; font-size: 26px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">TEOA Procurement Idea Hub</h1>
        <p style="color: #64748b; font-size: 16px;">Sign in with your TE email to continue</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Initialize confirmation state if not exists
    if "confirm_account_creation" not in st.session_state:
        st.session_state.confirm_account_creation = False
    if "pending_email" not in st.session_state:
        st.session_state.pending_email = None
    if "pending_full_name" not in st.session_state:
        st.session_state.pending_full_name = None

    # Show confirmation dialog if needed
    if st.session_state.confirm_account_creation and st.session_state.pending_email:
        st.warning("⚠️ New Account Creation")
        st.info(f"Creating account for: **{st.session_state.pending_email}**")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✓ Create Account", type="primary", use_container_width=True):
                # Create the account
                username = st.session_state.pending_email.split("@")[0]
                user_id = create_user(
                    username,
                    st.session_state.pending_email,
                    st.session_state.pending_full_name or "",
                )
                st.session_state.user_id = user_id
                st.session_state.username = username
                st.session_state.email = st.session_state.pending_email
                st.session_state.full_name = st.session_state.pending_full_name or ""

                # Clear pending state
                st.session_state.confirm_account_creation = False
                st.session_state.pending_email = None
                st.session_state.pending_full_name = None

                st.session_state.current_page = "home"
                st.rerun()

        with col2:
            if st.button("✗ Cancel", use_container_width=True):
                # Clear pending state
                st.session_state.confirm_account_creation = False
                st.session_state.pending_email = None
                st.session_state.pending_full_name = None
                st.rerun()

        return

    with st.form("login_form"):
        email = st.text_input(
            "TE Email",
            placeholder="your.name@te.com",
            label_visibility="visible",
        )
        full_name = st.text_input(
            "Your Name",
            placeholder="Enter your name",
            label_visibility="visible",
        )
        submitted = st.form_submit_button("Continue →", use_container_width=True)

        if submitted and email:
            # Normalize email
            email = normalize_email(email)

            # Get existing emails for similarity checking
            existing_emails = get_all_user_emails()

            # Validate email
            is_valid, error_message, suggestion = validate_email_complete(
                email, existing_emails
            )

            if not is_valid:
                if suggestion:
                    # Show error with suggestion
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.error(f"{error_message}")
                    with col2:
                        if st.button(f"Use {suggestion}", type="primary"):
                            # Update the email input with suggestion
                            st.session_state.suggested_email = suggestion
                            st.rerun()
                else:
                    st.error(f"🔒 {error_message}")
            else:
                # Email is valid, check if user exists
                user = get_user_by_email(email)
                if user:
                    # Existing user - log in
                    st.session_state.user_id = user["id"]
                    st.session_state.username = user["username"]
                    st.session_state.email = user["email"]
                    st.session_state.full_name = user["full_name"] or ""
                    st.session_state.current_page = "home"
                    st.rerun()
                else:
                    # New user - show confirmation
                    st.session_state.confirm_account_creation = True
                    st.session_state.pending_email = email
                    st.session_state.pending_full_name = full_name
                    st.rerun()


def render_sidebar():
    with st.sidebar:
        # Branding
        st.markdown(
            """
        <div class="sidebar-brand">
            <div class="logo">💡</div>
            <div class="brand-name">TEOA Procurement</div>
            <div class="brand-tagline">Idea Hub</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.session_state.user_id:
            # Welcome message
            st.markdown(
                f"""
            <div class="sidebar-welcome">
                <p class="greeting">Welcome back</p>
                <p class="user-name">{st.session_state.full_name or st.session_state.username}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Navigation buttons with icons
            nav_items = [
                ("Home", "🏠", "home"),
                ("Submit Idea", "✏️", "submit_idea"),
                ("My Ideas", "📁", "my_ideas"),
                ("Browse Ideas", "🔍", "browse_ideas"),
                ("Dashboard", "📊", "dashboard"),
                ("About", "ℹ️", "about"),
            ]

            for label, icon, page_key in nav_items:
                is_active = st.session_state.current_page == page_key
                btn_class = "nav-button active" if is_active else "nav-button"

                if st.button(
                    f"{icon}  {label}", key=f"nav_{page_key}", use_container_width=True
                ):
                    st.session_state.current_page = page_key
                    st.rerun()

            st.markdown(
                "<div style='margin-top: auto; padding-top: 20px;'>",
                unsafe_allow_html=True,
            )

            # Logout button
            if st.button("🚪  Sign out", key="logout_btn", use_container_width=True):
                st.session_state.user_id = None
                st.session_state.username = ""
                st.session_state.email = ""
                st.session_state.full_name = ""
                st.session_state.current_page = "Home"
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

        return None


def main():
    force_schema_update()
    init_db()
    init_session()

    # Only render sidebar when user is logged in
    if st.session_state.user_id:
        render_sidebar()

    if not st.session_state.user_id:
        login_user()
    else:
        current = st.session_state.current_page
        if current == "home":
            home.render()
        elif current == "submit_idea":
            submit_idea.render()
        elif current == "my_ideas":
            my_ideas.render()
        elif current == "browse_ideas":
            browse_ideas.render()
        elif current == "dashboard":
            dashboard.render()
        elif current == "about":
            about.render()


if __name__ == "__main__":
    main()
