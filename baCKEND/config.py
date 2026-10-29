
import os
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()

# application settings
app_name = "worksphere hrms"
app_version = "4.0.0"

# database configuration
database_url = os.getenv(
    "DATABASE_URL",
    "sqlite:///./worksphere.db"
)

# security configuration
secret_key = os.getenv(
    "SECRET_KEY",
    "dev-only-change-this-secret-key"
)

algorithm = "HS256"
access_token_expire_minutes = 30

# frontend configuration
frontend_url = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)
