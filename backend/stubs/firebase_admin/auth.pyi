from typing import Any, Dict, Optional

from firebase_admin import App

def verify_id_token(id_token: str, app: Optional[App] = None) -> Dict[str, Any]: ...
