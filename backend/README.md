# Judo Value Analysis Backend

Backend en FastAPI para análisis y simulación de apuestas de value en judo (sin conexión a casas de apuestas).

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

## 6) Inspección de judobase instalado

```bash
python scripts/inspect_judobase.py
```

## 7) Limitaciones actuales

- Motor de simulación inicial simplificado.
- `search_athlete` usa `find_contests` como adapter temporal (no hay search directo de judoka por nombre expuesto actualmente).
- Si falla Judobase, usa respuestas mock en modo desarrollo.

## 8) Roadmap

- Integrar rating Elo/Glicko por atleta.
- Simulación Monte Carlo por rounds completos.
- Mejor parser de brackets IJF.
- Persistencia de histórico y auditoría de cartera.
