# intuitive-openstack-manager

A proof-of-concept REST API for managing OpenStack virtual machine lifecycles.

This repo demonstrates a minimal but extensible Python-based design for:

- Creating, listing, and deleting VMs
- Starting, stopping, and rebooting VMs
- API-first design using OpenAPI/Swagger (FastAPI)
- Pluggable backend abstraction so a real OpenStack implementation can be swapped in

---

## ✅ Quick start (local demo)

```bash
python3.14 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]

# Run the API
uvicorn intuitive_openstack_manager.main:app --reload --host 0.0.0.0 --port 8000
```

Then open:

- API docs (Swagger UI): http://localhost:8000/docs
- Health check: http://localhost:8000/healthz

---

## 🔍 What’s included

### REST API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/vms` | List all VMs |
| GET | `/v1/vms/{vm_id}` | Get a VM by ID |
| POST | `/v1/vms` | Create a VM |
| DELETE | `/v1/vms/{vm_id}` | Delete a VM |
| POST | `/v1/vms/{vm_id}/actions` | Perform lifecycle actions (`start`, `stop`, `reboot`) |

### Automated tests

- `tests/test_api.py` exercises the full VM lifecycle against the REST API.

---

## 📚 Documentation & Next Steps

- **Design details:** See `DESIGN.md` for architecture, schema decisions, and implementation notes.
- **Roadmap/backlog:** See `BACKLOG.md` for planned improvements and future work.

---

## 🧪 Run tests

```bash
source .venv/bin/activate
python -m pytest -q
```
