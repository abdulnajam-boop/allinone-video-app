# TurboVec Memory Setup

TurboVec is an optional local vector-memory provider for ArautoVideo. It lets the research and script agents retrieve semantically related research, scripts, sources, brand rules, and previous video plans without sending that memory to a managed vector-database service.

## What it will store

Good candidates include:

- approved research notes and source summaries
- previously generated scripts
- storyboard and scene descriptions
- channel style and brand rules
- performance lessons from published videos
- reusable hooks, calls to action, and topic clusters

Do not store API keys, passwords, access tokens, or private user information in vector memory.

## 1. Open the project

In GitHub, open `abdulnajam-boop/allinone-video-app`, select **Code**, then **Codespaces**, then **Create codespace on main**.

## 2. Open a terminal

Use **Terminal → New Terminal**.

## 3. Create and activate the Python environment

```bash
python -m venv .venv
source .venv/bin/activate
```

When reopening the Codespace later, only run:

```bash
source .venv/bin/activate
```

## 4. Install the base project

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Install the optional memory packages

```bash
pip install -r requirements-memory.txt
```

This installs:

- `turbovec` for the local vector index
- `sentence-transformers` for a free local embedding model
- `numpy` for vector arrays

## 6. Run a quick TurboVec test

Create a temporary file:

```bash
cat > test_turbovec.py <<'PY'
from sentence_transformers import SentenceTransformer

from app.providers.memory.turbovec_store import MemoryDocument, TurboVecMemoryStore

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

store = TurboVecMemoryStore(
    embedding_model=model,
    dimension=384,
)

store.add(
    [
        MemoryDocument(
            document_id=1,
            text="Short videos should open with a strong hook in the first seconds.",
            metadata={"type": "content_rule", "platform": "youtube_shorts"},
        ),
        MemoryDocument(
            document_id=2,
            text="ArautoVideo uses research, script, storyboard, voice, and video agents.",
            metadata={"type": "project_note", "project": "arautovideo"},
        ),
    ]
)

for result in store.search("How should a short video begin?", limit=2):
    print(result)
PY
```

Run it:

```bash
python test_turbovec.py
```

The first run downloads the free embedding model. The output should return the document about using a strong opening hook near the top.

## 7. Confirm the local memory files

```bash
find data/memory -maxdepth 1 -type f -print
```

You should see:

```text
data/memory/arautovideo.tvim
data/memory/documents.json
```

The `.tvim` file contains the TurboVec index. The JSON file maps numeric vector IDs back to text and metadata.

## 8. Start the ArautoVideo API

```bash
cp -n .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open the forwarded port and add `/docs` to the URL.

## 9. Remove the temporary test file

After the test succeeds:

```bash
rm test_turbovec.py
```

## Current integration status

The TurboVec provider is installed and ready, but it is not yet called automatically by the research pipeline. The next code stage will add a memory service that:

1. searches TurboVec before script generation
2. inserts relevant memories into the agent prompt
3. saves approved scripts and research after a video job completes
4. keeps memory optional when TurboVec is not installed

## Troubleshooting

### `RuntimeError: TurboVec memory dependencies are not installed`

Run:

```bash
pip install -r requirements-memory.txt
```

### Embedding dimension error

`all-MiniLM-L6-v2` produces 384-dimensional vectors, so use:

```python
dimension=384
```

The configured dimension must always match the embedding model.

### Codespace runs out of memory

Close unused terminals and processes. For initial testing, use the small `all-MiniLM-L6-v2` model and only a few documents.

### Rebuild local memory

For development only, remove the index and metadata and rerun the test:

```bash
rm -f data/memory/arautovideo.tvim data/memory/documents.json
python test_turbovec.py
```
