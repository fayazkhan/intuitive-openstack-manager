"""REST API for managing OpenStack VM lifecycles."""

from functools import lru_cache

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .openstack_client import OpenStackClient, get_openstack_client
from .schemas import VMActionRequest, VMCreateRequest, VMInstance
from .settings import settings


app = FastAPI(
    title="Intuitive OpenStack VM Manager (PoC)",
    description="A proof-of-concept REST API for managing OpenStack virtual machines.",
    version="0.1.0",
)

# Allow local development tooling (e.g., Swagger UI in a web browser) to query the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache()
def get_client() -> OpenStackClient:
    """Provide a singleton client for the duration of the server process."""

    return get_openstack_client(settings.openstack_backend)


@app.get("/healthz", tags=["Health"])
def health_check() -> dict:
    """Basic health check endpoint."""

    return {"status": "ok"}


@app.get("/v1/vms", response_model=list[VMInstance], tags=["VMs"])
def list_vms(client=Depends(get_client)) -> list[VMInstance]:
    return client.list_vms()


@app.get("/v1/vms/{vm_id}", response_model=VMInstance, tags=["VMs"])
def get_vm(vm_id: str, client=Depends(get_client)) -> VMInstance:
    try:
        return client.get_vm(vm_id)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="VM not found")


@app.post(
    "/v1/vms",
    response_model=VMInstance,
    status_code=status.HTTP_201_CREATED,
    tags=["VMs"],
)
def create_vm(request: VMCreateRequest, client=Depends(get_client)) -> VMInstance:
    return client.create_vm(request)


@app.delete("/v1/vms/{vm_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["VMs"])
def delete_vm(vm_id: str, client=Depends(get_client)) -> None:
    try:
        client.delete_vm(vm_id)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="VM not found")


@app.post("/v1/vms/{vm_id}/actions", response_model=VMInstance, tags=["VMs"])
def vm_action(vm_id: str, request: VMActionRequest, client=Depends(get_client)) -> VMInstance:
    try:
        if request.action == "start":
            return client.start_vm(vm_id)
        if request.action == "stop":
            return client.stop_vm(vm_id)
        if request.action == "reboot":
            return client.reboot_vm(vm_id)

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported action")
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="VM not found")
