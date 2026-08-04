from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    # App
    app_name: str = "CloudPDF Toolkit"
    log_level: str = "INFO"
    frontend_url: str = "http://localhost:8080"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/cloudpdf"

    # JWT
    secret_key: str = "change-me-in-production-use-random-64-char-hex"
    jwt_expiry_days: int = 7

    # Google OAuth
    google_client_id: str = ""
    google_client_secret: str = ""

    # PDF
    max_file_size_mb: int = 30
    request_timeout_seconds: int = 600
    max_pages_rearrange: int = 200

    # Cleanup
    cleanup_interval_seconds: int = 300
    orphan_age_seconds: int = 900


settings = Settings()
