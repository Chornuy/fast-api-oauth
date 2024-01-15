import pytest

from app.libs.app_loader.middlewares.beanie import BeanieModelLoader
from app.libs.app_loader.middlewares.tests.fixture_beanie.app_a.models import (
    Bike,
    Car,
    Metrics,
    One,
    Owner,
    Parent,
    Two,
    Vehicle,
)


class TestBeanieLoader:
    @staticmethod
    def get_expected_models():
        return [
            Bike.__name__,
            Car.__name__,
            Metrics.__name__,
            One.__name__,
            Owner.__name__,
            Parent.__name__,
            Two.__name__,
            Vehicle.__name__,
        ]

    @staticmethod
    def get_fixture_config_for_app_a():
        return {
            "apps": {
                "app_a": {"module_path": "app.libs.app_loader.middlewares.tests.fixture_beanie.app_a"},
            }
        }

    @staticmethod
    def get_fixture_config_for_app_b():
        return {
            "apps": {
                "app_b": {"module_path": "app.libs.app_loader.middlewares.tests.fixture_beanie.app_b"},
            }
        }

    @staticmethod
    def get_fixture_config_for_app_c():
        return {
            "apps": {
                "app_b": {"module_path": "app.libs.app_loader.middlewares.tests.fixture_beanie.app_c"},
            }
        }

    @pytest.fixture
    def beanie_loader(self):
        return BeanieModelLoader()

    def test_beanie_loader_app_a(self, beanie_loader: BeanieModelLoader) -> None:
        context = beanie_loader.load(context=self.get_fixture_config_for_app_a(), config={})
        assert "beanie_models" in context.keys()
        assert context["beanie_models"]

        expected_models_name = self.get_expected_models()
        for model_cls in context["beanie_models"]:
            assert model_cls.__name__ in expected_models_name

    def test_beanie_loader_app_b(self, beanie_loader: BeanieModelLoader) -> None:
        context = beanie_loader.load(context=self.get_fixture_config_for_app_b(), config={})
        assert "beanie_models" in context.keys()
        assert context["beanie_models"]

        expected_models_name = self.get_expected_models()
        for model_cls in context["beanie_models"]:
            assert model_cls.__name__ in expected_models_name

    def test_beanie_loader_app_c(self, beanie_loader: BeanieModelLoader) -> None:
        context = beanie_loader.load(context=self.get_fixture_config_for_app_c(), config={})
        assert "beanie_models" in context.keys()
        assert context["beanie_models"] == []
