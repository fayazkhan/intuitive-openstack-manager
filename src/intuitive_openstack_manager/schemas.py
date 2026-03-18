from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class VMStatus(str, Enum):
    BUILD = "build"
    ACTIVE = "active"
    STOPPED = "stopped"
    DELETED = "deleted"


class VMCreateRequest(BaseModel):
    id: str = Field(..., description="Client-supplied unique VM identifier (for idempotency)")
    name: str = Field(..., description="Human-friendly name for the VM")
    image: str = Field(..., description="Image name or ID to boot from")
    flavor: str = Field(..., description="Flavor name or ID to use for sizing")
    network: Optional[str] = Field(None, description="Optional network ID to attach")


class VMAction(str, Enum):
    START = "start"
    STOP = "stop"
    REBOOT = "reboot"


class VMActionRequest(BaseModel):
    action: VMAction = Field(..., description="Lifecycle action to perform on the VM")


class VMInstance(BaseModel):
    id: str = Field(..., description="Unique VM identifier")
    name: str
    image: str
    flavor: str
    network: Optional[str] = None
    status: VMStatus
    created_at: datetime
    updated_at: datetime
