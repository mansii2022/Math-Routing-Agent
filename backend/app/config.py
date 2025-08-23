from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    model: str = Field(default="gpt-4o-mini", alias="MODEL")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    anthropic_api_key: str | None = Field(default=None, alias="ANTHROPIC_API_KEY")

    # search
    tavily_api_key: str | None = Field(default=None, alias="TAVILY_API_KEY")
    exa_api_key: str | None = Field(default=None, alias="EXA_API_KEY")
    serper_api_key: str | None = Field(default=None, alias="SERPER_API_KEY")

    # qdrant
    qdrant_url: str = Field(default="http://localhost:6333", alias="QDRANT_URL")
    qdrant_api_key: str | None = Field(default=None, alias="QDRANT_API_KEY")

    # mcp
    mcp_server: str | None = Field(default=None, alias="MCP_SERVER")
    mcp_tool_name: str | None = Field(default="search", alias="MCP_TOOL_NAME")

    allow_web_search: bool = Field(default=True, alias="ALLOW_WEB_SEARCH")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
