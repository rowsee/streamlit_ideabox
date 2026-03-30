import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587
SMTP_USERNAME = "noreply@te.com"
SMTP_PASSWORD = "TEideaboxhub2026"
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
        return False, "No recipients provided"

    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = FROM_EMAIL
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject

        part1 = MIMEText(body, "plain")
        part2 = MIMEText(body, "html")
        msg.attach(part1)
        msg.attach(part2)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, recipients, msg.as_string())
        server.quit()

        return True, "Email sent successfully"
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"SMTP Authentication Error: {e}"
        print(error_msg)
        return False, error_msg
    except smtplib.SMTPException as e:
        error_msg = f"SMTP Error: {e}"
        print(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Email send error: {e}"
        print(error_msg)
        return False, error_msg


def send_idea_submission_notification(
    idea_data, site_leaders, teoa_leaders, is_implemented
):
    """
    Send notification when a new idea is submitted.

    Args:
        idea_data: dict containing idea information
        site_leaders: list of site leader names
        teoa_leaders: list of TEOA leader names
        is_implemented: bool indicating if the idea is already implemented

    Returns:
        tuple: (success: bool, message: str)
    """
    # Get email addresses from assignment
    site_leader_emails = idea_data.get("site_leader_emails", [])
    teoa_leader_emails = idea_data.get("teoa_leader_emails", [])

    # Combine all recipient emails
    all_emails = []

    for email in site_leader_emails:
        if email and email not in all_emails:
            all_emails.append(email)

    for email in teoa_leader_emails:
        if email and email not in all_emails:
            all_emails.append(email)

    if not all_emails:
        return False, "No recipient emails found"

    # Build email content
    if is_implemented:
        subject = f"✅ New Implemented Improvement: {idea_data.get('title', 'N/A')}"
        body = f"""Dear Team,

A new implemented improvement has been submitted:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 IDEA DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Title: {idea_data.get("title", "N/A")}
Proposed Change: {idea_data.get("proposed_change", "N/A")}

Problem Statements: {idea_data.get("problem_statements", "N/A")}

Expected Benefits: {idea_data.get("benefits", "N/A")}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 LOCATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Region: {idea_data.get("region", "N/A")}
BU/CL Site: {idea_data.get("bu_cl_site", "N/A")}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 SUBMITTER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Submitted By: {idea_data.get("submitted_by_name", "N/A")}
Project Lead: {idea_data.get("project_lead", "N/A")}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

We greatly appreciate the commitment to improvement!

Best regards,
Procurement Idea Hub
"""
    else:
        site_leaders_str = ", ".join(site_leaders) if site_leaders else "TBD"
        teoa_leaders_str = ", ".join(teoa_leaders) if teoa_leaders else "TBD"

        subject = f"📝 New Idea Submission: {idea_data.get('title', 'N/A')}"
        body = f"""Dear Site Leader and TEOA Leader,

A new idea has been submitted and requires your attention:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 IDEA DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Title: {idea_data.get("title", "N/A")}
Proposed Change: {idea_data.get("proposed_change", "N/A")}

Problem Statements: {idea_data.get("problem_statements", "N/A")}

Expected Benefits: {idea_data.get("benefits", "N/A")}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 LOCATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Region: {idea_data.get("region", "N/A")}
BU/CL Site: {idea_data.get("bu_cl_site", "N/A")}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 SUBMITTER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Submitted By: {idea_data.get("submitted_by_name", "N/A")}
Project Lead: {idea_data.get("project_lead", "N/A")}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👔 LEADERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Site Leader: {site_leaders_str}
TEOA Functional Leader: {teoa_leaders_str}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please review and follow up with the submitter.

Best regards,
Procurement Idea Hub
"""

    return send_notification(all_emails, subject, body)
