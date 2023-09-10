import enum


class CustomEnum(enum.Enum):
    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other.upper()
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


class PlayerAction(CustomEnum):
    QUIT = enum.auto()
    HELP = enum.auto()
    INSPECT = enum.auto()
    PICKUP = enum.auto()
    EQUIP = enum.auto()
    UNEQUIP = enum.auto()
    ENTER = enum.auto()
    FILL = enum.auto()
    EMPTY = enum.auto()


class PlayerActionPreposition(CustomEnum):
    WITH = enum.auto()
    ON = enum.auto()
    INTO = enum.auto()
    IN = enum.auto()


class EquipableSlot(CustomEnum):
    HEAD = enum.auto()
    BODY = enum.auto()
    LEGS = enum.auto()
    FEET = enum.auto()
    HAND = enum.auto()
    OFFHAND = enum.auto()
    NECK = enum.auto()
    FINGER = enum.auto()


class UsageFormat(CustomEnum):
    ACTION = enum.auto()
    OBJECT = enum.auto()
    PREPOSITION = enum.auto()
    PREPOSITION_OBJECT = enum.auto()
