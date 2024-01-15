from asgi_lifespan import LifespanManager
from asyncclick import Context
from fastapi import FastAPI
import typing as t
from app.libs.click_cli.base import MultiCommandBase
import asyncclick as click


pass_fast_api = click.make_pass_decorator(FastAPI)


class FastAPICli(MultiCommandBase):

    def __init__(self, import_modules: list[str], fast_api: FastAPI, *args, **attrs) -> None:
        """
        Args:
            import_modules (list): object that helps to auto discover applications deps.
            *args:
            **attrs:
        """

        super().__init__(*args, **attrs)
        self.fast_api = fast_api
        self.import_modules = import_modules

    async def make_context(
        self,
        info_name: t.Optional[str],
        args: t.List[str],
        parent: t.Optional[Context] = None,
        **extra: t.Any,
    ) -> Context:
        context = await super().make_context(info_name, args, parent, **extra)
        context.obj = self.fast_api

        return context

    async def invoke(self, ctx: Context) -> t.Any:
        """Invoke command with triggering lifespan events for fast-api object
        Args:
            ctx (Context): click context object

        Returns:
            Any: command response
        """
        fastapi_obj = ctx.find_object(FastAPI)
        async with LifespanManager(fastapi_obj) as manager:
            ctx.obj = manager
            rv = await super().invoke(ctx)
        return rv

    def main(
        self,
        *args,
        **kwargs
    ) -> t.Any:
        """Modified main method, starts when creating an object of FastCli class, and call __call__ method
        Examples:
            ```
            fast_api_cli = FastApiCli()
            if __name__ == "__main__":
                fast_api_cli() # Will trigger __call__() after that will call main() method

            ```
        Args:
            *args:
            **kwargs:

        Returns:

        """
        self.load_commands(self.import_modules)
        return super().main(
            *args,
            **kwargs
        )
