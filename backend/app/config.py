from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(default="sqlite:///./ecommerce.db")
    ENABLE_NOMINATIM: bool = Field(default=False)
    NOMINATIM_USER_AGENT: str = Field(default="hyperlocal-ecommerce-demo")
    CORS_ORIGINS: str = Field(default="*")  # comma-separated for production

settings = Settings()
