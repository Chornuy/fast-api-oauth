import typing as t

import asyncclick as click
from asyncclick import Command
from asyncclick.core import _check_multicommand, Context

from app.utils.module_loading import cached_import_module


class MultiCommandBase(click.MultiCommand):

    commands = {}

    command_class: t.Optional[t.Type[Command]] = None

    @staticmethod
    def load_commands(command_modules: list[str]) -> None:
        """Load commands by importing modules that register command to

        Args:
            command_modules:

        Returns:

        """
        for command_module in command_modules:
            cached_import_module(command_module)

    def add_command(self, cmd: Command, name: t.Optional[str] = None) -> None:
        """Registers another :class:`Command` with this group.  If the name
        is not provided, the name of the command is used.
        """
        name = name or cmd.name
        if name is None:
            raise TypeError("Command has no name.")
        _check_multicommand(self, name, cmd, register=True)
        self.commands[name] = cmd

    def command(
        self, *args, **kwargs
    ) -> t.Callable:
        """Logic was taken from Group class of click library. Helps to register commands inside FastCli class

        Args:
            *args:
            **kwargs:

        Returns:
            Callable: decorator that register command
        """
        from asyncclick import command
        if self.command_class and kwargs.get("cls") is None:
            kwargs["cls"] = self.command_class

        func: t.Optional[t.Callable] = None

        if args and callable(args[0]):
            assert (
                len(args) == 1 and not kwargs
            ), "Use 'command(**kwargs)(callable)' to provide arguments."
            (func,) = args
            args = ()

        def decorator(f: t.Callable[..., t.Any]) -> Command:
            cmd: Command = command(*args, **kwargs)(f)
            self.add_command(cmd)
            return cmd

        if func is not None:
            return decorator(func)

        return decorator

    def get_command(self, ctx: Context, name: str) -> Command | None:
        """ Method get command that was registered by decorator

        Args:
            ctx (Context): click context object
            name (str): name of the command

        Returns:
            Command: command object of click
        """
        try:
            return self.commands[name]
        except KeyError:
            return None

    def list_commands(self, ctx: Context) -> t.List[str]:
        """ Return a list of commands, after importing all modules that contains commands decorator

        Args:
            ctx (Context):

        Returns:
            list[str]: list of commands name
        """
        return sorted(self.commands.keys())
