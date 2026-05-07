## Serial Number Detection Agent

FastAPI service and utilities for extracting serial numbers from equipment
images using a Gemini model. Includes a local runner script, an integration
test suite with labeled examples, and API endpoints for uploads and internal
images.

### Features

- Detect serial numbers from an uploaded image.
- Detect serial numbers from an image stored under data/.
- Cached model initialization via FastAPI dependency injection.
- Integration tests driven by tests/data/examples.json.

### Requirements

- Python 3.14+
- uv (recommended) or any environment manager

Runtime dependencies (see pyproject.toml):
- fastapi, uvicorn
- deepagents
- pydantic, pydantic-settings
- pillow
- python-dotenv
- python-multipart (for uploads)

### Setup

Create and sync the environment:

```bash
uv sync
```

If you manage dependencies manually, install from pyproject.toml.

### Environment

Create a .env file in the repo root. Example:

```env
GEMINI_API_KEY=your_api_key_here
```

The service loads .env on startup and Docker also passes it via env_file.

### Run the API

Local:

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Docker:

```bash
docker compose up -d --build
```

### API Routes

Upload an image:

```bash
curl -X POST "http://localhost:8000/serial-number/upload" \
	-F "file=@data/image_1.jpg"
```

Use an internal image path (data/ only):

```bash
curl -X POST "http://localhost:8000/serial-number/path" \
	-H "Content-Type: application/json" \
	-d '{"filename":"image_1.jpg"}'
```

### Tests

Unit tests (skip CI-marked integration tests):

```bash
uv run pytest -m "not ci"
```

Full test suite (includes integration tests that call the model):

```bash
uv run pytest
```

The integration test uses tests/data/examples.json to map image filenames to
expected serial numbers.

### Pre-commit

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

By default, pre-commit runs pytest with -m "not ci".

### Future improvements

- Include OpenRouter for using multiple models.
- Use a deep agent to chat with users, check manufacturer knowledge-base, consult
	historical data, and call an OCR subagent.
