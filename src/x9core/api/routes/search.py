"""Rotas HTTP da API."""

from fastapi import APIRouter, HTTPException, status

from x9core.api.dependencies import SearchByDorkDep
from x9core.api.schemas.search import (
    SearchDorkRequest,
    SearchDorkResponse,
    SearchHitResponse,
)
from x9core.application.use_cases.search_by_dork import SearchByDorkInput
from x9core.domain.value_objects.dork import Dork
from x9core.domain.value_objects.time_window import TimeWindow

router = APIRouter(prefix="/v1", tags=["search"])


@router.post("/search/dork", response_model=SearchDorkResponse)
async def search_dork(
    body: SearchDorkRequest,
    use_case: SearchByDorkDep,
) -> SearchDorkResponse:
    """Executa uma busca por Google Dork e retorna resultados deduplicados."""
    try:
        dork = Dork(body.dork)
        time_window = TimeWindow.from_string(body.time_window) if body.time_window else None
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    output = await use_case.execute(SearchByDorkInput(dork=dork, time_window=time_window))

    return SearchDorkResponse(
        dork=str(dork),
        time_window=body.time_window,
        total_raw=output.total_raw,
        total_unique=output.total_unique,
        results=[
            SearchHitResponse(title=hit.title, url=hit.url, snippet=hit.snippet)
            for hit in output.results
        ],
    )
