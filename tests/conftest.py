import pytest
from httpx import ASGITransport, AsyncClient
from pathlib import Path

from x9core.api.main import create_app
from x9core.infrastructure.config import Settings

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_serp_html() -> str:
    """HTML gravado de uma SERP do Google para testes offline."""
    return (FIXTURES_DIR / "google" / "sample_serp.html").read_text(encoding="utf-8")


@pytest.fixture
def test_settings() -> Settings:
    return Settings(
        app_env="test",
        debug=True,
        database_url="postgresql+asyncpg://x9core:x9core@localhost:5432/x9core_test",
        redis_url="redis://localhost:6379/1",
    )


@pytest.fixture
def app(test_settings: Settings):
    return create_app(settings=test_settings)


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
