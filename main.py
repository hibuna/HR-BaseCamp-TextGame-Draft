import logging
import sys

from src.command import CommandValidator
from src.config import Config
from src.containers import Globals, Environments, Items, Objects, Services, Resolvers, Effects
from src.core import Engine
from src.utils import overlap

if overlap(["-d", "--debug"], sys.argv[1:]):
    logging.basicConfig(level=logging.DEBUG)

player = Globals.player()
player.environment = Environments.prologue_cockpit()
player.effects = [Effects.full_bladder()]

player.inventory = [Items.fuel_can()]
player.environment = Environments.engine_room()

command_validator = CommandValidator(
    player=player,
    command_object_r=Resolvers.command_object(),
    config=Config,
)

engine = Engine(
    player=player,
    items_c=Items,
    objects_c=Objects,
    services_c=Services,
    resolvers_c=Resolvers,
    command_validator=command_validator,
    config=Config,
)

engine.start()
