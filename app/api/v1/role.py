from uuid import UUID

from fastapi import APIRouter

router = APIRouter(prefix="/v1/roles")


@router.get("/")
def list_roles():
    return {"roles": []}


@router.post("/")
def create_role():
    return {"role": {}}


@router.get("/{role_id}")
def get_role(role_id: UUID):
    return {"role": {"id": role_id}}


@router.put("/{role_id}")
def update_role(role_id: UUID):
    return {"role": {"id": role_id}}


@router.delete("/{role_id}")
def delete_role(role_id: UUID):
    # soft delete
    return {"deleted": True}


@router.post("/{role_id}/set_permissions")
def set_role_permissions(role_id: UUID):
    return {"role": {"id": role_id, "permissions_set": True}}


@router.post("/{role_id}/set_permission")
def set_role_permission(role_id: UUID):
    return {"role": {"id": role_id, "permission_set": True}}


@router.put("/{role_id}/remove_permission")
def remove_role_permission(role_id: UUID):
    return {"role": {"id": role_id, "permission_removed": True}}


@router.put("/{role_id}/remove_permissions")
def remove_role_permissions(role_id: UUID):
    return {"role": {"id": role_id, "permissions_removed": True}}
