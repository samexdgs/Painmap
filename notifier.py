"""Notifier — Brevo (Sendinblue) email for reminders and weekly digests.
Free tier: 300 emails/day. Same SMTP infrastructure as SpeakAgain.

Verified sender: Samuel@bloomgatelaw.com (Brevo verified domain).
Contact addresses for replies: soluwakoyat@gmail.com, samueloluwakoyat@gmail.com.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import streamlit as st


def _get_secret(key, default=""):
    """Read from Streamlit secrets first, then env. Accepts multiple
    common Brevo secret key names so the same credentials work whether
    you set them as BREVO_*, SMTP_*, or BREVO_API_KEY."""
    candidates = [key]
    # Allow alternate names matching SpeakAgain conventions
    aliases = {
        "BREVO_SMTP_USER": ["BREVO_USER", "SMTP_USER", "BREVO_LOGIN"],
        "BREVO_SMTP_KEY": ["BREVO_API_KEY", "BREVO_KEY", "SMTP_KEY",
                            "SMTP_PASSWORD", "BREVO_SMTP_PASSWORD"],
        "BREVO_SMTP_HOST": ["SMTP_HOST"],
        "BREVO_SMTP_PORT": ["SMTP_PORT"],
        "BREVO_SENDER": ["SMTP_SENDER", "SENDER_EMAIL", "FROM_EMAIL"],
        "BREVO_SENDER_NAME": ["SENDER_NAME"],
    }
    candidates.extend(aliases.get(key, []))

    for name in candidates:
        # Try Streamlit secrets first
        try:
            if hasattr(st, "secrets") and name in st.secrets:
                v = st.secrets[name]
                if v not in ("", None):
                    return str(v)
        except Exception:
            pass
        # Then env vars
        v = os.environ.get(name)
        if v:
            return v
    return default


def is_configured() -> bool:
    """Return True if Brevo SMTP credentials are present."""
    cfg = _smtp_config()
    return bool(cfg["user"] and cfg["key"])


def _smtp_config():
    return {
        "host": _get_secret("BREVO_SMTP_HOST", "smtp-relay.brevo.com"),
        "port": int(_get_secret("BREVO_SMTP_PORT", "587")),
        "user": _get_secret("BREVO_SMTP_USER", ""),
        "key": _get_secret("BREVO_SMTP_KEY", ""),
        "sender": _get_secret("BREVO_SENDER", "Samuel@bloomgatelaw.com"),
        "sender_name": _get_secret("BREVO_SENDER_NAME", "PainMap"),
    }


def _send(to_email: str, subject: str, html_body: str, text_body: str = "") -> bool:
    cfg = _smtp_config()
    if not cfg["user"] or not cfg["key"]:
        return False  # not configured — silent fail, app still works

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{cfg['sender_name']} <{cfg['sender']}>"
    msg["To"] = to_email
    msg["Reply-To"] = "soluwakoyat@gmail.com"

    if text_body:
        msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(cfg["host"], cfg["port"], timeout=15) as server:
            server.starttls()
            server.login(cfg["user"], cfg["key"])
            server.sendmail(cfg["sender"], [to_email], msg.as_string())
        return True
    except Exception as e:
        # Log silently — don't crash the app on email failure
        print(f"[notifier] Email send failed: {e}")
        return False


def send_test_email(to_email: str) -> tuple[bool, str]:
    """Returns (success, diagnostic_message)."""
    cfg = _smtp_config()
    if not cfg["user"]:
        return False, ("Brevo SMTP user is missing. In Streamlit Cloud → "
                        "App Settings → Secrets, add `BREVO_SMTP_USER` "
                        "(this is your Brevo login email, not API key).")
    if not cfg["key"]:
        return False, ("Brevo SMTP key is missing. In Streamlit Cloud → "
                        "App Settings → Secrets, add `BREVO_SMTP_KEY` with "
                        "your Brevo SMTP key from brevo.com → SMTP & API → "
                        "SMTP tab (NOT the API key from the API tab).")
    html = """
    <div style="font-family: Arial, sans-serif; max-width: 540px; margin: 0 auto;">
        <h2 style="color: #2D5986;">PainMap is connected ✅</h2>
        <p>Your email reminders are set up. You'll get gentle nudges to log
        pain at the times you chose, plus a weekly summary every Sunday.</p>
        <p style="color: #888; font-size: 12px;">
            Research prototype. Not medical advice.
        </p>
    </div>
    """
    ok = _send(to_email, "PainMap reminder test", html,
                "PainMap is connected. Your reminders are working.")
    if ok:
        return True, f"Email sent to {to_email}. Check your inbox (and spam)."
    return False, ("SMTP credentials look set but the connection failed. "
                    "Check Brevo logs at brevo.com → Logs.")


def send_reminder(to_email: str, label: str) -> bool:
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 540px; margin: 0 auto;">
        <h3 style="color: #2D5986;">🔔 PainMap reminder</h3>
        <p><strong>{label}</strong></p>
        <p>A small log right now keeps your patterns accurate.</p>
        <p style="text-align: center; margin: 24px 0;">
            <a href="https://painmap.streamlit.app"
               style="background: #2D5986; color: white; padding: 12px 24px;
                       text-decoration: none; border-radius: 6px;">
                Open PainMap
            </a>
        </p>
        <p style="color: #888; font-size: 12px;">
            Research prototype. Not medical advice.
        </p>
    </div>
    """
    return _send(to_email, f"PainMap: {label}", html,
                  f"PainMap reminder: {label}")


def send_weekly_digest(to_email: str, summary: dict) -> bool:
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 540px; margin: 0 auto;">
        <h2 style="color: #2D5986;">Your week in PainMap</h2>
        <ul>
            <li><strong>{summary.get('total_logs', 0)}</strong> logs this week</li>
            <li>Average intensity: <strong>{summary.get('avg_intensity', 0):.1f}/10</strong></li>
            <li>Most painful region: <strong>{summary.get('top_region', '—')}</strong></li>
        </ul>
        <p>Open the app to view trends and export a PDF for your physio.</p>
        <p style="color: #888; font-size: 12px;">
            Research prototype. Not medical advice.
        </p>
    </div>
    """
    return _send(to_email, "Your PainMap weekly summary", html)
