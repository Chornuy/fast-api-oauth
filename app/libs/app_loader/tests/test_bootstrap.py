from pathlib import PosixPath, Path
from typing import Type
from unittest.mock import call

import pytest
from pytest_mock import MockerFixture

from app.libs.app_loader.bootstrap import ApplicationBootStrap
from app.libs.app_loader.middlewares.exceptions import NotInstanceOfBaseMiddleware
from app.libs.app_loader.tests.middleware_fixtures import FixtureTestMiddleware, FixtureTestResultAfterTestMiddleware
from app.libs.app_loader.tests.pipeline_fixutres import success_flow_pipeline, skip_pipeline, broken_pipeline, \
    not_implemented_method_pipeline


def side_effect_first_pipeline(context: dict, config: dict) -> dict:
    context['first_pipeline_result'] = "ok"
    return context


def side_effect_second_pipeline(context: dict, config: dict) -> dict:
    context['side_effect_second_pipeline'] = "ok"
    return context


class BootstrapFixtures:

    @pytest.fixture
    def application_bootstrap_cls(self):
        return ApplicationBootStrap

    @pytest.fixture
    def application_bootstrap_working(
        self, application_bootstrap_cls: Type[ApplicationBootStrap]
    ) -> ApplicationBootStrap:
        return application_bootstrap_cls(base_dir=Path(""), app_dir=Path(""), loader_pipeline=success_flow_pipeline)

    @pytest.fixture()
    def application_loader_with_skip_middleware(
        self, application_bootstrap_cls: Type[ApplicationBootStrap]
    ) -> ApplicationBootStrap:
        return application_bootstrap_cls(base_dir=Path(""), app_dir=Path(""), loader_pipeline=skip_pipeline)

    @pytest.fixture()
    def application_loader_with_error_middleware(
        self, application_bootstrap_cls: Type[ApplicationBootStrap]
    ) -> ApplicationBootStrap:
        return application_bootstrap_cls(base_dir=Path(""), app_dir=Path(""), loader_pipeline=broken_pipeline)

    @pytest.fixture()
    def application_loader_with_not_implemented_middleware(
        self, application_bootstrap_cls: Type[ApplicationBootStrap]
    ) -> ApplicationBootStrap:
        return application_bootstrap_cls(
            base_dir=Path(""), app_dir=Path(""),
            loader_pipeline=not_implemented_method_pipeline
        )


class TestBaseFunctionality(BootstrapFixtures):

    def test_bootstrap_imports(self, application_bootstrap_working: ApplicationBootStrap) -> None:
        expected_classes_name = [
            FixtureTestMiddleware.__name__,
            FixtureTestResultAfterTestMiddleware.__name__
        ]

        application_bootstrap_working.load()

        for middleware in application_bootstrap_working._loader_middlewares:
            assert middleware.__name__ in expected_classes_name

    def test_bootstrap_success_flow(self, application_bootstrap_working: ApplicationBootStrap) -> None:

        assert application_bootstrap_working._state.loaded is False

        application_bootstrap_working.load()

        assert "testing_result" in application_bootstrap_working.context.keys()
        assert application_bootstrap_working.context["testing_result"] == "ok"

        assert "testing_result_another" in application_bootstrap_working.context.keys()
        assert application_bootstrap_working.context["testing_result_another"] == "ok.ok"

        assert application_bootstrap_working._state.loaded is True

    def test_pipeline_order_execution(
        self,
        mocker: MockerFixture,
        application_bootstrap_working: ApplicationBootStrap,
    ):

        first_middleware_mock = mocker.patch(
            'app.core.app_loader.tests.middleware_fixtures.FixtureTestMiddleware.load',
            side_effect=side_effect_first_pipeline
        )

        second_middleware_mock = mocker.patch(
            'app.core.app_loader.tests.middleware_fixtures.FixtureTestResultAfterTestMiddleware.load',
            side_effect=side_effect_second_pipeline
        )

        mock_parent = mocker.Mock()

        mock_parent.attach_mock(first_middleware_mock, "first_pipeline")
        mock_parent.attach_mock(second_middleware_mock, "second_pipeline")
        application_bootstrap_working.load()

        mock_parent.assert_has_calls(
            [
                call.first_pipeline(
                    context=
                    {
                        'bootstrap_config':
                            {
                                'app_dir': PosixPath(''),
                                'base_dir': PosixPath('')
                            },
                        'first_pipeline_result': 'ok',
                        'side_effect_second_pipeline': 'ok'
                    },
                    config={}
                ),
                call.second_pipeline(
                    context={
                        'bootstrap_config': {
                            'app_dir': PosixPath(''),
                            'base_dir': PosixPath('')
                        },
                        'first_pipeline_result': 'ok',
                        'side_effect_second_pipeline': 'ok'
                    },
                    config={}
                )
            ]
        )

    def test_ensure(self, application_bootstrap_working: ApplicationBootStrap):
        assert not application_bootstrap_working.is_loaded()
        assert not application_bootstrap_working._context

        assert application_bootstrap_working.context["testing_result_another"] == "ok.ok"
        assert application_bootstrap_working._state.loaded is True

    def test_wrong_subclass(self, application_loader_with_error_middleware: ApplicationBootStrap):
        with pytest.raises(NotInstanceOfBaseMiddleware):
            application_loader_with_error_middleware.load()

    def test_not_implemented(self, application_loader_with_not_implemented_middleware: ApplicationBootStrap):
        with pytest.raises(NotImplementedError):
            application_loader_with_not_implemented_middleware.load()

    def test_skippable_pipeline(self, application_loader_with_skip_middleware: ApplicationBootStrap):
        application_loader_with_skip_middleware.load()
        assert "testing_result" in application_loader_with_skip_middleware.context.keys()
        assert application_loader_with_skip_middleware.context["testing_result"] == "ok"

        assert "testing_result_another" in application_loader_with_skip_middleware.context.keys()
        assert application_loader_with_skip_middleware.context["testing_result_another"] == "ok.ok"

