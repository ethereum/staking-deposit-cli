import click
from typing import (
    Any,
    Callable,
    Optional,
    Sequence,
    Tuple,
    Union,
)

from staking_deposit.exceptions import ValidationError
from staking_deposit.utils import config


def _value_of(f: Union[Callable[[], Any], Any]) -> Any:
    '''
    If the input, f, is a function, return f(), else return f.
    '''
    return(f() if callable(f) else f)


class JITOption(click.Option):
    '''
    A click.Option, except certain values are recomputed before they are used.
    '''
    def __init__(
        self,
        param_decls: str,
        default: Union[Callable[[], Any], None, Any] = None,
        help: Union[Callable[[], str], str, None] = None,
        prompt: Union[Callable[[], str], str, None] = None,
        **kwargs: Any,
    ):

        self.callable_default = default
        self.callable_help = help
        self.callable_prompt = prompt

        return super().__init__(
            param_decls=[_value_of(param_decls)],
            default=_value_of(default),
            help=_value_of(help),
            prompt=_value_of(prompt),
            **kwargs,
        )

    def prompt_for_value(self, ctx: click.Context) -> Any:
        self.prompt = _value_of(self.callable_prompt)
        return super().prompt_for_value(ctx)

    def get_help_record(self, ctx: click.Context) -> Tuple[str, str]:
        self.help = _value_of(self.callable_help)
        return super().get_help_record(ctx)

    def get_default(self, ctx: click.Context) -> Any:
        self.default = _value_of(self.callable_default)
        return super().get_default(ctx)


def jit_option(*args: Any, **kwargs: Any) -> Callable[[Any], Any]:
    """Attaches an option to the command.  All positional arguments are
    passed as parameter declarations to :class:`Option`; all keyword
    arguments are forwarded unchanged (except ``cls``).
    This is equivalent to creating an :class:`Option` instance manually
    and attaching it to the :attr:`Command.params` list.

    :param cls: the option class to instantiate.  This defaults to
                :class:`Option`.
    """

    def decorator(f: Callable[[Any], Any]) -> Callable[[Any], Any]:
        click.decorators._param_memo(f, JITOption(*args, **kwargs))
        return f

    return decorator


def captive_prompt_callback(
    processing_func: Callable[[str], Any],
    prompt: Callable[[], str],
    confirmation_prompt: Optional[Callable[[], str]]=None,
    confirmation_mismatch_msg: Callable[[], str]=lambda: '',
    hide_input: bool=False,
) -> Callable[[click.Context, str, str], Any]:
    '''
    Traps the user in a prompt until the value chosen is acceptable
    as defined by `processing_func` not returning a ValidationError
    :param processing_func: A function to process the user's input that possibly raises a ValidationError
    :param prompt: the text to prompt the user with, should their input raise an error when passed to processing_func()
    :param confirmation_prompt: the optional prompt for confirming user input (the user must repeat their input)
    :param confirmation_mismatch_msg: the message displayed to the user should their input and confirmation not match
    :param hide_input: bool, hides the input as the user types
    '''
    def callback(ctx: click.Context, param: Any, user_input: str) -> Any:
        if config.non_interactive:
            return processing_func(user_input)
        while True:
            try:
                processed_input = processing_func(user_input)
                # Logic for confirming user input:
                if confirmation_prompt is not None and processed_input != '':
                    confirmation_input = click.prompt(confirmation_prompt(), hide_input=hide_input)
                    if processing_func(confirmation_input) != processed_input:
                        raise ValidationError(confirmation_mismatch_msg())
                return processed_input
            except ValidationError as e:
                click.echo(e)
                user_input = click.prompt(prompt(), hide_input=hide_input)
    return callback


def choice_prompt_func(prompt_func: Callable[[], str], choices: Sequence[str]) -> Callable[[], str]:
    '''
    Formats the prompt and choices in a printable manner.
    '''
    return lambda: '%s %s: ' % (prompt_func(), choices)
