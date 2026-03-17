import pytest

from fastapi.testclient import TestClient

from intuitive_openstack_manager.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_vm_lifecycle_flow(client: TestClient) -> None:
    # Create a new VM
    create_resp = client.post(
        "/v1/vms",
        json={
            "name": "test-vm",
            "image": "ubuntu-22.04",
            "flavor": "small",
            "network": "default",
        },
    )
    assert create_resp.status_code == 201
    vm = create_resp.json()
    assert vm["name"] == "test-vm"
    vm_id = vm["id"]

    # List VMs includes the new VM
    list_resp = client.get("/v1/vms")
    assert list_resp.status_code == 200
    assert any(item["id"] == vm_id for item in list_resp.json())

    # Start/Stop/Reboot actions
    start_resp = client.post("/v1/vms/{}/actions".format(vm_id), json={"action": "start"})
    assert start_resp.status_code == 200
    assert start_resp.json()["status"] == "active"

    stop_resp = client.post("/v1/vms/{}/actions".format(vm_id), json={"action": "stop"})
    assert stop_resp.status_code == 200
    assert stop_resp.json()["status"] == "stopped"

    reboot_resp = client.post("/v1/vms/{}/actions".format(vm_id), json={"action": "reboot"})
    assert reboot_resp.status_code == 200
    assert reboot_resp.json()["status"] == "active"

    # Delete VM
    delete_resp = client.delete(f"/v1/vms/{vm_id}")
    assert delete_resp.status_code == 204

    # After deletion, VM should not be found
    get_resp = client.get(f"/v1/vms/{vm_id}")
    assert get_resp.status_code == 404


def test_invalid_action_returns_400(client: TestClient) -> None:
    # Create a VM to act on
    create_resp = client.post(
        "/v1/vms",
        json={
            "name": "test-vm-2",
            "image": "ubuntu-22.04",
            "flavor": "small",
        },
    )
    vm_id = create_resp.json()["id"]

    invalid_action_resp = client.post(
        f"/v1/vms/{vm_id}/actions", json={"action": "invalid"}
    )
    assert invalid_action_resp.status_code == 422 or invalid_action_resp.status_code == 400
