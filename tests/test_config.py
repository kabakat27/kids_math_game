import pytest

from backend.config import (
    DevelopmentConfig,
    ProductionConfig,
    StagingConfig,
    TestingConfig,
    get_config,
)


def test_default_config_is_development(monkeypatch):
    monkeypatch.delenv("FLASK_ENV", raising=False)
    config = get_config()
    assert isinstance(config, DevelopmentConfig)
    assert config.ENV == "development"
    assert config.DEBUG is True


@pytest.mark.parametrize(
    "env, expected_class, expected_env",
    [
        ("development", DevelopmentConfig, "development"),
        ("dev", DevelopmentConfig, "development"),
        ("staging", StagingConfig, "staging"),
        ("production", ProductionConfig, "production"),
        ("prod", ProductionConfig, "production"),
        ("testing", TestingConfig, "testing"),
        ("test", TestingConfig, "testing"),
    ],
)
def test_get_config_aliases(env, expected_class, expected_env):
    config = get_config(env)
    assert isinstance(config, expected_class)
    assert config.ENV == expected_env


def test_config_classes_have_common_attributes():
    for cls in (DevelopmentConfig, StagingConfig, ProductionConfig, TestingConfig):
        config = cls()
        assert hasattr(config, "DEBUG")
        assert hasattr(config, "TESTING")
        assert hasattr(config, "CORS_ORIGINS")
        assert hasattr(config, "ENV")


def test_staging_and_production_cors_defaults():
    staging = StagingConfig()
    production = ProductionConfig()
    assert isinstance(staging.CORS_ORIGINS, list)
    assert isinstance(production.CORS_ORIGINS, list)
