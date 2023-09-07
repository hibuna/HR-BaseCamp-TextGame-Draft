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


class CustomEnumMeta(enum.EnumMeta):
    def __getitem__(self, name: str):
        try:
            return super().__getitem__(name.upper())
        except KeyError:
            return None

    def __contains__(self, item: str | enum.Enum):
        if isinstance(item, str):
            return item.upper() in self.__members__
        return super().__contains__(item)


class PlayerAction(CustomEnum, metaclass=CustomEnumMeta):
    HELP = enum.auto()
    ENTER = enum.auto()
    FILL = enum.auto()
    EMPTY = enum.auto()
    PICKUP = enum.auto()
    EQUIP = enum.auto()
    UNEQUIP = enum.auto()
    INSPECT = enum.auto()


class PlayerActionPreposition(CustomEnum, metaclass=CustomEnumMeta):
    WITH = enum.auto()
    ON = enum.auto()
    INTO = enum.auto()
    IN = enum.auto()


class EquipableSlot(CustomEnum, metaclass=CustomEnumMeta):
    head = enum.auto()
    body = enum.auto()
    legs = enum.auto()
    feet = enum.auto()
    hand = enum.auto()
    offhand = enum.auto()
    neck = enum.auto()
    finger = enum.auto()
