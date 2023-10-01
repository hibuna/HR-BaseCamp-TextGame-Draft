from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from src.effect import VacuumResistance, FullBladder
from src.resolvers import (
    ItemResolver,
    ObjectResolver,
    ServiceResolver,
    CommandObjectResolver,
)
from src.service import (
    Service,
    ItemService,
    ControlPanelService,
    ControlPanelExtinguishButtonService,
    HeavyDoorService,
    HeavyDoorWheelService,
    CockpitDoorService,
    EngineRoomDoorService,
    BedroomDoorService,
    BathroomDoorService,
    WorkshopDoorService,
    CanteenDoorService,
    StorageDoorService,
    ArmoryDoorService,
    HallwayDoorService, SpaceSuitService, GlassCaseService, HullService, RepairKitService, UrinalService,
    FuelCanService, EngineService,
)
from src.player import Player
from src.object.items import SpaceSuit, FireAxe, RepairKit, FuelCan
from src.object.objects import (
    HeavyDoorWheel,
    HeavyDoor,
    ControlPanelExtinguishButton,
    ControlPanel,
    ArmoryDoor,
    StorageDoor,
    CanteenDoor,
    WorkshopDoor,
    BathroomDoor,
    BedroomDoor,
    EngineRoomDoor,
    CockpitDoor,
    HallwayDoor, GlassCase, Hull, Engine, Urinal,
)
from src.environment import (
    PrologueCockpit,
    Cockpit,
    Hallway,
    EngineRoom,
    Workshop,
    Bathroom,
    Bedroom,
    Canteen,
    StorageRoom,
    Armory,
    Outside,
)


class CustomContainer(DeclarativeContainer):
    @classmethod
    def members(cls) -> dict:
        return {k: v for k, v in vars(cls).get("providers", {}).items()}


class Globals(DeclarativeContainer):
    player = Singleton(Player)


class Effects(DeclarativeContainer):
    full_bladder = Singleton(FullBladder)
    vacuum_resistance = Singleton(VacuumResistance)


class Items(CustomContainer):
    space_suit = Singleton(
        SpaceSuit,
        effects=[Effects.vacuum_resistance()]
    )
    fire_axe = Singleton(FireAxe)
    repair_kit = Singleton(RepairKit)
    fuel_can = Singleton(FuelCan)


class Objects(CustomContainer):
    control_panel_extinguish_button = Singleton(ControlPanelExtinguishButton)
    control_panel = Singleton(ControlPanel)
    heavy_door_wheel = Singleton(HeavyDoorWheel)
    heavy_door = Singleton(HeavyDoor)
    hallway_door = Singleton(HallwayDoor)
    cockpit_door = Singleton(CockpitDoor)
    engine_room_door = Singleton(EngineRoomDoor)
    bedroom_door = Singleton(BedroomDoor)
    bathroom_door = Singleton(BathroomDoor)
    workshop_door = Singleton(WorkshopDoor)
    canteen_door = Singleton(CanteenDoor)
    storage_door = Singleton(StorageDoor)
    armory_door = Singleton(ArmoryDoor)
    glass_case = Singleton(
        GlassCase,
        items=[Items.fire_axe()]
    )
    hull = Singleton(Hull)
    engine = Singleton(Engine)
    urinal = Singleton(Urinal)


class Environments(CustomContainer):
    prologue_cockpit = Singleton(
        PrologueCockpit,
        objects=[
            Objects.control_panel(),
            Objects.control_panel_extinguish_button(),
            Objects.heavy_door_wheel(),
            Objects.heavy_door()
        ]
    )
    cockpit = Singleton(
        Cockpit,
        objects=[
            Objects.control_panel(),
            Objects.heavy_door(),
            Objects.heavy_door_wheel(),
            Objects.hallway_door(),
            Objects.glass_case()
        ]
    )
    hallway = Singleton(
        Hallway,
        objects=[
            Objects.cockpit_door(),
            Objects.engine_room_door(),
            Objects.bedroom_door(),
            Objects.bathroom_door(),
            Objects.workshop_door(),
            Objects.canteen_door(),
            Objects.storage_door(),
            Objects.armory_door()
        ]
    )
    bathroom = Singleton(
        Bathroom,
        objects=[
            Objects.hallway_door(),
            Objects.urinal()
        ]
    )
    engine_room = Singleton(
        EngineRoom,
        objects=[
            Objects.hallway_door(),
            Objects.engine()
        ]
    )
    workshop = Singleton(
        Workshop,
        objects=[
            Objects.hallway_door()
        ],
        items=[
            Items.repair_kit(),
            Items.fuel_can()
        ]
    )
    bedroom = Singleton(
        Bedroom,
        objects=[
            Objects.hallway_door()
        ]
    )
    storage_room = Singleton(
        StorageRoom,
        objects=[
            Objects.hallway_door()
        ]
    )
    armory = Singleton(
        Armory,
        objects=[
            Objects.hallway_door()
        ],
        items=[
            Items.space_suit()
        ]
    )
    canteen = Singleton(
        Canteen,
        objects=[
            Objects.hallway_door()
        ]
    )
    outside = Singleton(
        Outside,
        objects=[
            Objects.heavy_door(),
            Objects.hull()
        ]
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
    control_panel_service = Singleton(
        ControlPanelService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    control_panel_extinguish_button_service = Singleton(
        ControlPanelExtinguishButtonService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    space_suit_service = Singleton(
        SpaceSuitService,
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
    glass_case_service = Singleton(
        GlassCaseService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    hallway_door_service = Singleton(
        HallwayDoorService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    cockpit_door_service = Singleton(
        CockpitDoorService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    engine_room_door_service = Singleton(
        EngineRoomDoorService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    workshop_door_service = Singleton(
        WorkshopDoorService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    bedroom_door_service = Singleton(
        BedroomDoorService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    bathroom_door_service = Singleton(
        BathroomDoorService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    storage_door_service = Singleton(
        StorageDoorService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    canteen_door_service = Singleton(
        CanteenDoorService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    armory_door_service = Singleton(
        ArmoryDoorService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    hull_service = Singleton(
        HullService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    repair_kit_service = Singleton(
        RepairKitService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    urinal_service = Singleton(
        UrinalService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    engine_service = Singleton(
        EngineService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    fuel_can_service = Singleton(
        FuelCanService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
        engine_service=engine_service()
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
        player=Globals.player(),
        items_r=items,
        objects_r=objects,
    )
