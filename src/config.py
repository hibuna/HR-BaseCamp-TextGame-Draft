from src.command import CommandUsage
from src.enums import PlayerAction, PlayerActionPreposition
from src.object.base import Item, Object, Equipable
from src.player import Player

action_usage_mapping = {
    PlayerAction.QUIT: [
        CommandUsage(
            action=PlayerAction.QUIT,
        ),
    ],
    PlayerAction.HELP: [
        CommandUsage(
            action=PlayerAction.HELP,
        ),
        CommandUsage(
            action=PlayerAction.HELP,
            object_types=[Object, Item],
        ),
    ],
    PlayerAction.INSPECT: [
        CommandUsage(
            action=PlayerAction.INSPECT,
        ),
        CommandUsage(
            action=PlayerAction.INSPECT,
            object_types=[Object, Item, Player],
        ),
    ],
    PlayerAction.PICKUP: [
        CommandUsage(
            action=PlayerAction.PICKUP,
            object_types=[Item],
        ),
    ],
    PlayerAction.EQUIP: [
        CommandUsage(
            action=PlayerAction.EQUIP,
            object_types=[Equipable],
        ),
    ],
    PlayerAction.UNEQUIP: [
        CommandUsage(
            action=PlayerAction.UNEQUIP,
            object_types=[Equipable],
        ),
    ],
    PlayerAction.ENTER: [
        CommandUsage(
            action=PlayerAction.ENTER,
            object_types=[Object],
        ),
    ],
    PlayerAction.FILL: [
        CommandUsage(
            action=PlayerAction.FILL,
            object_types=[Item, Object],
            preposition=PlayerActionPreposition.WITH,
            preposition_object_types=[Item, Object],
        ),
    ],
    PlayerAction.EMPTY: [
        CommandUsage(
            action=PlayerAction.EMPTY,
            object_types=[Item],
            preposition=PlayerActionPreposition.INTO,
            preposition_object_types=[Item, Object],
        ),
    ],
    PlayerAction.TURN: [
        CommandUsage(
            action=PlayerAction.TURN,
            object_types=[Object],
        ),
    ],
    PlayerAction.HIT: [
        CommandUsage(
            action=PlayerAction.HIT,
            object_types=[Object],
        ),
    ],
    PlayerAction.USE: [
        CommandUsage(
            action=PlayerAction.USE,
            object_types=[Item, Object],
        ),
        CommandUsage(
            action=PlayerAction.USE,
            object_types=[Item, Object],
            preposition=PlayerActionPreposition.ON,
            preposition_object_types=[Item, Object],
        ),
    ],
    PlayerAction.PRESS: [
        CommandUsage(
            action=PlayerAction.PRESS,
            object_types=[Object],
        ),
    ],
    PlayerAction.OPEN: [
        CommandUsage(
            action=PlayerAction.OPEN,
            object_types=[Object],
        ),
    ],
    PlayerAction.CLOSE: [
        CommandUsage(
            action=PlayerAction.CLOSE,
            object_types=[Object],
        ),
    ],
    PlayerAction.REPAIR: [
        CommandUsage(
            action=PlayerAction.REPAIR,
            object_types=[Object, Item],
            preposition=PlayerActionPreposition.WITH,
            preposition_object_types=[Object, Item],
        ),
    ],
}


def _build_action_object_amt_mapping() -> dict[PlayerAction, list[int]]:
    mapping = {}
    for action, usages in action_usage_mapping.items():
        object_amt_combinations = []
        for usage in usages:
            object_amt = 0
            object_amt += int(bool(usage.object_types))
            object_amt += int(bool(usage.preposition_object_types))
            object_amt_combinations.append(object_amt)
        mapping[action] = list(set(object_amt_combinations))
    return mapping


def _build_action_preposition_mapping() -> (
    dict[PlayerAction, list[PlayerActionPreposition]]
):
    mapping = {}
    for action, usages in action_usage_mapping.items():
        mapping[action] = []
        for usage in usages:
            if usage.preposition:
                mapping[action].append(usage.preposition)
    return mapping


class Config:
    user_prompt: str = "> "
    action_usage_mapping = action_usage_mapping
    action_object_amt_mapping = _build_action_object_amt_mapping()
    action_preposition_mapping = _build_action_preposition_mapping()
