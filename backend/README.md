# Judo Value Analysis Backend

Backend en FastAPI para análisis y simulación de apuestas de value en judo (sin conexión a casas de apuestas).

## Levantar backend + frontend

Terminal 1:
```bash
cd backend
uvicorn app.main:app --reload
```

Terminal 2:
```bash
cd frontend
npm install
npm run dev
```

## 1) Instalación

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Ejecutar backend

```bash
uvicorn app.main:app --reload
```

## 3) Instalar judobase

El paquete ya está en `requirements.txt`, pero también puedes instalarlo manualmente:

```bash
pip install judobase
```

## 4) Probar endpoint health

```bash
curl http://localhost:8000/health
```

## 5) Ejemplo `POST /analyze/bracket`

Primero crea/usa el ejemplo en `examples/qazaqstan_sample_request.json`.

```bash
curl -X POST http://localhost:8000/analyze/bracket \
  -H "Content-Type: application/json" \
  -d @examples/qazaqstan_sample_request.json
```

<<<<<<< codex/create-python-fastapi-app-for-judo-betting-analysis-ndfqli

## 5.1) Ejemplo `POST /analyze/tournament`

```bash
curl -X POST http://localhost:8000/analyze/tournament \
  -H "Content-Type: application/json" \
  -d @examples/qazaqstan_tournament_sample_request.json
```


## Construcción de request completo con cuotas/strengths

```bash
python scripts/build_tournament_request.py
```

Genera `examples/qazaqstan_2026_ready_to_analyze.json` fusionando brackets + cuotas + strengths.


## Análisis local Qazaqstan (CLI)

```bash
python scripts/analyze_qazaqstan.py --top 30 --only-positive
```

Opcional: `--weight "-60 kg"` para analizar solo un peso.

## 6) Cómo se calcula `strength_score`

Modelo inicial de scoring por judoka:

- Base:
  - si existe `manual_rating`, se usa como base fuerte,
  - si no, base = 50.
- Ranking:
  - `rank_score = max(0, 100 - world_rank)`
- Puntos:
  - `points_score = log(1 + ranking_points)`
- Forma reciente:
  - `recent_form = recent_wins * 3 - recent_losses * 2`
- H2H:
  - `h2h_bonus = h2h_wins * 4 - h2h_losses * 4`

Score final:

`strength = base + rank_score + points_score + recent_form + h2h_bonus`

Luego se normaliza para que nunca sea menor que 1.

Probabilidad de combate directo (A vs B):

`prob_a = 1 / (1 + 10 ** ((score_b - score_a) / 40))`

acotada entre 0.05 y 0.95.


## Simulación Monte Carlo de bracket

`/analyze/bracket` usa simulación Monte Carlo por estructura de pools (A/B/C/D):

- Simula combates de primera ronda (incluyendo byes).
- Simula cruces internos de cada pool hasta obtener 1 ganador por pool.
- Simula semifinales: A vs B y C vs D.
- Simula final para estimar campeón.

Definiciones:
- `winner_probability`: probabilidad de ganar el oro (la suma total es ~1).
- `top4_probability`: probabilidad de ganar el pool y llegar a semifinales (la suma total es ~4).

## 7) Uso de `manual_rating`

`manual_rating` permite corregir el modelo con criterio experto (lesiones recientes, forma no reflejada en ranking, contexto táctico, etc.).

## 8) Inspección de judobase instalado
=======
## 6) Inspección de judobase instalado
>>>>>>> main

```bash
python scripts/inspect_judobase.py
```

<<<<<<< codex/create-python-fastapi-app-for-judo-betting-analysis-ndfqli
## 9) Limitaciones actuales
=======
## 7) Limitaciones actuales
>>>>>>> main

- Motor de simulación inicial simplificado.
- `search_athlete` usa `find_contests` como adapter temporal (no hay search directo de judoka por nombre expuesto actualmente).
- Si falla Judobase, usa respuestas mock en modo desarrollo.
<<<<<<< codex/create-python-fastapi-app-for-judo-betting-analysis-ndfqli
- Este sistema es un modelo inicial para análisis y **no garantiza beneficio**.

## 10) Roadmap
=======

## 8) Roadmap
>>>>>>> main

- Integrar rating Elo/Glicko por atleta.
- Simulación Monte Carlo por rounds completos.
- Mejor parser de brackets IJF.
- Persistencia de histórico y auditoría de cartera.
<<<<<<< codex/create-python-fastapi-app-for-judo-betting-analysis-ndfqli

### Troubleshooting frontend "Failed to fetch"

Si `GET /health` responde OK pero en frontend aparece `Failed to fetch`, normalmente es:
- CORS mal configurado, o
- backend no levantado en `http://localhost:8000` (revisar `VITE_API_BASE_URL`).

=======
>>>>>>> main
