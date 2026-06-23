"""Schemas HTTP da API."""

from pydantic import BaseModel, Field


class SearchHitResponse(BaseModel):
    """Resultado individual de uma busca por dork."""

    title: str
    url: str
    snippet: str


class SearchDorkRequest(BaseModel):
    """Corpo da requisição de busca por Google Dork."""

    dork: str = Field(min_length=1, description="Query de Google Dork")
    time_window: str | None = Field(
        default=None,
        description="Janela temporal opcional (ex.: 12h, 24h, 7d)",
    )


class SearchDorkResponse(BaseModel):
    """Resposta da busca por dork."""

    dork: str
    time_window: str | None
    total_raw: int
    total_unique: int
    results: list[SearchHitResponse]
