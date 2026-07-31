# ArautoVideo Agent

An open-source, modular AI video automation platform for discovering trends, researching topics, writing scripts, generating voiceovers, assembling videos, and publishing content.

## Goal

Build one unified system using selected ideas from:

- `awesome-llm-apps` for agent patterns, research, memory, RAG, and multi-agent workflows
- `MoneyPrinterTurbo` for automated short-video production patterns
- `Pixelle-Video` for visual generation and editing ideas
- `vox-director` for directing and storyboard workflows
- `agent-reach` for distribution and outreach patterns
- `public-apis` for optional free data sources

We will not copy all repositories into this project. Each integration will be isolated behind a clean adapter.

## Phase 1 Pipeline

```text
Topic Request
    ↓
Trend Research Agent
    ↓
Research/Sources Agent
    ↓
Script Writer Agent
    ↓
Storyboard Agent
    ↓
Structured Video Job JSON
```

## Planned Architecture

```text
app/
  api/             FastAPI endpoints
  agents/          Research, script, storyboard and publishing agents
  core/            Configuration, logging and shared models
  providers/       LLM, search, TTS, image and video adapters
  services/        Pipeline orchestration and job management
  workers/         Long-running media jobs
  main.py           Application entry point

data/
  jobs/             Local development job files

tests/
```

## Provider Strategy

The project will support interchangeable providers:

- LLM: Ollama/local models, OpenRouter, Gemini, OpenAI
- Search: public APIs, RSS, Reddit and optional web-search providers
- TTS: Kokoro/Piper first, with optional cloud providers
- Video: FFmpeg-based assembly first
- Storage: local filesystem first, then optional Cloudflare R2/S3

## Development Roadmap

### Phase 1 — Agent foundation

- [ ] FastAPI application
- [ ] Environment configuration
- [ ] Shared content and job schemas
- [ ] Research agent
- [ ] Script-writing agent
- [ ] Storyboard agent
- [ ] Pipeline endpoint

### Phase 2 — Media generation

- [ ] Local/open-source TTS adapter
- [ ] Stock-media providers
- [ ] Image-generation adapter
- [ ] FFmpeg video assembler
- [ ] Captions

### Phase 3 — Automation and publishing

- [ ] Scheduler
- [ ] YouTube publishing
- [ ] TikTok/Instagram export workflow
- [ ] Analytics and retry handling
- [ ] n8n integration

## Important

Never commit API keys. Copy `.env.example` to `.env` and keep `.env` private.

## License

This repository will contain original integration code. Third-party components remain governed by their own licenses and notices.
