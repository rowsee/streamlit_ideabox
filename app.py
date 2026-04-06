import streamlit as st
from database import init_db, get_user_by_email, create_user, force_schema_update
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

# Force light mode - hide dark mode toggle
st.markdown(
    """
<style>
    /* Hide the default theme toggle in Streamlit */
    [data-testid="stThemeSelector"] {
        display: none !important;
    }
    
    /* Force light theme colors */
    .stApp {
        background: #F9FAFB !important;
        color: #111827 !important;
    }
    
    /* Force light colors on all elements */
    html, body, div, span, p, label {
        background-color: transparent !important;
    }
    
    /* Remove dark backgrounds anywhere they might appear */
    [class*="dark"], [style*="dark"], [style*="#1E1E1E"], [style*="#262626"] {
        background: #FFFFFF !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>
    /* Modern Clean Theme - Like Stripe/Notion/Linear */
    
    /* Main Background - Very Light Gray */
    .stApp {
        background: #F9FAFB;
    }
    
    /* Text Styling */
    h1, h2, h3, h4, h5, h6 {
        color: #111827 !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }
    
    p, span, div, label {
        color: #374151 !important;
    }
    
    /* Sidebar - Soft Blue-Gray */
    section[data-testid="stSidebar"] {
        background: #1E293B !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
    
    /* Hide default navigation */
    [data-testid="stSidebarNavItems"] {
        display: none !important;
    }
    
    /* Navigation Buttons - Clean Style */
    .nav-button {
        width: 100%;
        padding: 12px 16px;
        margin: 4px 0;
        border: none;
        border-radius: 8px;
        background: transparent;
        color: #94A3B8 !important;
        font-size: 13px;
        font-weight: 500;
        text-align: left;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .nav-button:hover {
        background: rgba(255, 255, 255, 0.08);
        color: #F1F5F9 !important;
    }
    
    .nav-button.active {
        background: #FF6B35;
        color: white !important;
    }
    
    .nav-button span {
        font-size: 16px;
    }
    
    /* Sidebar Branding */
    .sidebar-brand {
        text-align: center;
        padding: 24px 0 32px 0;
    }
    
    .sidebar-brand .logo {
        font-size: 40px;
        margin-bottom: 8px;
    }
    
    .sidebar-brand .brand-name {
        font-size: 18px;
        font-weight: 600;
        color: #F1F5F9 !important;
        margin: 0;
    }
    
    .sidebar-brand .brand-tagline {
        font-size: 11px;
        color: #64748B !important;
        margin: 4px 0 0 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Welcome Message */
    .welcome-msg {
        background: rgba(255, 107, 53, 0.1);
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        margin-bottom: 24px;
    }
    
    .welcome-msg .greeting {
        font-size: 11px;
        color: #FF6B35 !important;
        margin: 0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .welcome-msg .user-name {
        font-size: 13px;
        color: #F1F5F9 !important;
        margin: 6px 0 0 0;
        font-weight: 500;
    }
    
    /* Modern Buttons - Clean Orange */
    .stButton > button {
        background: #FF6B35 !important;
        border: none !important;
        border-radius: 8px !important;
        color: white !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #E55A2B !important;
    }
    
    /* 1. Form Inputs - Clean White Style (Like Notion/Linear) */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        color: #111827 !important;
        padding: 11px !important;
        font-size: 13px !important;
        box-shadow: none !important;
    }
    
    .stTextInput > div > div,
    .stTextArea > div > div {
        background: #FFFFFF !important;
    }
    
    .stTextInput > div,
    .stTextArea > div {
        background: #FFFFFF !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #9CA3AF !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #FF6A3D !important;
        box-shadow: 0 0 0 3px rgba(255, 106, 61, 0.1) !important;
        outline: none !important;
    }
    
    /* Selectbox - White background with consistent font */
    .stSelectbox > div > div > div {
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        color: #111827 !important;
        padding: 11px !important;
        font-size: 13px !important;
    }
    
    .stSelectbox > div > div > div > div {
        font-size: 13px !important;
        color: #111827 !important;
    }
    
    .stSelectbox > div > div > div span {
        font-size: 13px !important;
        color: #111827 !important;
    }
    
    .stSelectbox > div > div > div > div > div {
        font-size: 13px !important;
        color: #111827 !important;
    }
    
    .stSelectbox > div > div,
    .stSelectbox > div {
        background: #FFFFFF !important;
        font-size: 13px !important;
    }
    
    .stSelectbox > div > div > div:focus-within {
        border-color: #FF6A3D !important;
    }
    
    /* Multiselect - Consistent font */
    .stMultiSelect > div > div > div {
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        padding: 11px !important;
        font-size: 13px !important;
    }
    
    .stMultiSelect > div > div > div > div {
        font-size: 13px !important;
        color: #111827 !important;
    }
    
    .stMultiSelect > div > div > div span {
        font-size: 13px !important;
    }
    
    .stMultiSelect > div > div,
    .stMultiSelect > div {
        background: #FFFFFF !important;
        font-size: 13px !important;
    }
    
    /* Date Input - Consistent font */
    .stDateInput > div > div > div {
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        font-size: 13px !important;
    }
    
    .stDateInput > div > div > div input {
        font-size: 13px !important;
        color: #111827 !important;
    }
    
    .stDateInput > div > div,
    .stDateInput > div {
        background: #FFFFFF !important;
        font-size: 13px !important;
    }
    
    /* Date picker calendar popup - White background */
    div[data-baseweb="popover"][aria-label="Select date"] {
        background: #FFFFFF !important;
    }
    
    div[data-baseweb="popover"][aria-label="Select date"] > div {
        background: #FFFFFF !important;
    }
    
    /* Calendar styling */
    div[data-baseweb="popover"] [class*="Calendar"] {
        background: #FFFFFF !important;
    }
    
    div[data-baseweb="popover"] [class*="Month"] {
        background: #FFFFFF !important;
        color: #111827 !important;
    }
    
    div[data-baseweb="popover"] [class*="Day"] {
        background: #FFFFFF !important;
        color: #111827 !important;
    }
    
    div[data-baseweb="popover"] [class*="Day"]:hover {
        background: #F3F4F6 !important;
    }
    
    div[data-baseweb="popover"] [class*="Day"][aria-selected="true"] {
        background: #FF6B35 !important;
        color: white !important;
    }
    
    /* Year/Month selectors in calendar */
    div[data-baseweb="popover"] [class*="YearMonth"] {
        background: #FFFFFF !important;
        color: #111827 !important;
    }
    
    /* Number Input - Consistent font */
    .stNumberInput > div > div > input {
        font-size: 13px !important;
        color: #111827 !important;
    }
    
    /* Dropdown menu items - Consistent font */
    [data-testid="stSelectboxPopover"] li div,
    [data-testid="stMultiSelectPopover"] li div,
    [data-testid="stDateInputPopover"] li div {
        font-size: 13px !important;
    }
    
    div[role="option"] div,
    div[role="option"] span {
        font-size: 13px !important;
    }
    
    /* Toggle Switch - Orange when ON, Grey when OFF */
    .stToggle {
        background: transparent !important;
    }
    
    .stToggle > label {
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
    }
    
    /* Toggle track - grey when OFF */
    .stToggle [data-testid="stToggleSwitch"] {
        width: 48px !important;
        height: 26px !important;
        background: #9CA3AF !important;
        border-radius: 13px !important;
        border: none !important;
        padding: 2px !important;
        flex-shrink: 0 !important;
    }
    
    /* Toggle track - orange when ON */
    .stToggle [data-testid="stToggleSwitch"][aria-checked="true"] {
        background: #FF6B35 !important;
    }
    
    /* Toggle knob */
    .stToggle [data-testid="stToggleSwitch"]::before {
        content: '' !important;
        width: 22px !important;
        height: 22px !important;
        background: white !important;
        border-radius: 50% !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
        transition: transform 0.2s ease !important;
        display: block !important;
        visibility: visible !important;
    }
    
    .stToggle [data-testid="stToggleSwitch"][aria-checked="true"]::before {
        transform: translateX(22px) !important;
    }
    
    /* Toggle label text */
    .stToggle label > div:last-child {
        font-weight: 500 !important;
        color: #111827 !important;
        font-size: 15px !important;
    }
    
    /* Multiselect - White background */
    .stMultiSelect > div > div > div {
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        padding: 11px !important;
    }
    
    .stMultiSelect > div > div,
    .stMultiSelect > div {
        background: #FFFFFF !important;
    }
    
    /* Date Input */
    .stDateInput > div > div > div {
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
    }
    
    .stDateInput > div > div,
    .stDateInput > div {
        background: #FFFFFF !important;
    }
    
    /* 2. File Uploader - Clean white drag-and-drop card */
    .stFileUploader {
        background: transparent !important;
    }
    
    .stFileUploader > div,
    .stFileUploader > div > div,
    .stFileUploader > div > div > div,
    .stFileUploader > div > section {
        background: #FFFFFF !important;
    }
    
    .stFileUploader > div > section {
        background: #FFFFFF !important;
        border: 2px dashed #D1D5DB !important;
        border-radius: 10px !important;
        padding: 32px 20px !important;
    }
    
    .stFileUploader > div > section:hover {
        border-color: #FF6A3D !important;
        background: #FFFBF9 !important;
    }
    
    /* File uploader text and icon */
    .stFileUploader p {
        color: #6B7280 !important;
    }
    
    .stFileUploader span {
        color: #9CA3AF !important;
    }
    
    /* File uploader button */
    .stFileUploader button {
        background: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 6px !important;
        color: #374151 !important;
    }
    
    .stFileUploader button:hover {
        background: #F3F4F6 !important;
        border-color: #FF6A3D !important;
    }
        background: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 6px !important;
        color: #374151 !important;
    }
    
    /* 3. Number Input - Light stepper buttons */
    .stNumberInput > div {
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
    }
    
    .stNumberInput > div > div {
        background: transparent !important;
    }
    
    .stNumberInput input {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
    }
    
    .stNumberInput button {
        background: #F9FAFB !important;
        border: none !important;
        border-left: 1px solid #E5E7EB !important;
        color: #374151 !important;
    }
    
    .stNumberInput button:hover {
        background: #F3F4F6 !important;
    }
    
    .stNumberInput button:first-child {
        border-radius: 0 !important;
    }
    
    .stNumberInput button:last-child {
        border-radius: 0 !important;
    }
    
    /* 4. Dropdown Menu - White with shadow */
    [data-testid="stSelectboxPopover"],
    [data-testid="stMultiSelectPopover"],
    [data-testid="stDateInputPopover"] {
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08) !important;
    }
    
    [data-testid="stSelectboxPopover"] div,
    [data-testid="stMultiSelectPopover"] div,
    [data-testid="stDateInputPopover"] div {
        background: #FFFFFF !important;
    }
    
    [data-testid="stSelectboxPopover"] ul,
    [data-testid="stMultiSelectPopover"] ul,
    [data-testid="stDateInputPopover"] ul {
        background: #FFFFFF !important;
        border: none !important;
    }
    
    [data-testid="stSelectboxPopover"] li,
    [data-testid="stMultiSelectPopover"] li,
    [data-testid="stDateInputPopover"] li {
        background: #FFFFFF !important;
        color: #111827 !important;
    }
    
    [data-testid="stSelectboxPopover"] li:hover,
    [data-testid="stMultiSelectPopover"] li:hover,
    [data-testid="stDateInputPopover"] li:hover {
        background: #F3F4F6 !important;
    }
    
    [data-testid="stSelectboxPopover"] li[aria-selected="true"],
    [data-testid="stMultiSelectPopover"] li[aria-selected="true"] {
        background: #FFE8E1 !important;
    }
    
    /* Dropdown/selectbox specific fixes */
    .stSelectbox div[data-baseweb="select"],
    .stMultiSelect div[data-baseweb="select"] {
        background: #FFFFFF !important;
    }
    
    /* Baseweb select dropdown menus */
    div[data-baseweb="popover"] {
        background: #FFFFFF !important;
    }
    
    div[data-baseweb="popover"] > div {
        background: #FFFFFF !important;
    }
    
    /* Menu component inside dropdowns */
    ul[aria-multiselectable="true"] {
        background: #FFFFFF !important;
    }
    
    ul[aria-multiselectable="true"] li {
        background: #FFFFFF !important;
        color: #111827 !important;
    }
    
    /* Additional selectors for popover content */
    div[role="listbox"] {
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
    }
    
    div[role="listbox"] div {
        background: #FFFFFF !important;
    }
    
    div[role="option"] {
        background: #FFFFFF !important;
        color: #111827 !important;
    }
    
    div[role="option"]:hover {
        background: #F3F4F6 !important;
    }
    
    div[role="option"][aria-selected="true"] {
        background: #FFE8E1 !important;
    }
    
    /* Force white on any nested menu items */
    * [data-baseweb="menu"] {
        background: #FFFFFF !important;
    }
    
    * [data-baseweb="menu"] li {
        background: #FFFFFF !important;
    }
    
    /* 5. Multi-select Dropdown - White with shadow */
    [data-testid="stMultiSelectPopover"] {
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08) !important;
    }
    
    [data-testid="stMultiSelectPopover"] ul {
        background: #FFFFFF !important;
        border: none !important;
    }
    
    [data-testid="stMultiSelectPopover"] li {
        background: #FFFFFF !important;
        color: #111827 !important;
        padding: 10px 12px !important;
    }
    
    [data-testid="stMultiSelectPopover"] li:hover {
        background: #F3F4F6 !important;
    }
    
    [data-testid="stMultiSelectPopover"] li[aria-selected="true"] {
        background: #FFE8E1 !important;
    }
    
    /* Checkbox in multi-select */
    [data-testid="stMultiSelectPopover"] svg {
        color: #FF6B35 !important;
    }
    
    /* 6. Section spacing - 32px between sections, 16px between fields */
    .stTextInput, .stTextArea, .stSelectbox, .stMultiSelect, .stDateInput, .stNumberInput {
        margin-bottom: 16px;
    }
    
    /* Section Dividers */
    hr {
        border: none;
        border-top: 1px solid #E5E7EB;
        margin: 32px 0;
    }
    
    /* Cards / Expanders - Clean Style */
    .stExpander {
        background: #FFFFFF !important;
        border-radius: 8px !important;
        border: 1px solid #E5E7EB !important;
        box-shadow: none !important;
    }
    
    .stExpander > div > div:first-child {
        color: #111827 !important;
        font-weight: 500 !important;
        font-size: 13px !important;
    }
    
    /* Metrics - Clean Cards */
    div[data-testid="stMetric"] {
        background: #FFFFFF !important;
        border-radius: 8px !important;
        padding: 16px !important;
        border: 1px solid #E5E7EB !important;
        box-shadow: none !important;
    }
    
    div[data-testid="stMetric"] label {
        color: #6B7280 !important;
        font-size: 12px !important;
        font-weight: 500 !important;
    }
    
    div[data-testid="stMetric"] div {
        color: #111827 !important;
        font-weight: 600 !important;
        font-size: 24px !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        padding: 8px 16px;
        color: #6B7280 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: #FF6B35 !important;
        border-bottom: 2px solid #FF6B35 !important;
    }
    
    /* DataFrame */
    .stDataFrame {
        background: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
    }
    
    /* Messages - Clean Style */
    .stSuccess {
        background: #ECFDF5 !important;
        color: #065F46 !important;
        border: 1px solid #A7F3D0 !important;
        border-radius: 6px !important;
    }
    
    .stError {
        background: #FEF2F2 !important;
        color: #991B1B !important;
        border: 1px solid #FECACA !important;
        border-radius: 6px !important;
    }
    
    .stInfo {
        background: #EFF6FF !important;
        color: #1E40AF !important;
        border: 1px solid #BFDBFE !important;
        border-radius: 6px !important;
    }
    
    .stWarning {
        background: #FFFBEB !important;
        color: #92400E !important;
        border: 1px solid #FDE68A !important;
        border-radius: 6px !important;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: #FFFFFF !important;
        color: #374151 !important;
        border: 1px solid #E5E7EB !important;
    }
    
    .stDownloadButton > button:hover {
        background: #F3F4F6 !important;
    }
    
    /* Radio buttons */
    .stRadio > div {
        gap: 8px;
    }
    
    /* Checkbox */
    .stCheckbox > label > div:first-child {
        border-color: #D1D5DB !important;
        border-radius: 4px !important;
    }
    
    /* Date Input */
    .stDateInput > div > div > div {
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
    }
    
    /* 7. Submit Button - Smaller, refined */
    button[kind="primary"] {
        padding: 12px 20px !important;
        border-radius: 8px !important;
        max-width: 300px;
        font-size: 13px !important;
    }
    
    /* Hide form submission hints */
    .stTextInput > div > div > div > span,
    .stTextArea > div > div > div > span,
    .stSelectbox > div > div > div > span,
    form > div > div > div:has(> div > small) {
        display: none !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .nav-button {
            padding: 10px 14px;
            font-size: 13px;
        }
        
        .sidebar-brand .logo {
            font-size: 32px;
        }
        
        .sidebar-brand .brand-name {
            font-size: 16px;
        }
    }
    
    /* FORCE WHITE BACKGROUNDS - Catch all remaining dark elements */
    /* Input field containers */
    .stTextInput > div,
    .stTextInput > div > div,
    .stTextArea > div,
    .stTextArea > div > div,
    .stSelectbox > div,
    .stSelectbox > div > div,
    .stMultiSelect > div,
    .stMultiSelect > div > div,
    .stNumberInput > div,
    .stDateInput > div,
    .stDateInput > div > div {
        background: #FFFFFF !important;
    }
    
    /* All input elements */
    input[type="text"],
    input[type="number"],
    input[type="email"],
    textarea,
    select {
        background: #FFFFFF !important;
        color: #111827 !important;
    }
    
    /* Placeholder text */
    input::placeholder,
    textarea::placeholder {
        color: #9CA3AF !important;
    }
    
    /* Dropdown options container */
    ul[role="listbox"],
    div[role="listbox"] {
        background: #FFFFFF !important;
    }
    
    /* All dropdown options */
    div[role="option"],
    li[role="option"] {
        background: #FFFFFF !important;
        color: #111827 !important;
    }
    
    /* Hover states for options */
    div[role="option"]:hover,
    li[role="option"]:hover {
        background: #F3F4F6 !important;
    }
    
    /* Selected state */
    div[role="option"][aria-selected="true"],
    li[role="option"][aria-selected="true"] {
        background: #FFE8E1 !important;
    }
    
    /* Baseweb select/menu components - Force white */
    [data-baseweb="select"] > div,
    [data-baseweb="menu"] > div,
    [data-baseweb="popover"] > div {
        background: #FFFFFF !important;
    }
    
    /* Override any dark backgrounds in dropdowns */
    .stSelectbox [class*="Menu"],
    .stMultiSelect [class*="Menu"] {
        background: #FFFFFF !important;
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
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            """
        <div style="text-align: center; margin-bottom: 40px;">
            <div style="font-size: 70px; margin-bottom: 20px;">💡</div>
            <h1 style="color: #1E3A5F; margin-bottom: 10px; font-weight: 800;">Procurement Idea Hub</h1>
            <p style="color: #64748B; font-size: 18px;">Share your ideas, drive excellence</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <style>
            /* Style form inputs */
            .stTextInput > div > div > input {
                background: #f8fafc !important;
                border: 2px solid #e2e8f0 !important;
                border-radius: 12px !important;
                padding: 15px !important;
                font-size: 16px !important;
                transition: all 0.3s ease;
            }
            
            .stTextInput > div > div > input:focus {
                border-color: #6366f1 !important;
                box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
            }
            
            /* Style form button */
            .stButton > button {
                background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
                border: none !important;
                border-radius: 12px !important;
                padding: 15px 30px !important;
                font-size: 16px !important;
                font-weight: 600 !important;
                transition: all 0.3s ease;
                width: 100%;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(99, 102, 241, 0.3) !important;
            }
            
            /* Reduce top padding for login page */
            .block-container {
                padding-top: 1rem !important;
                padding-bottom: 1rem !important;
            }
            
            /* Remove extra space from empty elements */
            .stMarkdown p:empty {
                display: none;
            }
        </style>
        """,
            unsafe_allow_html=True,
        )

        with st.form("login_form"):
            email = st.text_input(
                "TE Email",
                placeholder="Enter your @te.com email",
                label_visibility="visible",
            )
            full_name = st.text_input(
                "Full Name (optional)",
                placeholder="Enter your name",
                label_visibility="visible",
            )
            submitted = st.form_submit_button("Continue", use_container_width=True)

            if submitted and email:
                if not email.endswith("@te.com"):
                    st.error("Only @te.com email addresses are allowed")
                else:
                    user = get_user_by_email(email)
                    if user:
                        st.session_state.user_id = user["id"]
                        st.session_state.username = user["username"]
                        st.session_state.email = user["email"]
                        st.session_state.full_name = user["full_name"] or ""
                    else:
                        username = email.split("@")[0]
                        user_id = create_user(username, email, full_name or "")
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.session_state.email = email
                        st.session_state.full_name = full_name or ""
                    st.session_state.current_page = "home"
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
            <div class="welcome-msg">
                <p class="greeting">Welcome back!</p>
                <p class="user-name">{st.session_state.full_name or st.session_state.username}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Navigation buttons
            nav_items = [
                ("Home", "🏠", "home"),
                ("Submit Ideas", "💡", "submit_idea"),
                ("My Ideas", "👤", "my_ideas"),
                ("Browse Ideas", "📋", "browse_ideas"),
                ("Dashboard", "📊", "dashboard"),
                ("About", "ℹ️", "about"),
            ]

            for label, icon, page_key in nav_items:
                is_active = st.session_state.current_page == page_key
                btn_class = "nav-button active" if is_active else "nav-button"

                if st.button(
                    f"{icon} {label}", key=f"nav_{page_key}", use_container_width=True
                ):
                    st.session_state.current_page = page_key
                    st.rerun()

            st.markdown(
                "<div style='margin-top: auto; padding-top: 20px;'>",
                unsafe_allow_html=True,
            )

            # Logout button
            if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
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

    selected_page = render_sidebar()

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
