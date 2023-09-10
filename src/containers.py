from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from src.resolvers import (
    ItemResolver,
    ObjectResolver,
    ServiceResolver,
    CommandObjectResolver,
)
from src.service import Service, ItemService, WellService, RiverService, BucketService
from src.player import Player
from src.effect import WaterBreathing
from src.object.items import Sword, Bucket
from src.object.objects import Well, River
from src.environment import TownSquare


class CustomContainer(DeclarativeContainer):
    @classmethod
    def members(cls) -> dict:
        return {k: v for k, v in vars(cls).get("providers", {}).items()}


class Globals(DeclarativeContainer):
    player = Singleton(Player)


class Effects(DeclarativeContainer):
    water_breathing = Singleton(WaterBreathing)


class Items(CustomContainer):
    bucket = Singleton(Bucket, effects=[Effects.water_breathing()])
    sword = Singleton(Sword)


class Objects(CustomContainer):
    well = Singleton(
        Well,
        items=[Items.sword()],
    )
    river = Singleton(River)


class Environments(DeclarativeContainer):
    town_square = Singleton(
        TownSquare,
        objects=[Objects.well(), Objects.river()],
        items=[Items.bucket()],
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
    well_service = Singleton(
        WellService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    river_service = Singleton(
        RiverService,
        player=Globals.player(),
        effects_c=Effects,
        items_c=Items,
        objects_c=Objects,
        environments_c=Environments,
    )
    bucket_service = Singleton(
        BucketService,
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
