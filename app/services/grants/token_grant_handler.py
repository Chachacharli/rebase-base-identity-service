from typing import Any, Dict, Protocol


class TokenGrantHandler(Protocol):
    def handle(self, form_data: Dict[str, Any]) -> Dict[str, Any]: ...
