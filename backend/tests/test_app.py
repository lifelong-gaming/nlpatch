from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from nlpatch.app import generate_app
from nlpatch.settings import GlobalSettings


def test_generate_app(mocker: MockerFixture) -> None:
    FastAPI = mocker.patch("nlpatch.app.FastAPI")
    create_auth_provider = mocker.patch("nlpatch.app.create_auth_provider")
    create_storage = mocker.patch("nlpatch.app.create_storage")
    generate_model_router = mocker.patch("nlpatch.app.generate_model_router")
    settings = MagicMock(spec=GlobalSettings).return_value
    actual = generate_app(settings=settings)
    assert actual == FastAPI.return_value
    FastAPI.assert_called_once_with()
    create_auth_provider.assert_called_once_with(settings=settings)
    create_storage.assert_called_once_with(settings=settings)
    generate_model_router.assert_called_once_with(
        auth_provider=create_auth_provider.return_value, storage=create_storage.return_value
    )
    FastAPI.return_value.add_middleware.assert_called_once_with(
        mocker.ANY, allow_origins=settings.origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
    )
