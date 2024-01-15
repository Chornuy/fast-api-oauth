
success_flow_pipeline = [
    "app.core.app_loader.tests.middleware_fixtures:FixtureTestMiddleware",
    "app.core.app_loader.tests.middleware_fixtures:FixtureTestResultAfterTestMiddleware"
]

broken_pipeline = [
    "app.core.app_loader.tests.middleware_fixtures:FixtureWrongSubclassMiddleware"
]

skip_pipeline = [
    "app.core.app_loader.tests.middleware_fixtures:FixtureTestMiddleware",
    "app.core.app_loader.tests.middleware_fixtures:SkippableLoaderMethodMiddleware",
    "app.core.app_loader.tests.middleware_fixtures:FixtureTestResultAfterTestMiddleware"
]

not_implemented_method_pipeline = [
    "app.core.app_loader.tests.middleware_fixtures:NotImplementLoadMethodMiddleware",
]

