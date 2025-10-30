from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.db import get_session
from app.repositories.app_settings_repository import AppSettingRepository
from app.schemas.app_settings import AppSettingCreate, AppSettingRead, AppSettingUpdate

router = APIRouter()


# GET: get value of a specific configuration
@router.get("/app-settings/{key}")
def get_app_setting(key: str, session: Session = Depends(get_session)):
    app_setting = AppSettingRepository(session).get(key)
    if not app_setting:
        raise HTTPException(status_code=404, detail="App setting not found")
    # TODO: Convert to AppSettingRead schema
    return AppSettingRead.model_validate(app_setting)


# GET : get all configurations
@router.get("/app-settings/")
def get_all_app_settings(session: Session = Depends(get_session)):
    app_settings = AppSettingRepository(session).get_all()
    # TODO: Convert to list of AppSettingRead schema
    return app_settings


# POST: create a configuration value
@router.post("/app-settings/")
def create_app_setting(
    app_setting: AppSettingCreate,
    session: Session = Depends(get_session),
):
    app_setting = AppSettingRepository(session).set(
        key=app_setting.key,
        value=app_setting.value,
        description=app_setting.description,
    )
    # TODO: Convert to AppSettingRead schema
    return app_setting


# PUT: update a configuration value
@router.put("/app-settings/{key}")
def update_app_setting(
    app_setting_update: AppSettingUpdate,
    session: Session = Depends(get_session),
):
    print(app_setting_update)
    app_setting = AppSettingRepository(session).set(
        key=app_setting_update.key,
        value=app_setting_update.value,
        description=app_setting_update.description,
        is_active=app_setting_update.is_active,
    )
    if not app_setting:
        raise HTTPException(status_code=404, detail="App setting not found")

    # TODO: Convert to AppSettingRead schema
    return app_setting
