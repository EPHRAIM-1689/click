import pytest

import click
from click.parser import _OptionParser
from click.shell_completion import split_arg_string


@pytest.mark.parametrize(
    ("value", "expect"),
    [
        ("cli a b c", ["cli", "a", "b", "c"]),
        ("cli 'my file", ["cli", "my file"]),
        ("cli 'my file'", ["cli", "my file"]),
        ("cli my\\", ["cli", "my"]),
        ("cli my\\ file", ["cli", "my file"]),
    ],
)
def test_split_arg_string(value, expect):
    assert split_arg_string(value) == expect


def test_parser_default_prefixes():
    parser = _OptionParser()
    assert parser._opt_prefixes == {"-", "--"}


def test_parser_collects_prefixes():
    ctx = click.Context(click.Command("test"))
    parser = _OptionParser(ctx)
    click.Option("+p", is_flag=True).add_to_parser(parser, ctx)
    click.Option("!e", is_flag=True).add_to_parser(parser, ctx)
    assert parser._opt_prefixes == {"-", "--", "+", "!"}

@pytest.mark.parametrize("number", ["-1", "-1.5", "-0.5"])
def test_negative_number_as_argument(number):
    @click.command()
    @click.argument("number", type=float)
    def test(number):
        click.echo(f"Number received: {number}")

    result = click.testing.CliRunner().invoke(test, [number])

    assert result.exit_code == 0
    assert f"Number received: {float(number)}" in result.output