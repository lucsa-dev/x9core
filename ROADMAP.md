# Roadmap x9core

API de monitoramento com **scraping direto** — sem APIs externas pagas (SerpAPI, Apify, etc.).

## Princípios

- **Hexagonal:** ports & adapters; use cases não conhecem Playwright nem HTML
- **TDD:** teste antes do código; CI 100% offline com HTML fixtures
- **Scraping próprio:** Google Dorks via Playwright; redes sociais via scrapers dedicados
- **Dois gatilhos de monitor:** rota manual `POST /monitors/{id}/run` + scheduler Taskiq

---

## Fase 0 — Fundação ✅

| Step | Entrega | Status |
|------|---------|--------|
| 0 | Docker, FastAPI, PostgreSQL, Redis, pytest, CI | ✅ |
| 0b | Docstrings obrigatórias (Ruff `D`) | ✅ |

---

## Fase 1 — Google Dorks + scraper

| Step | Entrega | Rede na CI? |
|------|---------|-------------|
| **1** | `Dork`, `Clock`, `DorkBuilder` | Não ✅ |
| **2** | `SearchHit`, parser HTML, `SearchProvider`, `SearchByDork`, fake | Não |
| **3** | `POST /v1/search/dork` | Não (fake) |
| **4** | `PlaywrightGoogleScraper` — navega `google.com/search` | Manual/optional |
| **4b** | Rate limit, user-agent, proxy, retry | — |
| **4c** | Gravar HTML fixtures quando layout Google mudar | — |

### Step 4 — scraper Google (detalhe)

```text
Dork + TimeWindow
    → monta URL (q=, tbs=qdr:h|d)
    → Playwright (headless Chromium)
    → HTML da SERP
    → google_serp_parser
    → list[SearchHit]
```

---

## Fase 2 — Monitores (manual + agendado)

| Step | Entrega |
|------|---------|
| **5** | `Person`, `Monitor`, Alembic migrations |
| **6** | Use case `RunMonitor` (trigger: `manual` \| `scheduled`) |
| **7** | `POST /v1/monitors/{id}/run` — disparo manual |
| **8** | Taskiq worker + beat por `interval_minutes` |

```text
POST /monitors/{id}/run  ──┐
                           ├──► RunMonitor ──► SearchByDork ──► PlaywrightGoogleScraper
Taskiq scheduler       ──┘
```

---

## Fase 3 — Scrapers por rede social

Cada plataforma = enricher scraper (Playwright), **sem API oficial**.

| Step | Plataforma | Dificuldade |
|------|------------|-------------|
| **9** | `EnricherRouter` + port `Enricher` | — |
| **10** | YouTube (página do vídeo) | Média |
| **11** | X / Twitter | Alta |
| **12** | TikTok | Alta |
| **13** | Instagram | Muito alta |
| **14** | Facebook | Muito alta |
| **15** | `GET /v1/persons/{id}/mentions` + download de mídia |

---

## Stack de scraping

| Componente | Ferramenta |
|------------|------------|
| Browser | Playwright (Chromium) |
| Parser SERP | BeautifulSoup + lxml |
| Testes | HTML fixtures em `tests/fixtures/` |
| Fila | Taskiq + Redis |
| Anti-ban (prod) | Proxy rotativo, delays, perfis persistentes |

---

## Riscos aceitos

- Google e redes mudam HTML → manutenção contínua dos parsers
- CAPTCHA / IP ban → proxies em produção
- ToS e LGPD → avaliação jurídica necessária
