from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# 项目根目录
# app/core/config.py
# parent -> core
# parent.parent -> app
# parent.parent.parent -> project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """
    Application configuration
    """

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


    # =====================
    # App
    # =====================

    app_title: str = "Enterprise Knowledge Agent"

    app_description: str = (
        "AI Agent Knowledge Base System"
    )

    app_version: str = "0.1.0"


    # =====================
    # LLM API
    # =====================

    openai_api_key: str | None = None


    deepseek_api_key: str | None = None


    deepseek_base_url: str = (
        "https://api.deepseek.com/v1"
    )


    deepseek_model: str = (
        "deepseek-chat"
    )



    # =====================
    # Data
    # =====================

    upload_dir: str = "data"


    chroma_persist_dir: str = (
        "chroma_db"
    )



    # =====================
    # Embedding
    # =====================

    # 本地模型路径
    embedding_model: str = (
        "models/bge-small-zh-v1.5"
    )



    # =====================
    # Path helpers
    # =====================

    @property
    def upload_path(self) -> Path:

        path = Path(self.upload_dir)

        if path.is_absolute():
            return path

        return BASE_DIR / path



    @property
    def chroma_path(self) -> Path:

        path = Path(
            self.chroma_persist_dir
        )

        if path.is_absolute():
            return path

        return BASE_DIR / path



    @property
    def embedding_path(self) -> Path:

        """
        本地 embedding 模型绝对路径
        """

        path = Path(
            self.embedding_model
        )

        if path.is_absolute():
            return path

        return BASE_DIR / path



@lru_cache
def get_settings() -> Settings:

    return Settings()



settings = get_settings()