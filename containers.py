from typing import Any, TYPE_CHECKING

from dependency_injector import containers, providers

from src.effect import WaterBreathing
from src.environment import TownSquare
from src.item import Bucket, Sword
from src.object import Well, Object, River, Interactable
from src.player import Player
from src.service import WellService, Service, ItemService, RiverService

if TYPE_CHECKING:
    from src.object import Object


class CustomContainer(containers.DeclarativeContainer):
    @classmethod
    def get(cls, item: str | Object) -> Any:
        attributes = vars(cls).get("providers", {}).items()
        for k, v in attributes:
            v = v()
            if item == k:
                return v
            if issubclass(type(v), Interactable) and item in v.references:
                return v
            if issubclass(type(v), Service) and isinstance(item, v.object_type):
                return v


class Globals(containers.DeclarativeContainer):
    player = providers.Singleton(Player)


class Effects(containers.DeclarativeContainer):
    water_breathing = providers.Singleton(WaterBreathing)


class Items(CustomContainer):
    bucket = providers.Singleton(
        Bucket,
        effects=[Effects.water_breathing()]
    )
    sword = providers.Singleton(Sword)


class Objects(CustomContainer):
    well = providers.Singleton(
        Well,
        items=[Items.sword()],
    )
    river = providers.Singleton(River)


class Environments(CustomContainer):
    town_square = providers.Singleton(
        TownSquare,
        objects=[Objects.well(), Objects.river()],
        items=[Items.bucket()],
    )


class Services(CustomContainer):
    generic_service = providers.Singleton(
        Service,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    item_service = providers.Singleton(
        ItemService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    well_service = providers.Singleton(
        WellService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    river_service = providers.Singleton(
        RiverService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
