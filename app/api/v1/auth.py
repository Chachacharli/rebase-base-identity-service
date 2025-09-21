from uuid import uuid4

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from app.core.db import get_session
from app.core.store import save_authorization_code
from app.repositories.client_application_repository import ClientApplicationRepository
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()


# GET: mostrar login
@router.get("/authorize")
def authorize_get(
    request: Request,
    response_type: str,
    client_id: str,
    redirect_uri: str,
    scope: str,
    state: str,
    code_challenge: str,
    code_challenge_method: str = "S256",
    session: Session = Depends(get_session),
):
    repository = ClientApplicationRepository(session)
    client = repository.get_by_client_id(client_id)
    if not client:
        raise HTTPException(status_code=400, detail="Invalid client_id")
    if redirect_uri not in client.redirect_uris:
        raise HTTPException(status_code=400, detail="Invalid redirect_uri")

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "state": state,
            "scope": scope,
            "code_challenge": code_challenge,
            "code_challenge_method": code_challenge_method,
            "error": None,  # sin error al inicio
        },
    )


# POST: procesar login y generar authorization code
@router.post("/authorize")
def authorize_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    client_id: str = Form(...),
    redirect_uri: str = Form(...),
    state: str = Form(...),
    scope: str = Form(...),
    code_challenge: str = Form(...),
    code_challenge_method: str = Form(...),
    session: Session = Depends(get_session),
):
    repo = UserRepository(session)
    service = UserService(repo)
    user = service.authenticate_user(username, password)

    if not user:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "state": state,
                "scope": scope,
                "code_challenge": code_challenge,
                "code_challenge_method": code_challenge_method,
                "error": "Usuario o contraseña incorrectos",
            },
        )

    # Generar authorization code (asociado al user_id)
    auth_code = str(uuid4())
    save_authorization_code(auth_code, client_id, redirect_uri, code_challenge, user.id)

    # Redirigir con code + state
    redirect_url = f"{redirect_uri}?code={auth_code}&state={state}"
    return RedirectResponse(redirect_url, status_code=302)
