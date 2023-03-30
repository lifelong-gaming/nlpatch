from .base import BaseAuthProvider
from .firebase import FirebaseAuthProvider, FirebaseAuthProviderSettings
from ..settings import GlobalSettings, AuthProviderType


def create_auth_provider(settings: GlobalSettings) -> BaseAuthProvider:
    if settings.auth_provider == AuthProviderType.FIREBASE:
        return FirebaseAuthProvider(settings=FirebaseAuthProviderSettings.from_global_settings(settings))
    raise ValueError(f"Unknown auth provider type: {settings.auth_provider}")
