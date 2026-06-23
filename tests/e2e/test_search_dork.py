"""Testes e2e da rota de busca por dork."""

import pytest
from httpx import ASGITransport, AsyncClient

from x9core.api.dependencies import get_search_provider
from x9core.infrastructure.scraping.fake_search_provider import FakeSearchProvider


@pytest.fixture
def app_with_search(app, sample_serp_html: str):
    app.dependency_overrides[get_search_provider] = lambda: FakeSearchProvider(html=sample_serp_html)
    yield app
    app.dependency_overrides.clear()


@pytest.fixture
async def search_client(app_with_search):
    transport = ASGITransport(app=app_with_search)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.e2e
async def test_search_dork_returns_results(search_client: AsyncClient) -> None:
    response = await search_client.post(
        "/v1/search/dork",
        json={"dork": '"João Silva" site:x.com', "time_window": "24h"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total_raw"] == 3
    assert data["total_unique"] == 2
    assert data["results"][0]["title"] == "João Silva no X"
    assert data["results"][0]["url"] == "https://x.com/joao/status/123456"
    assert data["time_window"] == "24h"


@pytest.mark.e2e
async def test_search_dork_without_time_window(search_client: AsyncClient) -> None:
    response = await search_client.post(
        "/v1/search/dork",
        json={"dork": "site:x.com"},
    )

    assert response.status_code == 200
    assert response.json()["time_window"] is None


@pytest.mark.e2e
async def test_search_dork_rejects_empty_dork(search_client: AsyncClient) -> None:
    response = await search_client.post("/v1/search/dork", json={"dork": "  "})

    assert response.status_code == 422


@pytest.mark.e2e
async def test_search_dork_rejects_invalid_time_window(search_client: AsyncClient) -> None:
    response = await search_client.post(
        "/v1/search/dork",
        json={"dork": "site:x.com", "time_window": "invalid"},
    )

    assert response.status_code == 422


@pytest.mark.e2e
async def test_search_dork_returns_503_when_provider_not_configured(client: AsyncClient) -> None:
    response = await client.post("/v1/search/dork", json={"dork": "site:x.com"})

    assert response.status_code == 503
