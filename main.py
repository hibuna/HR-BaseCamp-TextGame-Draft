import logging

from containers import Globals, Environments, Items, Objects, Services
from src.input_resolver import Engine

logging.basicConfig(level=logging.DEBUG)

player = Globals.player()
player.environment = Environments.town_square()
engine = Engine(items_c=Items, objects_c=Objects, services_c=Services)

while True:
    engine.ask_input()
