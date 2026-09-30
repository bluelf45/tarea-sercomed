# Chatbot IA

Chatbot web con **React + Vite** (frontend) y **FastAPI** (backend) que usa **Claude Haiku 4.5** para responder a partir de la información que tú le entregas.

## Configuración

1. Copia el archivo de entorno y agrega tu API key de Anthropic:
   ```bash
   cp backend/.env.example backend/.env
   # edita backend/.env → ANTHROPIC_API_KEY=sk-ant-...
   ```
2. Pon tu información en `backend/knowledge/` como archivos `.md` o `.txt` (FAQ, servicios, horarios, precios…). Reemplaza `ejemplo.md`. Todos los archivos se incluyen en el contexto del bot.
3. (Opcional) Personaliza el comportamiento con `SYSTEM_PROMPT` en `backend/.env`. El prompt por defecto está en `backend/app/config.py`.

> El conocimiento y el prompt se cargan al iniciar: **reinicia el backend** después de editarlos.

## Ejecutar con Docker Compose

```bash
docker compose up --build
```
Abre http://localhost:8080 (el backend también queda expuesto en http://localhost:8000, así que `npm run dev` en :5173 funciona contra él).

## Ejecutar en desarrollo

Backend (puerto 8000):
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend (puerto 5173, con proxy de `/api` al backend):
```bash
cd frontend
npm install
npm run dev
```
Abre http://localhost:5173

## API

- `GET /api/health` → `{"status": "ok", "model": "claude-haiku-4-5"}`
- `POST /api/chat` con `{"messages": [{"role": "user", "content": "Hola"}]}` → `{"reply": "..."}`

El servidor no guarda estado: el frontend envía el historial completo en cada solicitud (se usan los últimos `MAX_HISTORY` mensajes, 40 por defecto).

## Variables de entorno (backend)

| Variable | Por defecto | Descripción |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | API key de Anthropic (obligatoria) |
| `MODEL` | `claude-haiku-4-5` | Modelo de Claude |
| `MAX_TOKENS` | `1024` | Largo máximo de cada respuesta |
| `SYSTEM_PROMPT` | ver `config.py` | Instrucciones / personalidad del bot |
| `KNOWLEDGE_DIR` | `backend/knowledge` | Carpeta con la información |
| `MAX_HISTORY` | `40` | Mensajes del historial enviados al modelo |
| `CORS_ORIGINS` | `["http://localhost:5173"]` | Orígenes permitidos (JSON) |
