success_flow_pipeline = [
    "app.libs.app_loader.tests.middleware_fixtures:FixtureTestMiddleware",
    "app.libs.app_loader.tests.middleware_fixtures:FixtureTestResultAfterTestMiddleware",
]

broken_pipeline = ["app.libs.app_loader.tests.middleware_fixtures:FixtureWrongSubclassMiddleware"]

skip_pipeline = [
    "app.libs.app_loader.tests.middleware_fixtures:FixtureTestMiddleware",
    "app.libs.app_loader.tests.middleware_fixtures:SkippableLoaderMethodMiddleware",
    "app.libs.app_loader.tests.middleware_fixtures:FixtureTestResultAfterTestMiddleware",
]

not_implemented_method_pipeline = [
    "app.libs.app_loader.tests.middleware_fixtures:NotImplementLoadMethodMiddleware",
]
