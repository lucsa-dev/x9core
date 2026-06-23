import pytest

from x9core.api.main import create_app


def test_create_app_uses_default_settings() -> None:
    app = create_app()
    assert app.title == "x9core"


@pytest.mark.asyncio
async def test_lifespan_context_runs() -> None:
    app = create_app()
    async with app.router.lifespan_context(app):
        assert app.version == "0.1.0"
