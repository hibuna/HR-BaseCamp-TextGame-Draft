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


class WaterBreathing(Effect):
    name = "Water Breathing"
    description = "You can breathe underwater."
