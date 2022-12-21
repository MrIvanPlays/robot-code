#!/usr/bin/env python3

from typing import Optional

import typer
import time

from robot import __version__
from robot import robot as controls

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"robot controller v{__version__}")
        raise typer.Exit()


@app.command()
def control(
        duty_cycle: int = typer.Option(
            100,
            "--duty-cycle",
            help="Change the duty cycle of the application. Should be between 0 and 100 (0 and 100 included)"
        ),
        vreme: int = typer.Option(
            3,
            "--time",
            help="For how much time should the robot do the move you need. Measured in seconds"
        ),
        movement: str = typer.Option(
            "forward",
            "--movement",
            help="Movement type. Available types: forward, backward, right, left, parallel_right, parallel_left"
        )
) -> None:
    if duty_cycle < 0 or duty_cycle > 100:
        typer.echo("Error: duty cycle should be between 0 and 100 (0 and 100 included)")
        raise typer.Exit(1)

    if movement == "backward":
        typer.echo(f"Initializing backwards movement for {vreme} seconds with duty cycle of {duty_cycle}")
        controls.backward(duty_cycle)
        time.sleep(vreme)
        controls.cleanup()
        raise typer.Exit()
    elif movement == "forward":
        typer.echo(f"Initializing forwards movement for {vreme} seconds with duty cycle of {duty_cycle}")
        controls.forward(duty_cycle)
        time.sleep(vreme)
        controls.cleanup()
        raise typer.Exit()
    elif movement == "right":
        typer.echo(f"Initializing right turn for {vreme} seconds with duty cycle of {duty_cycle}")
        controls.right(duty_cycle)
        time.sleep(vreme)
        controls.cleanup()
        raise typer.Exit()
    elif movement == "left":
        typer.echo(f"Initializing left turn for {vreme} seconds with duty cycle of {duty_cycle}")
        controls.left(duty_cycle)
        time.sleep(vreme)
        controls.cleanup()
        raise typer.Exit()
    elif movement == "parallel_left":
        typer.echo(f"Initializing parallel left turn for {vreme} seconds with duty cycle of {duty_cycle}")
        controls.parallel_left(duty_cycle)
        time.sleep(vreme)
        controls.cleanup()
        raise typer.Exit()
    elif movement == "parallel_right":
        typer.echo(f"Initializing parallel right tun for {vreme} seconds with duty cycle of {duty_cycle}")
        controls.parallel_right(duty_cycle)
        time.sleep(vreme)
        controls.cleanup()
        raise typer.Exit()
    else:
        typer.echo("Error: Invalid movement type.")
        raise typer.Exit(1)


@app.command
def cleanup(

) -> None:
    controls.cleanup()
    raise typer.Exit()

@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application's version and exit",
            callback=_version_callback,
            is_eager=True
        )
) -> None:
    return
