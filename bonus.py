from dataclasses import dataclass

@dataclass(frozen=True)
class Bonus:
    """Class to represent a bonus."""
    bonusType: str
    value: int
