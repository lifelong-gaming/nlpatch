from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth_providers.factories import create_auth_provider
from .routers.dialogue_router import generate_dialogue_router
from .routers.model_router import generate_model_router
from .settings import GlobalSettings
from .storages.factories import create_storage
from .types import User


def generate_app(settings: GlobalSettings) -> FastAPI:
    app = FastAPI()
    auth_provider = create_auth_provider(settings=settings)
    storage = create_storage(settings=settings)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/v1/user/me", response_model=User)
    async def user_me(user: User = Depends(auth_provider.get_user_token)) -> User:
        return user

    app.include_router(generate_model_router(auth_provider=auth_provider, storage=storage), prefix="/api/v1/models")
    app.include_router(
        generate_dialogue_router(auth_provider=auth_provider, storage=storage), prefix="/api/v1/dialogues"
    )

    return app
