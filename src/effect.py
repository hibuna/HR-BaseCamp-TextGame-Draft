class Effect:
    """
    An effect that can be applied to the player.

    Attributes:
    -----------
    name : str
        The name of the effect.
    description : str
        The description of the effect.
    """

    name: str
    description: str

    def __repr__(self):
        return f"<{str(self)}>"

    def __str__(self):
        return f"{self.name.upper()}"


class VacuumResistance(Effect):
    name = "vacuum resistance"
    description = "You can enter the void."


class FullBladder(Effect):
    name = "full bladder"
    description = "You need to pee."
