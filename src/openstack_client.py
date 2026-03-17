"""OpenStack VM lifecycle operations interface.

This module defines a minimal interface for VM lifecycle operations and provides a
lightweight in-memory (mock) implementation that can be used for local development
and proof-of-concept demos.

A production-ready implementation would use `openstacksdk` and map these
operations to the OpenStack Compute API (Nova).
"""

from __future__ import annotations

import uuid
from datetime import datetime
from threading import Lock
from typing import Dict, List, Optional

from .schemas import VMAction, VMCreateRequest, VMInstance, VMStatus


class OpenStackClient:
    """Abstract VM lifecycle interface."""

    def list_vms(self) -> List[VMInstance]:
        raise NotImplementedError

    def get_vm(self, vm_id: str) -> VMInstance:
        raise NotImplementedError

    def create_vm(self, request: VMCreateRequest) -> VMInstance:
        raise NotImplementedError

    def delete_vm(self, vm_id: str) -> None:
        raise NotImplementedError

    def start_vm(self, vm_id: str) -> VMInstance:
        raise NotImplementedError

    def stop_vm(self, vm_id: str) -> VMInstance:
        raise NotImplementedError

    def reboot_vm(self, vm_id: str) -> VMInstance:
        raise NotImplementedError


class MockOpenStackClient(OpenStackClient):
    """A simple in-memory VM store for prototyping."""

    def __init__(self):
        self._store: Dict[str, VMInstance] = {}
        self._lock = Lock()

    def list_vms(self) -> List[VMInstance]:
        with self._lock:
            return list(self._store.values())

    def get_vm(self, vm_id: str) -> VMInstance:
        with self._lock:
            vm = self._store.get(vm_id)
            if not vm:
                raise KeyError(vm_id)
            return vm

    def create_vm(self, request: VMCreateRequest) -> VMInstance:
        now = datetime.utcnow()
        vm_id = str(uuid.uuid4())
        vm = VMInstance(
            id=vm_id,
            name=request.name,
            image=request.image,
            flavor=request.flavor,
            network=request.network,
            status=VMStatus.BUILD,
            created_at=now,
            updated_at=now,
        )
        with self._lock:
            self._store[vm_id] = vm

        # Simulate a transition to ACTIVE state.
        return self._transition(vm_id, VMStatus.ACTIVE)

    def delete_vm(self, vm_id: str) -> None:
        with self._lock:
            if vm_id not in self._store:
                raise KeyError(vm_id)
            del self._store[vm_id]

    def start_vm(self, vm_id: str) -> VMInstance:
        return self._transition(vm_id, VMStatus.ACTIVE)

    def stop_vm(self, vm_id: str) -> VMInstance:
        return self._transition(vm_id, VMStatus.STOPPED)

    def reboot_vm(self, vm_id: str) -> VMInstance:
        vm = self._transition(vm_id, VMStatus.STOPPED)
        return self._transition(vm.id, VMStatus.ACTIVE)

    def _transition(self, vm_id: str, status: VMStatus) -> VMInstance:
        with self._lock:
            if vm_id not in self._store:
                raise KeyError(vm_id)
            vm = self._store[vm_id]
            updated = vm.copy(update={"status": status, "updated_at": datetime.utcnow()})
            self._store[vm_id] = updated
            return updated


def get_openstack_client(backend: str = "mock") -> OpenStackClient:
    # Future: choose a real OpenStack-backed implementation based on the backend.
    if backend == "mock":
        return MockOpenStackClient()
    raise ValueError(f"Unknown openstack_backend: {backend}")
