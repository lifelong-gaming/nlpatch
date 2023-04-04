from ...settings import GlobalSettings
from ..settings import BaseAuthProviderSettings


class FirebaseAuthProviderSettings(BaseAuthProviderSettings):
    firebase_credentials: str

    @classmethod
    def from_global_settings(cls, settings: GlobalSettings) -> "FirebaseAuthProviderSettings":
        return cls(firebase_credentials=settings.auth_provider_settings["firebase_credentials"])
