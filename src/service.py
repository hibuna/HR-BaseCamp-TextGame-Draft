from typing import TYPE_CHECKING, Generic, TypeVar

from src.enums import PlayerAction
from src.object.base import Object, Item, Equipable
from src.object.items import SpaceSuit, RepairKit, FuelCan
from src.object.objects import (
    HeavyDoor,
    ControlPanel,
    ControlPanelExtinguishButton,
    HeavyDoorWheel,
    HallwayDoor,
    ArmoryDoor,
    BedroomDoor,
    CanteenDoor,
    StorageDoor,
    BathroomDoor,
    WorkshopDoor,
    EngineRoomDoor,
    CockpitDoor,
    GlassCase, Hull, Engine, Urinal,
)
from src.utils import die_in_void

if TYPE_CHECKING:
    from src.player import Player
    from src.containers import Effects, Items, Objects, Environments
    from src.command import Command

T = TypeVar("T", bound=Object)


class Service(Generic[T]):
    """
    Generic service class for interacting with objects. Separates the responsibility
    of interaction with an object from the object itself.

    Attributes:
    -----------
    object_type : type
        The type of object that this service interacts with.
    _player : Player
        The player.
    _effects_c : Effects
        The effects container.
    _items_c : Items
        The items container.
    _objects_c : Objects
        The objects container.
    _environments_c : Environments
        The environments container.
    _action_mapping : dict[PlayerAction, function]
        A mapping of actions to functions that perform the action.
    """

    object_type: T = type(None)

    def __init__(
            self,
            player: "Player",
            effects_c: "Effects",
            items_c: "Items",
            objects_c: "Objects",
            environments_c: "Environments",
    ):
        self._player = player
        self._effects_c = effects_c
        self._items_c = items_c
        self._objects_c = objects_c
        self._environments_c = environments_c

        self._action_mapping = {
            PlayerAction.EQUIP: self._equip,
            PlayerAction.UNEQUIP: self._unequip,
            PlayerAction.PICKUP: self._pickup,
            PlayerAction.FILL: self._fill,
            PlayerAction.EMPTY: self._empty,
            PlayerAction.INSPECT: self._inspect,
            PlayerAction.ENTER: self._enter,
            PlayerAction.USE: self._use,
            PlayerAction.HIT: self._hit,
            PlayerAction.TURN: self._turn,
            PlayerAction.PRESS: self._press,
            PlayerAction.OPEN: self._open,
            PlayerAction.CLOSE: self._close,
            PlayerAction.REPAIR: self._repair,
        }

    def interact(self, cmd: "Command") -> str:
        """Interact with an object with dynamically using the action and preposition
        object."""
        action_method = self._action_mapping.get(cmd.action)
        if action_method is None:
            raise ValueError(f"Action '{cmd.action_str.upper()}' is not recognized")
        return action_method(cmd)  # noqa

    def _pickup(self, cmd: "Command") -> str:
        """Default pickup method. Can be overridden by subclasses."""
        return "You can't pick that up."

    def _fill(self, cmd: "Command") -> str:
        """Default fill method. Can be overridden by subclasses."""
        return "You can't fill that."

    def _empty(self, cmd: "Command") -> str:
        """Default empty method. Can be overridden by subclasses."""
        return "You can't empty that."

    def _inspect(self, cmd: "Command") -> str:
        """Default inspect method. Can be overridden by subclasses."""
        if cmd.object:
            return cmd.object.description

        description = self._player.environment.description
        objects = self._player.environment.shown_objects_and_items_str
        return " ".join((description, objects)).strip()

    def _enter(self, cmd: "Command") -> str:
        """Default enter method. Can be overridden by subclasses."""
        return "You can't enter that."

    def _equip(self, cmd: "Command") -> str:
        """Default equip method. Can be overridden by subclasses."""
        return "You can't equip that."

    def _unequip(self, cmd: "Command") -> str:
        """Default unequip method. Can be overridden by subclasses."""
        return "You can't unequip that."

    def _use(self, cmd: "Command") -> str:
        """Default use method. Can be overridden by subclasses."""
        return "You can't use that."

    def _hit(self, cmd: "Command") -> str:
        """Default hit method. Can be overridden by subclasses."""
        return f"You hit {cmd.object}. Nothing happens."

    def _turn(self, cmd: "Command") -> str:
        """Default turn method. Can be overridden by subclasses."""
        return "You can't turn that."

    def _press(self, cmd: "Command") -> str:
        """Default press method. Can be overridden by subclasses."""
        return "You can't press that."

    def _open(self, cmd: "Command") -> str:
        """Default open method. Can be overridden by subclasses."""
        return "You can't open that."

    def _close(self, cmd: "Command") -> str:
        """Default close method. Can be overridden by subclasses."""
        return "You can't close that."

    def _repair(self, cmd: "Command"):
        """Default repair method. Can be overridden by subclasses."""
        return "You can't repair that."


class ItemService(Service[Item]):
    object_type = Item

    def _pickup(self, cmd: "Command") -> str:
        """Generic item pickup method."""
        if not issubclass(type(cmd.object), Item):
            return "You can't pick that up."

        if PlayerAction.PICKUP not in cmd.object.interactions:
            return "You can't pick that up."

        self._player.environment.items.remove(cmd.object)
        self._player.inventory.append(cmd.object)

        return f"Picked up: {cmd.object.name.upper()}"

    def _equip(self, cmd: "Command") -> str:
        """Generic item equip method."""
        if cmd.object not in self._player.inventory:
            return "You don't have that."

        if not issubclass(type(cmd.object), Equipable):
            return "You can't equip that."

        if PlayerAction.EQUIP not in cmd.object.interactions:
            return "You can't equip that."

        return self._player.equip(cmd.object)  # noqa

    def _unequip(self, cmd: "Command") -> str:
        """Generic item unequip method.""" ""
        if cmd.object not in self._player.equipped:
            return f"You don't have that equipped: {cmd.object.name.upper()}"

        return self._player.unequip(cmd.object)  # noqa


class SpaceSuitService(ItemService):
    object_type = SpaceSuit

    def _unequip(self, cmd: "Command") -> str:
        player_in_vacuum = (
            self._player.environment is self._environments_c.outside()
            or self._player.environment is self._environments_c.cockpit()
            and self._objects_c.heavy_door().state is self._objects_c.heavy_door().States.OPEN
        )
        if player_in_vacuum:
            die_in_void()
        return self._player.unequip(self._items_c.space_suit())


class ControlPanelService(Service[ControlPanel]):
    object_type = ControlPanel

    def _inspect(self, cmd: "Command") -> str:
        panel = self._objects_c.control_panel()
        if panel.state is panel.States.PROLOGUE:
            return "A control panel with a lot of buttons. A symbol of a flame flashes on the screen. Next to it is a red button."

        str_ = panel.description

        heavy_door = self._objects_c.heavy_door()
        heavy_door_wheel = self._objects_c.heavy_door_wheel()
        hidden_conditions = [
            heavy_door.state is heavy_door.States.CLOSED,
            heavy_door_wheel.state is heavy_door_wheel.States.CLOSED,
            self._effects_c.full_bladder() not in self._player.effects,
        ]
        if not all(hidden_conditions):
            str_ += " You feel like you are forgetting something."

        engine_fixed = self._objects_c.engine().state is self._objects_c.engine().States.WORKING
        if not engine_fixed:
            str_ += " The engine light is flashing."

        hull_fixed = self._objects_c.hull().state is self._objects_c.hull().States.REPAIRED
        if not hull_fixed:
            str_ += " The hull light is flashing."

        return str_


    def _use(self, cmd: "Command"):
        str_ = self._inspect(cmd)

        if str_ != self._objects_c.control_panel().description:
            return str_

        str_ += (
            " All control seem to be functional. You sit down in the pilot seat and strap "
            "yourself in. After running diagnostics, the control panel displays a message: "
            '"All systems functional. Ready for takeoff."'
            " You press the ignition button and the ship starts to rumble. You feel the G-force "
            "increasing. You are going home."
        )
        print(str_)
        exit(0)


class ControlPanelExtinguishButtonService(Service[ControlPanelExtinguishButton]):
    object_type = ControlPanelExtinguishButton

    def _press(self, cmd: "Command") -> str:
        self._player.environment = self._environments_c.cockpit()
        self._objects_c.control_panel().state = self._objects_c.control_panel().States.MAIN
        return "A vent opens and you hear a hissing sound. You start feeling woozy and pass out."

    def _use(self, cmd: "Command"):
        return self._press(cmd)

    def _hit(self, cmd: "Command"):
        return self._press(cmd)


class HeavyDoorService(Service[HeavyDoor]):
    object_type = HeavyDoor

    def _inspect(self, cmd: "Command"):
        wheel = self._objects_c.heavy_door_wheel()
        direction = "left" if wheel.state is wheel.States.OPEN else "right"
        return (
            f"A heavy door with a wheel on it. The wheel is turned to the {direction}."
        )

    def _enter(self, cmd: "Command"):
        door = self._objects_c.heavy_door()
        if door.state is door.States.CLOSED:
            return "The door is closed."
        if door.state is door.States.OPEN:
            if self._player.environment is self._environments_c.cockpit():
                self._player.environment = self._environments_c.outside()
                return "You enter the void."
            if self._player.environment is self._environments_c.outside():
                self._player.environment = self._environments_c.cockpit()
                return "You enter the cockpit."

    def _open(self, cmd: "Command"):
        wheel = self._objects_c.heavy_door_wheel()
        if wheel.state is wheel.States.CLOSED:
            return "The door is locked."
        if wheel.state is wheel.States.OPEN:
            if self._effects_c.vacuum_resistance() not in self._player.effects:
                die_in_void(inside=True, opening_door=True)
            door = self._objects_c.heavy_door()
            door.state = door.States.OPEN
            return "You open the door."
        return ""

    def _close(self, cmd: "Command"):
        door = self._objects_c.heavy_door()
        if door.state is door.States.OPEN:
            door.state = door.States.CLOSED
            return "You close the door."
        return "The door is already closed."


class HeavyDoorWheelService(Service[HeavyDoorWheel]):
    object_type = HeavyDoorWheel

    def _turn(self, cmd: "Command"):
        if self._objects_c.heavy_door().state is self._objects_c.heavy_door().States.OPEN:
            return "You can't turn the wheel when the door is open."
        wheel = self._objects_c.heavy_door_wheel()
        if wheel.state is wheel.States.OPEN:
            wheel.state = wheel.States.CLOSED
        elif wheel.state is wheel.States.CLOSED:
            wheel.state = wheel.States.OPEN
        return "You turn the wheel."


class GlassCaseService(Service[GlassCase]):
    object_type = GlassCase

    def _inspect(self, cmd: "Command"):
        case = self._objects_c.glass_case()
        if case.state is case.States.INTACT:
            return case.description
        if self._items_c.fire_axe() in self._objects_c.glass_case().items:
            return "A broken glass case with a fire axe inside."
        return "A broken glass case. It's empty."

    def _hit(self, cmd: "Command"):
        case = self._objects_c.glass_case()
        if case.state is case.States.INTACT:
            case.state = case.States.BROKEN
            self._environments_c.cockpit().items += [self._items_c.fire_axe()]
            return "You shatter the glass."
        return "The glass case is already broken."


class HallwayDoorService(Service[HallwayDoor]):
    object_type = HallwayDoor

    def _enter(self, cmd: "Command"):
        door = self._objects_c.hallway_door()
        if door.state is door.States.STUCK:
            return "The door is stuck."
        self._player.environment = self._environments_c.hallway()
        return "You enter the hallway."

    def _hit(self, cmd: "Command"):
        door = self._objects_c.hallway_door()
        if door.state is door.States.STUCK and self._items_c.fire_axe() in self._player.equipped:
            door.state = door.States.OPEN
            return "You hit the door with the axe. It clicks."
        return super()._hit(cmd)


class CockpitDoorService(Service[CockpitDoor]):
    object_type = CockpitDoor

    def _enter(self, cmd: "Command"):
        door = self._objects_c.heavy_door()
        if door.state is door.States.OPEN and self._effects_c.vacuum_resistance() not in self._player.effects:
            die_in_void(inside=True)
        self._player.environment = self._environments_c.cockpit()
        return "You enter the cockpit."


class ArmoryDoorService(Service[ArmoryDoor]):
    object_type = ArmoryDoor

    def _enter(self, cmd: "Command"):
        self._player.environment = self._environments_c.armory()
        return "You enter the armory."


class BedroomDoorService(Service[BedroomDoor]):
    object_type = BedroomDoor

    def _enter(self, cmd: "Command"):
        self._player.environment = self._environments_c.bedroom()
        return "You enter the bedroom."


class CanteenDoorService(Service[CanteenDoor]):
    object_type = CanteenDoor

    def _enter(self, cmd: "Command"):
        self._player.environment = self._environments_c.canteen()
        return "You enter the canteen."


class StorageDoorService(Service[StorageDoor]):
    object_type = StorageDoor

    def _enter(self, cmd: "Command"):
        self._player.environment = self._environments_c.storage_room()
        return "You enter the storage room."


class BathroomDoorService(Service[BathroomDoor]):
    object_type = BathroomDoor

    def _enter(self, cmd: "Command"):
        self._player.environment = self._environments_c.bathroom()
        return "You enter the bathroom."


class WorkshopDoorService(Service[WorkshopDoor]):
    object_type = WorkshopDoor

    def _enter(self, cmd: "Command"):
        self._player.environment = self._environments_c.workshop()
        return "You enter the workshop."


class EngineRoomDoorService(Service[EngineRoomDoor]):
    object_type = EngineRoomDoor

    def _enter(self, cmd: "Command"):
        self._player.environment = self._environments_c.engine_room()
        return "You enter the engine room."


class HullService(Service[Hull]):
    object_type = Hull

    def _inspect(self, cmd: "Command"):
        hull = self._objects_c.hull()
        if hull.state is hull.States.DAMAGED:
            return " ".join([hull.description, "It is damaged."])
        return hull.description

    def _repair(self, cmd: "Command"):
        hull = self._objects_c.hull()
        if cmd.preposition_object is self._items_c.repair_kit():
            if hull.state is hull.States.DAMAGED:
                hull.state = hull.States.REPAIRED
                hull.remove_reference("damage")
                return "You repair the hull."
            return "The hull is already intact."
        return super()._repair(cmd)


class RepairKitService(ItemService):
    object_type = RepairKit

    def _use(self, cmd: "Command"):
        hull = self._objects_c.hull()
        if cmd.preposition_object is not hull:
            return super()._use(cmd)
        if hull.state is hull.States.DAMAGED:
            hull.state = hull.States.REPAIRED
            hull.remove_reference("damage")
            return "You repair the hull."
        return "The hull is already intact."


class EngineService(Service[Engine]):
    object_type = Engine

    def _fill(self, cmd: "Command"):
        if cmd.preposition_object is not self._items_c.fuel_can():
            return super()._fill(cmd)

        engine = self._objects_c.engine()
        if engine.state is engine.States.EMPTY:
            engine.state = engine.States.FUELED
            return "You fill the engine."
        return "The engine is already fueled."

    def _hit(self, cmd: "Command"):
        engine = self._objects_c.engine()
        if self._items_c.fire_axe() in self._player.equipped:
            engine.state = engine.States.BROKEN
            return "You hit the engine with the axe. It breaks into pieces."
        if engine.state is engine.States.FUELED:
            engine.state = engine.States.WORKING
            return "The engine start roaring."
        return super()._hit(cmd)


class FuelCanService(ItemService):
    object_type = FuelCan

    def __init__(self, engine_service: EngineService, *args, **kwargs):
        self._engine_service = engine_service
        super().__init__(*args, **kwargs)

    def _empty(self, cmd: "Command") -> str:
        if cmd.preposition_object is not self._objects_c.engine():
            return super()._empty(cmd)

        cmd.object, cmd.preposition_object = cmd.preposition_object, cmd.object
        cmd.action = PlayerAction.FILL
        return self._engine_service.interact(cmd)


class UrinalService(Service[Urinal]):
    object_type = Urinal

    def _use(self, cmd: "Command"):
        if self._items_c.space_suit() in self._player.equipped:
            return "You can't use the urinal while wearing a space suit."
        if self._effects_c.full_bladder() in self._player.effects:
            self._player.effects.remove(self._effects_c.full_bladder())
            return "You relieve yourself."
        return "You don't feel like going."
