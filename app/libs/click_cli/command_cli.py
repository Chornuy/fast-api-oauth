import typing as t

import asyncclick as click
from asyncclick import Command
from asyncclick.core import Context
from fastapi import FastAPI
from asgi_lifespan import LifespanManager

from app.libs.app_loader.bootstrap import ApplicationBootStrap
from app.libs.utils.managment import get_fast_api_app
from app.utils.module_loading import cached_import_module

pass_fast_api = click.make_pass_decorator(FastAPI)


class FastApiCli(click.MultiCommand):

    commands = {}

    command_class: t.Optional[t.Type[Command]] = None

    def __init__(self, bootstrap: ApplicationBootStrap, *args, **attrs):
        """Overriding init for injecting helper object of ApplicationBootStrap class.
        ApplicationBootStrap, helps to autodiscover modules with possible commands list.

        Args:
            bootstrap (ApplicationBootStrap): object that helps to auto discover applications deps.
            *args:
            **attrs:
        """

        super().__init__(*args, **attrs)
        self.bootstrap = bootstrap

    async def make_context(
        self,
        info_name: t.Optional[str],
        args: t.List[str],
        parent: t.Optional[Context] = None,
        **extra: t.Any,
    ) -> Context:
        context = await super().make_context(info_name, args, parent, **extra)
        context.obj = get_fast_api_app()

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

    @staticmethod
    def load_commands(command_modules: list[str]) -> None:
        """Load commands by importing modules that register command to

        Args:
            command_modules:

        Returns:

        """
        for command_module in command_modules:
            cached_import_module(command_module)

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
        self.load_commands(self.bootstrap.context["commands_modules"])
        return super().main(
            *args,
            **kwargs
        )
