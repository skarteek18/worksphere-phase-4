# worksphere-phase-4

WorkSphere – HR Management System (HRMS)

Phase 4: Employee Experience & System Integrations

Project Overview

WorkSphere is a full-stack Human Resource Management System (HRMS) designed to simplify employee management, improve internal communication, and automate HR workflows.

Phase 4 focuses on employee onboarding, resignation management, internal announcements, task tracking, third-party integrations, employee feedback, and profile settings.

Technologies Used

Backend

- Python 3.9+
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- JWT Authentication

Frontend

- React.js
- Vite
- JavaScript
- CSS
- Axios

Project Modules

Module 21: Employee Onboarding System

- Assign onboarding tasks to employees.
- Track onboarding task status.
- Display an employee onboarding checklist.
- Monitor onboarding progress.

Module 22: Resignation & Exit Management

- Allow employees to submit resignation requests.
- Enable HR/Admin to approve or reject resignations.
- Track resignation status and notice periods.
- Maintain exit workflow records.

Module 23: Internal Announcements System

- Allow HR/Admin to publish announcements.
- Display announcements to employees.
- View announcement details and publication dates.

Module 24: Task Assignment & Tracking

- Assign tasks to employees.
- Set task descriptions and due dates.
- Track pending and completed tasks.
- Allow employees to update task status.

Module 25: Third-Party Integrations

- Support email notifications.
- Provide optional Google Calendar integration.
- Export reports in CSV and PDF formats.
- Provide a calendar synchronization interface.

Module 26: Employee Feedback System

- Allow employees to submit feedback.
- Collect ratings and feedback messages.
- Enable HR/Admin to review submitted feedback.

Module 27: Profile & Settings Management

- Update personal profile details.
- Change account passwords securely.
- Manage notification preferences.

Database Tables

New tables

- Onboarding
- Resignations
- Announcements
- Tasks
- Feedback

Existing tables retained

- Users
- Employees
- Attendance
- Leaves
- Payroll
- Notifications
- Shifts
- Performance
- Documents

Security Features

- JWT-based authentication.
- Role-based authorization for employees and HR/Admin.
- Ownership validation for employee-specific records.
- Request validation using Pydantic.
- Secure password hashing.
- Environment-based configuration for secrets and application settings.

Project Structure

worksphere-phase4/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── config.py
│   ├── auth.py
│   ├── onboarding.py
│   ├── resignations.py
│   ├── announcements.py
│   ├── tasks.py
│   ├── integrations.py
│   ├── feedback.py
│   ├── profile.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── api.js
│       ├── index.css
│       └── components/
├── .gitignore
└── README.md

Installation and Setup

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL
cd worksphere-phase4

Replace "YOUR_GITHUB_REPOSITORY_URL" with your actual repository URL.

2. Set up the backend

cd backend
python -m venv venv

Activate the virtual environment.

Windows

venv\Scripts\activate

Linux / GitHub Codespaces

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Configure your environment variables using ".env.example" as a reference. Use development-only secrets and never commit real credentials.

Start the FastAPI server:

uvicorn main:app --reload

Open the API documentation at:

"http://127.0.0.1:8000/docs"

3. Set up the frontend

Open a new terminal:

cd frontend
npm install
npm run dev

Open the local URL provided by Vite, usually:

"http://localhost:5173"

API Functionality

The backend provides endpoints for:

- Employee onboarding and checklist management.
- Resignation submission and approval workflows.
- Announcement creation and viewing.
- Employee task assignment and status updates.
- Email and report export integrations.
- Employee feedback submission and review.
- Profile updates, password changes, and preferences.

Actual endpoint paths and request formats should match the implemented backend modules.

Testing

- Verify API endpoints using Swagger UI.
- Test authentication and role permissions.
- Verify employee ownership restrictions.
- Test onboarding, resignation, and task workflows.
- Validate feedback submission and profile updates.
- Test report exports and configured integrations.

Future Enhancements

- Google Calendar synchronization.
- Automated email notifications.
- Advanced HR analytics and reporting.
- Improved dashboard design.
- Automated testing and deployment.

Conclusion

WorkSphere Phase 4 extends the existing HRMS with employee-focused workflows, communication tools, feedback collection, and system integrations. The goal is to deliver a secure, maintainable, and user-friendly platform that improves everyday HR operations.

Project: WorkSphere – HR Management System
Phase: 4 – Employee Experience & System Integrations
Modules: 21–27
Planned Duration: 2 Days
