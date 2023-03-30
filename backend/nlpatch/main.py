from .app import generate_app
from .settings import GlobalSettings

settings = GlobalSettings()

app = generate_app(settings=settings)