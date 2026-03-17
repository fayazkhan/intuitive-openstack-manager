# Design Document — Intuitive OpenStack VM Manager (PoC)

## 📌 Purpose

This prototype demonstrates a **REST API for managing OpenStack VM lifecycles** with a focus on:

- Clean API design and documentation (OpenAPI/Swagger)
- Modular architecture with a pluggable backend
- Python best practices (type-safe schemas, config via environment variables)
- Working prototype w/ automated tests

---

## 🧩 High-Level Architecture

### Components

1. **API Layer (FastAPI)**
   - Exposes a versioned REST API under `/v1/vms`
   - Provides OpenAPI documentation automatically
   - Performs request validation and response serialization via Pydantic

2. **Domain Models (Pydantic schemas)**
   - Defines request/response shapes and validation rules
   - Ensures contracts are explicit and self-documenting

3. **Backend Abstraction (OpenStack client interface)**
   - Defines `OpenStackClient` interface for VM lifecycle operations.
   - Provides a `MockOpenStackClient` for local development and PoC.
   - Enables future implementation of a real OpenStack backend using `openstacksdk`.

4. **Configuration (Pydantic Settings)**
   - Uses `pydantic-settings` to load config from environment variables.
   - Allows switching backend (`mock` vs `openstack`) without changing code.

---

## ✅ API Endpoints (v1)

### VM Lifecycle

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/vms` | List all VMs |
| GET | `/v1/vms/{vm_id}` | Fetch details for a single VM |
| POST | `/v1/vms` | Create a new VM |
| DELETE | `/v1/vms/{vm_id}` | Delete a VM |
| POST | `/v1/vms/{vm_id}/actions` | Perform a lifecycle action (`start`, `stop`, `reboot`) |

### Health

| Method | Path | Description |
|--------|------|-------------|
| GET | `/healthz` | Basic health check |

---

## ✅ Domain Model (Core Schemas)

### VMCreateRequest

- `name`: str
- `image`: str
- `flavor`: str
- `network` (optional): str

### VMActionRequest

- `action`: enum `start | stop | reboot`

### VMInstance

- `id`: str
- `name`: str
- `image`: str
- `flavor`: str
- `network`: Optional[str]
- `status`: `build | active | stopped | deleted`
- `created_at`, `updated_at`: datetime

---

## 🔧 Key Design Decisions

### 1) Pluggable Backend

The prototype uses a `get_openstack_client()` factory that selects a backend based on configuration.

- Default: `mock` backend (in-memory store)
- Future: `openstack` backend that uses the `openstacksdk` client to talk to Nova

Benefits:
- Enables fast local development without needing an OpenStack environment
- Clean separation between API and cloud provider logic

### 2) API-first (OpenAPI)

Using FastAPI enables:

- Auto-generated API docs (`/docs` and `/redoc`)
- Strong validation via Pydantic
- Fast iteration with minimal boilerplate

### 3) Testing & Validation

- `pytest` tests ensure API behaves as expected and that the VM lifecycle works end-to-end.
- The mock backend provides deterministic behavior for tests.

---

## 🧠 Implementation Notes

### Configuration

Config is stored in `.env` and loaded via `src/settings.py`.

Key variable:

- `OPENSTACK_BACKEND=mock` (default)

### Mock Backend Behavior

- VM creation returns an instance with `status: build` then immediately transitions to `status: active`.
- VM state is stored in an in-memory dictionary shared across requests using an LRU-cached singleton client.

---

---

## 📌 How to Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Open docs: http://localhost:8000/docs

---

## 🧪 How to Test

```bash
pytest -q
```
