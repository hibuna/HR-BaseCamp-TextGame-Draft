from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from src.resolvers import (
    ItemResolver,
    ObjectResolver,
    ServiceResolver,
    CommandObjectResolver,
)
from src.service import (
    Service,
    ItemService,
    PrologueControlPanelService,
    PrologueControlPanelButtonService,
    HeavyDoorService,
    HeavyDoorWheelService,
)
from src.player import Player
from src.object.objects import (
    HeavyDoorWheel,
    HeavyDoor,
    PrologueControlPanelButton,
    PrologueControlPanel,
    ControlPanel,
)
from src.environment import PrologueCockpit, Cockpit


class CustomContainer(DeclarativeContainer):
    @classmethod
    def members(cls) -> dict:
        return {k: v for k, v in vars(cls).get("providers", {}).items()}


class Globals(DeclarativeContainer):
    player = Singleton(Player)


class Effects(DeclarativeContainer):
    ...


class Items(CustomContainer):
    ...


class Objects(CustomContainer):
    prologue_control_panel = Singleton(PrologueControlPanel)
    prologue_control_panel_button = Singleton(PrologueControlPanelButton)
    control_panel = Singleton(ControlPanel)
    heavy_door_wheel = Singleton(HeavyDoorWheel)
    heavy_door = Singleton(HeavyDoor)


class Environments(DeclarativeContainer):
    prologue_cockpit = Singleton(
        PrologueCockpit,
        objects=[
            Objects.prologue_control_panel(),
            Objects.prologue_control_panel_button(),
            Objects.heavy_door_wheel(),
            Objects.heavy_door(),
        ],
    )
    cockpit = Singleton(
        Cockpit,
        objects=[
            Objects.control_panel(),
            Objects.heavy_door(),
            Objects.heavy_door_wheel(),
        ],
    )


class Services(CustomContainer):
    generic_service = Singleton(
        Service,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    item_service = Singleton(
        ItemService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    prologue_control_panel_service = Singleton(
        PrologueControlPanelService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    prologue_control_panel_button_service = Singleton(
        PrologueControlPanelButtonService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    heavy_door_service = Singleton(
        HeavyDoorService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    heavy_door_wheel_service = Singleton(
        HeavyDoorWheelService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )


class Resolvers(CustomContainer):
    items = Singleton(
        ItemResolver,
        container=Items,
    )
    objects = Singleton(
        ObjectResolver,
        container=Objects,
    )
    services = Singleton(
        ServiceResolver,
        container=Services,
        objects_r=objects,
    )
    command_object = Singleton(
        CommandObjectResolver,
        items_r=items,
        objects_r=objects,
    )
