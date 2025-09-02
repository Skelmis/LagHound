from datetime import timedelta
from enum import Enum
from pathlib import Path
from time import sleep
from typing import Literal, Annotated

import click
import typer
from humanize import naturaldelta
from rich.progress import SpinnerColumn, Progress, TextColumn
from termcolor import colored

app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)


class ModeChoices(str, Enum):
    discovery = "Discovery"
    exploitation = "Exploitation"


def print_banner(
    *,
    mode: Literal["Discovery", "Exploitation", "Unknown"] = "Unknown",
    expected_runtime: timedelta | float = None,
):
    print(colored("LagHound", "green", "on_black", attrs=["underline"]))
    print(
        colored(
            "A tool for automating the discovery and exploitation of time based user enumeration.",
        )
    )
    print(
        "Current runtime mode: ",
        colored(
            mode,
            "yellow",
        ),
        sep="",
    )
    if expected_runtime is not None:
        print(
            "Expected program runtime: ",
            colored(
                "Roughly " + naturaldelta(expected_runtime),
                "blue",
            ),
            sep="",
        )


@app.command()
def discover(
    fake_user: Annotated[
        str,
        typer.Option(
            "--fake",
            "--fake-user",
            help="A known fake user on the application.",
            rich_help_panel="Required Data",
            prompt=True,
        ),
    ],
    real_user: Annotated[
        str,
        typer.Option(
            "--real",
            "--real-user",
            help="A known real user on the application.",
            rich_help_panel="Required Data",
            prompt=True,
        ),
    ],
    request_file: Annotated[
        Path,
        typer.Option(
            "--file",
            "--request-file",
            help="The path to a file the HTTP request to make",
            rich_help_panel="Required Data",
            prompt="Please provide the path to your file containing the HTTP request",
        ),
    ],
    time_between_requests: Annotated[
        float,
        typer.Option(
            help="How many seconds to wait between requests. "
            "Unless you have a specific reason, the default is recommended.",
            rich_help_panel="Optional Data",
        ),
    ] = 5,
    total_request_per_user: Annotated[
        float,
        typer.Option(
            help="How requests to make per user to gather timing data. "
            "Unless you have a specific reason, the default is recommended.",
            rich_help_panel="Optional Data",
        ),
    ] = 5,
    string_to_replace_with_users: Annotated[
        str,
        typer.Option(
            help="The string present within the HTTP request which LagHound will put the provided users into",
            rich_help_panel="Optional Data",
        ),
    ] = "$USER",
):
    """Runs discovery against the target and confirms if enumeration is possible.

    This command will answer with whether or not enumeration is present
    based on the provided initial arguments.
    """
    print_banner(
        mode="Discovery",
        expected_runtime=timedelta(
            seconds=(time_between_requests * total_request_per_user) * 2
        ),
    )
    if not request_file.exists():
        ctx = click.get_current_context()
        ctx.fail(
            "The file provided in --request-file does not exist. Please try again."
        )

    main()


@app.command()
def exploit(
    time_between_requests: Annotated[
        float,
        typer.Option(
            help="How many seconds to wait between requests. "
            "Unless you have a specific reason, the default is recommended.",
        ),
    ] = 5,
):
    """Given a list of plausible users, confirm whether or not they
    are real users within the application.

    We recommend running discover first in order to confirm exploitation is possible.
    """
    print_banner(
        mode="Discovery",
        expected_runtime=timedelta(seconds=1, minutes=10),
    )
    main()


def main():
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        t_1 = progress.add_task(description="Processing...", total=None)
        sleep(5)
        progress.remove_task(t_1)
        progress.add_task(description="Preparing...", total=None)
        sleep(10)


if __name__ == "__main__":
    app(prog_name="laghound")
