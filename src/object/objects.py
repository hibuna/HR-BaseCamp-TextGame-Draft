import enum
from typing import TYPE_CHECKING

from src.object.base import Object
from src.enums import PlayerAction

if TYPE_CHECKING:
    from src.object.base import Item


class Well(Object):
    class States(enum.Enum):
        EMPTY = enum.auto()
        FULL = enum.auto()

    name = "well"
    description = "A deep cobblestone well."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.FILL,
        PlayerAction.EMPTY,
        PlayerAction.ENTER,
    ]
    _references = ["water well"]
    state = States.EMPTY

    fills_until_full = 3


class PrologueControlPanel(Object):
    name = "control panel"
    description = "A control panel with a lot of buttons. A symbol of a flame flashes on the screen. Next to it is a red button."
    interactions = [
        PlayerAction.INSPECT,
    ]
    _references = ["control panel", "panel"]
    state = None
    shown = True


class PrologueControlPanelButton(Object):
    name = "red button"
    description = "A red button."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.HIT,
        PlayerAction.USE,
        PlayerAction.PRESS,
    ]
    _references = ["red button", "button"]
    state = None
    shown = False


class ControlPanel(Object):
    name = "control panel"
    description = "A control panel with a lot of buttons."
    interactions = [
        PlayerAction.INSPECT,
    ]
    _references = ["control panel", "panel"]
    state = None
    shown = True


class HeavyDoor(Object):
    name = "heavy door"
    description = "A heavy door."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.OPEN,
    ]
    _references = ["heavy door"]
    state = None
    shown = True


class HeavyDoorWheel(Object):
    class States:
        OPEN = enum.auto()
        CLOSED = enum.auto()

    name = "heavy door wheel"
    description = "A solid metal wheel is attached to the door."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.TURN,
    ]
    _references = ["wheel", "heavy door wheel"]
    state = States.CLOSED
    shown = False
