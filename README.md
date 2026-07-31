# ArautoVideo Agent

ArautoVideo is a modular AI video automation platform for discovering topics, researching them, writing scripts, creating storyboards, generating media, and publishing short-form videos.

## Current status

Phase 1 is now runnable. The application accepts a content request and returns:

- a research brief
- a short-form narration script
- a scene-by-scene storyboard
- a structured video-job object

The current agents are deterministic development agents. Live LLM and search providers will be added behind adapters next.

## Run locally

```bash
git clone https://github.com/abdulnajam-boop/allinone-video-app.git
cd allinone-video-app
python -m venv .venv
```

Activate the environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS or Linux
source .venv/bin/activate
```

Install and start:

```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open:

- API documentation: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

## Test the pipeline

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/video-jobs/plan" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "How AI agents create short videos",
    "audience": "new content creators",
    "platform": "youtube_shorts",
    "duration_seconds": 60,
    "tone": "educational"
  }'
```

Run automated tests:

```bash
pytest
```

## Architecture

```text
app/
  agents/          Research, script and storyboard agents
  core/            Settings and shared Pydantic schemas
  providers/       Upcoming LLM, search, TTS, image and video adapters
  services/        Pipeline orchestration
  main.py          FastAPI entry point

tests/             API and pipeline tests
```

## Integration strategy

We will selectively adapt ideas rather than merge entire repositories:

- `awesome-llm-apps`: agent patterns, research, memory, RAG and multi-agent workflows
- `API-mega-list`: API discovery only; every provider must be independently verified
- `MoneyPrinterTurbo`: automated short-video workflow patterns
- `Pixelle-Video`: visual-generation and editing ideas
- `vox-director`: storyboard and directing workflows
- `agent-reach`: distribution and outreach patterns
- `public-apis`: optional free data providers

## Roadmap

### Phase 1 — Agent foundation

- [x] FastAPI application
- [x] Environment configuration
- [x] Shared content and job schemas
- [x] Development research agent
- [x] Development script-writing agent
- [x] Development storyboard agent
- [x] Pipeline endpoint
- [ ] Live search provider
- [ ] Ollama/OpenRouter LLM adapter
- [ ] Source verification and citations

### Phase 2 — Media generation

- [ ] Kokoro or Piper TTS adapter
- [ ] Pexels and Pixabay media adapters
- [ ] Image-generation adapter
- [ ] FFmpeg video assembler
- [ ] Captions

### Phase 3 — Automation and publishing

- [ ] Persistent job storage
- [ ] Scheduler and workers
- [ ] YouTube publishing
- [ ] TikTok and Instagram export workflow
- [ ] Analytics and retry handling
- [ ] n8n integration

## Security

Never commit API keys. Copy `.env.example` to `.env`; `.env` is ignored by Git.

## Licensing

ArautoVideo integration code will be original. Any third-party component or adapted code must retain its own license and attribution requirements.
