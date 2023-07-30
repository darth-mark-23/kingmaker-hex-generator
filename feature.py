from dataclasses import dataclass, field

@dataclass()
class Feature():
    """Class to represent a feature."""
    name: str
    bonuses: list = field(default_factory=list)

    def addBonus(self, bonus):
        self.bonuses.append(bonus)

    def get_bonus(self, key):
        for bonus in self.bonuses:
            if bonus.bonusType == key:
                return bonus.value
        return 0