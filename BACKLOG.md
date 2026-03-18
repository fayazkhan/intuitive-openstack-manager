Improvements
============

- [x] Working prototype.
- [x] Design document.
- [x] Comprehensive README.

## Roadmap (Beyond PoC)

### Short-term

- [x] GitHub Actions CI pipeline with tests and linting.
- [x] Add a Dockerfile for containerized deployment.
- [x] Use idempotent API design for VM creation (e.g., client-generated UUIDs).
- [x] Fix singleton client so state persists across requests
- [x] Convert deprecated Pydantic APIs (`BaseModel.copy`, etc.)
- [ ] Add pagination/filtering for `GET /v1/vms`
- [ ] Add metrics / structured logging
- [ ] Add API versioning strategy (headers / content negotiation)
- [ ] Add idempotency for update operations.
- [ ] Stronger code quality checks (type coverage, static analysis)
- [ ] Freeze build dependencies for reproducible installs (e.g., `pip freeze > requirements.txt`)

### Mid-term

- [ ] Implement real OpenStack backend using `openstacksdk`:
  - [ ] Authentication (Keystone)
  - [ ] Tenant/Project isolation
  - [ ] Flavor, image, network validation
  - [ ] Error mapping (OpenStack errors → HTTP errors)

- [ ] Add authentication/authorization (JWT or OAuth 2.0)
- [ ] Introduce a background job model (async create/delete with job tracking)

### Long-term

- [ ] Multi-cloud provider abstraction (AWS / Azure) for uniform VM lifecycle API
- [ ] Event streaming for VM lifecycle changes (webhooks / message bus)
- [ ] Policy enforcement and quota management
