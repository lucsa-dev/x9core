from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict

from x9core.infrastructure.config import Settings, get_settings


def _isolated_settings(**kwargs: object) -> Settings:
    class IsolatedSettings(Settings):
        model_config = SettingsConfigDict(env_file=None, extra="ignore")

        @classmethod
        def settings_customise_sources(
            cls,
            settings_cls: type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
        ) -> tuple[PydanticBaseSettingsSource, ...]:
            return (init_settings,)

    return IsolatedSettings(**kwargs)  # type: ignore[arg-type]


def test_settings_defaults() -> None:
    settings = _isolated_settings()
    assert settings.app_name == "x9core"
    assert settings.app_env == "development"
    assert settings.is_development is True
    assert settings.debug is False


def test_settings_test_env() -> None:
    settings = _isolated_settings(app_env="test")
    assert settings.is_development is False


def test_get_settings_returns_settings_instance() -> None:
    settings = get_settings()
    assert isinstance(settings, Settings)
