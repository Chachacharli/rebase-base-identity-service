# REBASE BASE IDENTITY SERVICE

Este proyecto consiste en el desarrollo de un **Identity Provider (IdP)** propio que actuará como el **servicio central de autenticación y autorización** para una suite de aplicaciones multi-tenant. El sistema estará basado en los estándares modernos de identidad, principalmente **OAuth 2.0** y **OpenID Connect (OIDC)**, con soporte de **PKCE (Proof Key for Code Exchange)** para mayor seguridad en aplicaciones públicas (ej. SPAs, móviles).


## To run the app:
```bash
typer cli.py run
```

or 
```bash
fastapi dev app/main.py
```

## Upgrade requirements:
```bash
pip freeze > requirements.txt
```

## Download requirements:
```bash
pip install -r requirements.txt
```
