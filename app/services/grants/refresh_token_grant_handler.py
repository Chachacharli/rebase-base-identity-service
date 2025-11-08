from app.domain.tokens.token_response import FormTokenRequest, GrantTokenResponse
from app.exceptions.bussiness_exceptions import TokenExpiredException
from app.services.grants.token_grant_handler import TokenGrantHandler
from app.services.token_service import TokenService


class RefreshTokenGrantHandler(TokenGrantHandler):
    def handle(self, form_data: FormTokenRequest) -> GrantTokenResponse:
        token_service = TokenService(self.session)

        try:
            token_pair = token_service.refresh_with_rotation(
                refresh_token_str=form_data.refresh_token, client_id=form_data.client_id
            )
        except ValueError as e:
            raise TokenExpiredException(
                details={
                    "error": "invalid_grant",
                    "error_description": str(e.args[0]),
                }
            )

        # Aquí podrías regenerar el ID token (opcional)
        return GrantTokenResponse(
            access_token=token_pair.access_token,
            token_type="bearer",
            expires_in=token_pair.expires_in,
            id_token="",  # opcional si no se requiere renovar
            refresh_token=token_pair.refresh_token,
            scope="",
            user_id="",
            client_id=form_data.client_id,
        )
