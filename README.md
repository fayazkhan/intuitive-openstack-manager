# intuitive-openstack-manager

A proof-of-concept REST API for managing OpenStack virtual machine lifecycles.

This repository shows a minimal but extensible Python-based design for:

- Creating, listing, and deleting VMs
- Starting, stopping, and rebooting VMs
- API-first design using OpenAPI/Swagger (FastAPI)
- Pluggable backend abstraction so a real OpenStack implementation can be swapped in

---

## ✅ Quick start (local demo)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Then open:

- API docs (Swagger UI): http://localhost:8000/docs
- Health check: http://localhost:8000/healthz

---

## 🧠 Architecture & Design

### High-level design

- **API Layer**: `src/main.py` defines a versioned REST API (`/v1/vms`) using FastAPI.
- **Domain Models**: `src/schemas.py` defines request/response models and enums with Pydantic.
- **Backend Abstraction**: `src/openstack_client.py` defines an interface (`OpenStackClient`) and a mock implementation (`MockOpenStackClient`).
- **Configuration**: `src/settings.py` uses Pydantic `BaseSettings` for environment-driven configuration.

### Key design choices

- **Pluggable backend**: A `get_openstack_client` factory selects the backend implementation (mock by default). This delivers a clear seam for adding a real OpenStack-backed implementation later.
- **FastAPI + OpenAPI**: Provides automatic API docs and built-in validation, speeding up development and improving API contract clarity.
- **In-memory mock**: The prototype uses an in-memory store to demonstrate lifecycle workflows without needing an OpenStack deployment.
- **Test coverage**: `tests/test_api.py` verifies the full VM lifecycle against the API.

---

## 🛠️ Implemented API Endpoints

### VM lifecycle

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/vms` | List all VMs |
| GET | `/v1/vms/{vm_id}` | Get a VM by ID |
| POST | `/v1/vms` | Create a VM |
| DELETE | `/v1/vms/{vm_id}` | Delete a VM |
| POST | `/v1/vms/{vm_id}/actions` | Perform lifecycle actions (`start`, `stop`, `reboot`) |

### Health

| Method | Path | Description |
|--------|------|-------------|
| GET | `/healthz` | Basic health check |

---

## 🧪 Running Tests

```bash
pytest -q
```

---

## 🧭 Roadmap / Backlog (beyond PoC)

### Short-term (next iterations)

- ✅ Add a real OpenStack backend using `openstacksdk` and environment-driven config
- ✅ Add request/response schemas for more OpenStack VM properties (metadata, tags, networks, security groups)
- ✅ Add pagination + filtering for list endpoints
- ✅ Add audit/logging / structured request tracing

### Mid-term (production readiness)

- Integrate with CI/CD and automated API contract validation
- Add authentication/authorization (JWT, OAuth 2.0, RBAC)
- Add OpenStack policy enforcement, quota checks, and per-tenant isolation
- Add async job model (create/delete as background jobs with a `/jobs` endpoint)

### Long-term

- Add WebSocket/notification hooks for lifecycle events
- Add multi-region / multi-cloud support (e.g., AWS, Azure) via a provider abstraction

---

## 🧩 Notes / How to Extend

- Swap the mock client by implementing a new backend in `src/openstack_client.py` and wiring it via `openstack_backend` in `.env`.
- Add new VM actions (e.g., `resize`, `snapshot`, `migrate`) by extending `VMAction` and implementing logic in the backend.

---

## 🔎 Useful commands

```bash
# Run the API locally
uvicorn src.main:app --reload

# Run tests
pytest
```
