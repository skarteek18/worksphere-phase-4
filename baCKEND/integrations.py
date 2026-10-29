

import csv
import io
import os
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from database import get_db
from models import User, Task, Onboarding, Resignation, Feedback
from auth import get_current_user, require_hr_or_admin

router = APIRouter()


# send email notification
@router.post("/email")
def send_email(
    recipient: str,
    subject: str,
    message: str,
    current_user: User = Depends(require_hr_or_admin)
):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("SMTP_FROM", smtp_user or "")

    if not all([smtp_host, smtp_user, smtp_password, sender]):
        raise HTTPException(
            status_code=503,
            detail="Email integration is not configured"
        )

    import smtplib
    from email.message import EmailMessage

    email = EmailMessage()
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = subject
    email.set_content(message)

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(email)
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Unable to send email"
        )

    return {"message": "Email sent successfully"}


# export tasks report as csv
@router.get("/export/tasks/csv")
def export_tasks_csv(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr_or_admin)
):
    tasks = db.query(Task).all()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "id", "assigned_to", "title", "description", "due_date", "status"
    ])

    for task in tasks:
        writer.writerow([
            task.id,
            task.assigned_to,
            task.title,
            task.description or "",
            task.due_date.isoformat() if task.due_date else "",
            task.status
        ])

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=tasks_report.csv"
        }
    )


# export tasks report as pdf
@router.get("/export/tasks/pdf")
def export_tasks_pdf(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr_or_admin)
):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError:
        raise HTTPException(
            status_code=503,
            detail="Install reportlab to enable PDF export"
        )

    tasks = db.query(Task).all()

    output = io.BytesIO()
    pdf = canvas.Canvas(output, pagesize=A4)
    width, height = A4
    y = height - 50

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, "WorkSphere HRMS - Tasks Report")
    y -= 30

    pdf.setFont("Helvetica", 9)

    for task in tasks:
        line = (
            f"ID: {task.id} | Employee: {task.assigned_to} | "
            f"Task: {task.title[:35]} | Status: {task.status}"
        )

        pdf.drawString(40, y, line)
        y -= 18

        if y < 50:
            pdf.showPage()
            y = height - 50
            pdf.setFont("Helvetica", 9)

    pdf.save()
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=tasks_report.pdf"
        }
    )


# integration status
@router.get("/status")
def integration_status(
    current_user: User = Depends(get_current_user)
):
    return {
        "email_configured": bool(
            os.getenv("SMTP_HOST")
            and os.getenv("SMTP_USER")
            and os.getenv("SMTP_PASSWORD")
        ),
        "google_calendar": "optional - not configured",
        "csv_export": True,
        "pdf_export": True
    }


# optional google calendar sync placeholder
@router.post("/calendar/sync")
def calendar_sync(
    current_user: User = Depends(require_hr_or_admin)
):
    return {
        "message": "Google Calendar integration requires OAuth credentials",
        "configured": bool(os.getenv("GOOGLE_CLIENT_ID"))
    }
