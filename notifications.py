import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587
SMTP_USERNAME = "noreply@te.com"
SMTP_PASSWORD = "your-password-here"
FROM_EMAIL = "noreply@te.com"

def send_notification(recipients, subject, body):
    """
    Send email notification to recipients.
    
    Args:
        recipients: list of email addresses
        subject: email subject
        body: email body (HTML or plain text)
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not recipients:
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = FROM_EMAIL
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = subject
        
        part1 = MIMEText(body, 'plain')
        part2 = MIMEText(body, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, recipients, msg.as_string())
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email send error: {e}")
        return False

def send_idea_submission_notification(idea_data, site_leaders, teoa_leaders, is_implemented):
    """
    Send notification when a new idea is submitted.
    
    Args:
        idea_data: dict containing idea information
        site_leaders: list of site leader names
        teoa_leaders: list of TEOA leader names
        is_implemented: bool indicating if the idea is already implemented
    """
    all_emails = []
    
    for entry in idea_data.get('emails', []):
        if entry and entry not in all_emails:
            all_emails.append(entry)
    
    if not all_emails:
        return False
    
    if is_implemented:
        subject = f"New Implemented Improvement Submitted: {idea_data['title']}"
        body = f"""
Dear Team,

A new implemented improvement has been submitted:

Title: {idea_data['title']}
Description: {idea_data['description']}
Region: {idea_data['region']}
BU/CL Site: {idea_data['bu_cl_site']}
Project Lead: {idea_data['project_lead']}
Submitted By: {idea_data['submitted_by_name']}

We greatly appreciate the commitment to improvement - it means a lot!

Best regards,
Procurement Idea Hub
"""
    else:
        site_leaders_str = ", ".join(site_leaders) if site_leaders else "TBD"
        teoa_leaders_str = ", ".join(teoa_leaders) if teoa_leaders else "TBD"
        
        subject = f"New Idea Submitted: {idea_data['title']}"
        body = f"""
Dear Site Leader and Manager,

A new idea has been submitted and requires your attention:

Title: {idea_data['title']}
Description: {idea_data['description']}
Region: {idea_data['region']}
BU/CL Site: {idea_data['bu_cl_site']}
Project Lead: {idea_data['project_lead']}
Submitted By: {idea_data['submitted_by_name']}

Site Leader: {site_leaders_str}
TEOA Functional Leader: {teoa_leaders_str}

Please review and follow up with the submitter.

Best regards,
Procurement Idea Hub
"""
    
    return send_notification(all_emails, subject, body)
