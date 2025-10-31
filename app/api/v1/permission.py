from fastapi import APIRouter

router = APIRouter(prefix="/v1/permissions")


@router.get("/")
def list_permissions():
    return {"permissions": []}


@router.post("/")
def create_permission():
    return {"permission": {}}


@router.get("/{permission_id}")
def get_permission(permission_id: str):
    return {"permission": {"id": permission_id}}


@router.put("/{permission_id}")
def update_permission(permission_id: str):
    return {"permission": {"id": permission_id}}


@router.delete("/{permission_id}")
def delete_permission(permission_id: str):
    # soft delete
    return {"deleted": True}
