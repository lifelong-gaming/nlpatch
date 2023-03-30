from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import GlobalSettings
from .auth_providers.factories import create_auth_provider

def generate_app(settings: GlobalSettings) -> FastAPI:
   app = FastAPI()
   auth_provider = create_auth_provider(settings=settings)

   app.add_middleware(
      CORSMiddleware,
      allow_origins=settings.origins,
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
   )

   @app.get("/api/")
   async def hello():
      return {"msg":"Hello, this is API server"} 


   @app.get("/api/user/me")
   async def user_me(user = Depends(auth_provider.get_user_token)):
      return {"id":user['uid']} 

   return app
