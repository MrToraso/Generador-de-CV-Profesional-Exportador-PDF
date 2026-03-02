# ResumeFix (FastAPI SaaS)

ResumeFix es un SaaS para optimizar candidaturas laborales mediante análisis de compatibilidad entre CV y ofertas.

## Funcionalidades incluidas
- Registro y login con JWT
- Subida de CV en texto (`.txt`) o PDF (`.pdf`)
- Pegado de descripción de oferta laboral
- Análisis de coincidencia de palabras clave
- Cálculo de score de compatibilidad
- Persistencia de usuarios, CVs, ofertas y resultados en base de datos
- Sistema de planes `free` y `premium`
- Exportación de CV optimizado en PDF (ATS-friendly)
- Cobros internacionales con Stripe (checkout + webhook)

## Estructura del proyecto
```bash
.
├── app
│   ├── main.py
│   ├── api
│   │   ├── deps.py
│   │   └── v1
│   │       ├── auth.py
│   │       ├── billing.py
│   │       ├── plans.py
│   │       └── resume_analysis.py
│   ├── core
│   │   ├── config.py
│   │   └── security.py
│   ├── db
│   │   ├── base.py
│   │   └── session.py
│   ├── models
│   │   ├── analysis.py
│   │   ├── job_offer.py
│   │   ├── resume.py
│   │   └── user.py
│   ├── schemas
│   │   ├── analysis.py
│   │   ├── auth.py
│   │   ├── plan.py
│   │   └── resume.py
│   ├── services
│   │   ├── billing.py
│   │   ├── matching.py
│   │   ├── pdf_generator.py
│   │   └── resume_parser.py
│   └── utils
│       └── limits.py
├── requirements.txt
├── .env.example
└── tests
    ├── test_matching.py
    └── test_pdf_generator.py
```

## Configuración
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Configura Stripe en `.env`:
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `STRIPE_PREMIUM_PRICE_ID`
- `STRIPE_SUCCESS_URL`
- `STRIPE_CANCEL_URL`

## Ejecutar
```bash
uvicorn app.main:app --reload
```

## Endpoints principales
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/plans/me`
- `POST /api/v1/plans/upgrade`
- `POST /api/v1/billing/checkout/premium`
- `POST /api/v1/billing/webhook`
- `POST /api/v1/resume-analysis/analyze`
- `GET /api/v1/resume-analysis/history`
- `GET /api/v1/resume-analysis/{analysis_id}/export-pdf`

## Notas de planes
- Plan `free`: máx. 3 análisis guardados.
- Plan `premium`: sin límite.


## Frontend React
Se agregó un frontend completo en `frontend/` con:
- Login y registro
- Dashboard con formulario para subir CV y analizarlo
- Vista de resultados y descarga de PDF optimizado
- Ruteo con `react-router-dom`
- Manejo de estado global de autenticación con Context API
- Integración con backend en `/api/v1` (proxy en Vite a `http://localhost:8000`)

### Ejecutar frontend
```bash
cd frontend
npm install
npm run dev
```

Rutas frontend:
- `/login`
- `/registro`
- `/dashboard`
- `/resultados/:analysisId`
