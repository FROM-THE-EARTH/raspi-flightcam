import typing as t

import click
import pigpio
from pisat.handler import PigpioDigitalInputHandler

from .recorder import (
    GPIOPins,
    IORecorder,
    isvalid_video_format,
)


def validate_fname(
    ctx: click.Context,
    param: str,
    value: t.Optional[str],
) -> t.Optional[str]:
    if value is None or isvalid_video_format(value):
        return value
    raise click.BadParameter(f"'{value}' has an invalid extension.")


def validate_interval(
    ctx: click.Context,
    param: str,
    value: float,
) -> float:
    if value > 0:
        return value
    raise click.BadParameter(
        "Parameter 'interval' must be a positive number."
    )


def validate_pin(
    ctx: click.Context,
    param: str,
    value: int,
) -> int:
    if value in GPIOPins:
        return value
    raise click.BadParameter(
        "Parameter 'pin' must be an integer of "
        f"{GPIOPins.GPIO_MIN} ~ {GPIOPins.GPIO_MAX}."
    )


def validate_resolution(
    ctx: click.Context,
    param: str,
    value: str,
) -> t.Tuple[int, int]:
    value = value.split(":")
    if len(value) != 2:
        raise click.BadParameter(
            ""
        )

    try:
        width, height = int(value[0]), int(value[1])
    except ValueError as e:
        raise click.BadParameter() from e
    else:
        return (width, height)


def validate_timeout(
    ctx: click.Context,
    param: str,
    value: t.Optional[str],
) -> float:
    if value is None:
        return -1.

    timesum = 0
    temp = []
    for char in value:
        if str.isnumeric(char) or char == ".":
            temp.append(char)
            continue

        alpha = str.lower(char)
        num = float("".join(temp))
        temp.clear()

        if alpha == "h":
            timesum += num * 3600
        elif alpha == "m":
            timesum += num * 60
        elif alpha == "s":
            timesum += num
        else:
            raise click.BadParameter(f"'{value}' has an invalid time format.")
    if len(temp):
        timesum += float("".join(temp))

    return timesum


@click.group()
def main() -> None:
    pass


@main.command()
@click.argument(
    "pin",
    type=int,
    callback=validate_pin,
)
@click.option(
    "-f",
    "--fname",
    callback=validate_fname,
)
@click.option(
    "-i",
    "--interval",
    type=float,
    default=1.,
    show_default=True,
    callback=validate_interval,
)
@click.option(
    "-r",
    "--resolution",
    default="640:480",
    show_default=True,
    callback=validate_resolution,
)
@click.option(
    "--start-with-low",
    is_flag=True,
    default=False,
    show_default=True,
)
@click.option(
    "-t",
    "--timeout",
    callback=validate_timeout,
)
def iorec(
    pin: int,
    fname: t.Optional[str],
    interval: float,
    resolution: t.Tuple[int, int],
    start_with_low: bool,
    timeout: float,

) -> None:
    pi = pigpio.pi()
    handler = PigpioDigitalInputHandler(pi, pin, pulldown=True)
    recorder = IORecorder(handler, fname=fname, resolution=resolution)
    recorder.start_record(
        interval=interval,
        timeout=timeout,
        start_with_low=start_with_low,
    )
