import streamlit as st

def render():
    st.title("About Procurement Idea Hub")
    
    st.info("The TEOA team is reviewing every submitted idea weekly. We encourage everyone to submit their ideas!")
    
    st.header("Welcome to the Procurement Idea Hub")
    
    st.markdown("""
    The TEOA (Total Equipment and Operational Advantage) IdeaHub is a platform designed to capture 
    and cultivate innovative ideas from every team member. We believe that great ideas can come from 
    anywhere — and we want to hear yours!
    """)
    
    st.header("What is an Improvement Idea?")
    
    st.markdown("""
    An improvement idea is a **specific, actionable proposal** to eliminate waste, reduce variation, 
    improve flow, or enhance value delivery to the customer by changing a process, method, tool, or system.
    """)
    
    st.markdown("""
    An improvement idea could result in a **Kaizen Event** or **Transformation project** – 
    but it should NOT be limited to such "big" ideas only. Everybody in the Organization also needs to focus on 
    improvement ideas, which are **small and simple** – ideas to improve everyday operational excellence.
    """)
    
    st.markdown("""
    Every employee is encouraged to focus on **quick wins** — ideas that can be implemented easily 
    without major resources or long projects. This empowers every employee to contribute to continuous improvement 
    in their daily work.
    """)
    
    st.header("Example of an Improvement Idea")
    
    with st.expander("View Example"):
        st.markdown("**Specific observation:**")
        st.markdown('"Step 3 in the approval process requires manual data entry that duplicates information from Step 1, causing 2 hours of delay per request"')
        
        st.markdown("**Root cause:**")
        st.markdown('"Because systems don\'t communicate automatically"')
        
        st.markdown("**Proposed solution:**")
        st.markdown('"Integrate the two systems to auto-populate fields, eliminating redundant entry"')
        
        st.markdown("**Expected impact:**")
        st.markdown('"Reduce cycle time by 2 hours, eliminate transcription errors, free up 10 staff hours per week"')
    
    st.header("Characteristics of an Improvement Idea")
    
    st.subheader("1. Problem or Opportunity Identification")
    st.markdown("""
    - Clearly identifies what is wrong or what could be better
    - Based on observation of actual work (Gemba)
    - Addresses a gap between current state and desired state
    """)
    
    st.subheader("2. Root Cause Understanding")
    st.markdown("""
    - Goes beyond symptoms to identify underlying causes
    - Often uses tools like 5 Whys, Fishbone diagrams
    - Demonstrates understanding of why the problem exists
    """)
    
    st.subheader("3. Proposed Countermeasure/Solution")
    st.markdown("""
    - Specific action or change to address the root cause
    - Describes HOW the improvement will be implemented
    - Includes what will change in the current process
    """)
    
    st.subheader("4. Expected Impact")
    st.markdown("""
    - Quantifiable or observable benefits
    - Connection to lean objectives: waste reduction, quality improvement, cycle time reduction, safety enhancement, cost reduction
    - Addresses one or more of the 8 Wastes (TIMWOODS): Transport, Inventory, Motion, Waiting, Overproduction, Overprocessing, Defects, Skills
    """)
    
    st.subheader("5. Feasibility")
    st.markdown("""
    - Can be implemented with available resources
    - Considers scope and scale appropriate to the suggester's level
    - Has clear ownership and timeline
    """)
    
    st.header("How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 1. Submit Your Idea")
        st.markdown("Fill out the form with your improvement proposal")
    
    with col2:
        st.markdown("### 2. Weekly Review")
        st.markdown("TEOA team reviews all submissions weekly")
    
    with col3:
        st.markdown("### 3. Implementation")
        st.markdown("Viable ideas are implemented and tracked")
    
    st.markdown("---")
    
    st.caption("© 2026 Procurement Idea Hub. All rights reserved. Built with love for continuous improvement.")
