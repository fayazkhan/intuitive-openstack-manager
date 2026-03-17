# intuitive-openstack-manager

[![CI](https://github.com/fayazkhan/intuitive-openstack-manager/actions/workflows/ci.yml/badge.svg)](https://github.com/fayazkhan/intuitive-openstack-manager/actions/workflows/ci.yml) [![Python](https://img.shields.io/badge/python-3.14%2B-blue)](https://www.python.org/) [![Coverage](https://img.shields.io/codecov/c/github/fayazkhan/intuitive-openstack-manager?logo=codecov)](https://codecov.io/gh/fayazkhan/intuitive-openstack-manager) [![Code Quality](https://img.shields.io/codefactor/grade/github/fayazkhan/intuitive-openstack-manager?logo=codefactor)](https://www.codefactor.io/repository/github/fayazkhan/intuitive-openstack-manager)

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
