import enum

from src.object.base import Object
from src.enums import PlayerAction


class ControlPanelExtinguishButton(Object):
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
    class States:
        PROLOGUE = enum.auto()
        MAIN = enum.auto()

    name = "control panel"
    description = "The control panel."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.USE,
    ]
    _references = ["control panel", "panel"]
    state = States.PROLOGUE
    shown = True


class HeavyDoor(Object):
    class States:
        OPEN = enum.auto()
        CLOSED = enum.auto()

    name = "heavy door"
    description = "A heavy door."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.OPEN,
        PlayerAction.CLOSE,
        PlayerAction.ENTER,
    ]
    _references = ["heavy door", "outside", "void"]
    shown = True
    state = States.CLOSED


class HeavyDoorWheel(Object):
    class States:
        OPEN = enum.auto()
        CLOSED = enum.auto()

    name = "heavy door wheel"
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.TURN,
    ]
    _references = ["wheel", "heavy door wheel"]
    state = States.CLOSED
    shown = False

    @property
    def description(self):
        str_ = "A solid metal wheel is attached to the door."
        if self.state is self.States.OPEN:
            return str_ + " The wheel is turned to the left."
        if self.state is self.States.CLOSED:
            return str_ + " The wheel is turned to the right."


class StorageDoor(Object):
    name = "storage door"
    description = "A door to the storage room."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.ENTER,
    ]
    _references = ["storage", "storage door"]
    state = None
    shown = True


class WorkshopDoor(Object):
    name = "workshop door"
    description = "A door to the workshop."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.ENTER,
    ]
    _references = ["workshop", "workshop door"]
    state = None
    shown = True


class ArmoryDoor(Object):
    name = "armory door"
    description = "A door to the armory."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.ENTER,
    ]
    _references = ["armory", "armory door"]
    state = None
    shown = True


class CanteenDoor(Object):
    name = "canteen door"
    description = "A door to the canteen."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.ENTER,
    ]
    _references = ["canteen", "canteen door"]
    state = None
    shown = True


class BedroomDoor(Object):
    name = "bedroom door"
    description = "A door to the bedroom."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.ENTER,
    ]
    _references = ["bedroom", "bedroom door"]
    state = None
    shown = True


class BathroomDoor(Object):
    name = "bathroom door"
    description = "A door to the bathroom."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.ENTER,
    ]
    _references = ["bathroom", "bathroom door"]
    state = None
    shown = True


class EngineRoomDoor(Object):
    name = "engine room door"
    description = "A door to the engine room."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.ENTER,
    ]
    _references = ["engine room", "engine room door"]
    state = None
    shown = True


class HallwayDoor(Object):
    class States:
        OPEN = enum.auto()
        STUCK = enum.auto()

    name = "hallway door"
    description = "A door to the hallway."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.ENTER,
        PlayerAction.HIT,
    ]
    _references = ["hallway", "hallway door"]
    state = States.STUCK
    shown = True


class CockpitDoor(Object):
    name = "cockpit door"
    description = "A door to the cockpit."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.ENTER,
    ]
    _references = ["cockpit", "cockpit door"]
    state = None
    shown = True


class GlassCase(Object):
    class States:
        INTACT = enum.auto()
        BROKEN = enum.auto()

    name = "glass case"
    description = 'A glass case. It reads: "Break in case of emergency".'
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.HIT,
    ]
    _references = ["glass case", "glass", "case"]
    state = States.INTACT
    shown = True


class Hull(Object):
    class States:
        DAMAGED = enum.auto()
        REPAIRED = enum.auto()

    name = "hull"
    description = "A hull plate."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.REPAIR,
    ]
    _references = ["hull", "damage"]
    state = States.DAMAGED
    shown = True


class Engine(Object):
    class States:
        EMPTY = enum.auto()
        FUELED = enum.auto()
        WORKING = enum.auto()
        BROKEN = enum.auto()

    name = "engine"
    # description = "The engine."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.FILL,
        PlayerAction.HIT,
    ]
    _references = ["engine"]
    state = States.EMPTY
    shown = True

    @property
    def description(self):
        if self.state is self.States.EMPTY:
            return "The engine."
        if self.state is self.States.FUELED:
            return "The engine is filled to the brim."
        if self.state is self.States.WORKING:
            return "The engine is roaring with life."
        if self.state is self.States.BROKEN:
            return "The engine looks permanently broken."


class Urinal(Object):
    name = "urinal"
    description = "A urinal."
    interactions = [
        PlayerAction.INSPECT,
        PlayerAction.USE,
    ]
    _references = ["urinal"]
    state = None
    shown = True
