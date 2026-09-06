# CareOrchestrator MVP

CareOrchestrator is a multi-agent AI system for proactive chronic disease management.

## MVP stack

- Frontend: Next.js 14 + Tailwind CSS
- Backend: FastAPI + Python 3.10
- Database/Auth/Realtime: Supabase
- AI orchestration: LangChain
- AI inference: OpenRouter
- Free AI routing: `openrouter/free`
- WhatsApp integration: OpenWA
- Scheduling: APScheduler

## Important safety boundary

This is an MVP and not a certified medical device.

The deterministic monitoring thresholds in this repository are engineering defaults. They must be reviewed and validated by qualified clinicians before use with real patients.

The AI model must not determine clinical severity. Risk classification is performed by deterministic monitoring rules. OpenRouter is used only for communication wording and summarization.

## OpenWA

OpenWA is used as a self-hosted WhatsApp API gateway.

For this MVP:

```bash
git clone https://github.com/rmyndharis/OpenWA.git
cd OpenWA
npm ci
```

Copy the minimal configuration and create runtime directories.

On Windows PowerShell:

```powershell
Copy-Item .env.minimal .env
New-Item -ItemType Directory -Force data\sessions
New-Item -ItemType Directory -Force data\media
npm run start:dev
```

The API runs at:

```text
http://localhost:2785/api
```

Swagger:

```text
http://localhost:2785/api/docs
```

On first run OpenWA generates an API key. Store it in the CareOrchestrator backend `.env` file.

Create and connect a WhatsApp session through the OpenWA API or Swagger interface. Set its session ID as:

```env
OPENWA_SESSION_ID=your_session_id
```

## OpenRouter

Create an OpenRouter API key and configure:

```env
OPENROUTER_API_KEY=your_key
OPENROUTER_MODEL=openrouter/free
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

`openrouter/free` automatically routes requests to an available free model.

Free models can have rate and availability limits. This is acceptable for a low-volume MVP but is not a reliability guarantee for production.

## Supabase setup

1. Create a Supabase project.
2. Open SQL Editor.
3. Execute:

```text
backend/db/schema.sql
```

4. Enable Realtime for the `alerts` table.
5. Copy the project URL, anon key, and service-role key.

Never expose the service-role key to the frontend.

## Backend setup

```bash
cd backend
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy:

```text
.env.example -> .env
```

Configure all environment variables.

Start:

```bash
uvicorn main:app --reload --port 8000
```

API docs:

```text
http://localhost:8000/docs
```

## Frontend setup

```bash
cd frontend
npm install
```

Copy:

```text
.env.example -> .env.local
```

Start:

```bash
npm run dev
```

Open:

```text
http://localhost:3000
```

## Environment variables

### Backend

```env
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
SUPABASE_ANON_KEY=

OPENROUTER_API_KEY=
OPENROUTER_MODEL=openrouter/free
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

OPENWA_BASE_URL=http://localhost:2785/api
OPENWA_API_KEY=
OPENWA_SESSION_ID=careorchestrator

FRONTEND_ORIGIN=http://localhost:3000
ORCHESTRATOR_INTERVAL_HOURS=6
ORCHESTRATOR_ENABLED=true
```

### Frontend

```env
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Agent flow

```text
Vitals
  |
  v
Monitoring Agent
  |
  v
Deterministic Risk Assessment
  |
  +--> LOW ---------> Store status
  |
  +--> MEDIUM ------> OpenRouter message -> OpenWA -> Patient WhatsApp
  |
  +--> HIGH --------> Patient WhatsApp + Clinical Alert + Clinician WhatsApp
  |
  +--> CRITICAL ----> Patient WhatsApp + Clinical Alert + Clinician WhatsApp
  |
  +--> Missed 24h check-in -> Caregiver Agent -> Caregiver WhatsApp
```

## Build ZIP

From the project root:

```bash
python scripts/build_zip.py
```

This creates:

```text
careorchestrator.zip
```
