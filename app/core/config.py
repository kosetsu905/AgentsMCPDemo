# app/core/config.py
""" Application configuration """

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",  # 从.env文件读取配置
        case_sensitive=True,
        extra="ignore",  # 允许额外的环境变量而不报错
    )

    # 应用基础配置
    PROJECT_NAME: str = "AI Agent API"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # API配置
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # LLM配置（支持多供应商）
    LLM_PROVIDER: str = "openai"  # 或 "anthropic"
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    DEFAULT_LLM_MODEL: str = "gpt-4o"
    DEFAULT_TEMPERATURE: float = 0.7

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "console"  # 或 "json"

    # Database (optional)
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_agent"

    # Observability (optional)
    LANGSMITH_API_KEY: str = ""
    LANGSMITH_PROJECT: str = "ai-agent-project"
    ENABLE_TRACING: bool = False


settings = Settings()  # 全局配置实例