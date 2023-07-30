import random

class DiceRoller:
    """Class to roll dice and return the modifier value based on the dice roll."""
    def __init__(self, dice_modifiers):
        self.dice_modifiers = dice_modifiers

    def roll_dice(self):
        """Rolls three dice and returns the modifier value based on the dice roll."""
        dice_rolls = [random.randint(1, 6) for _ in range(3)]
        dice_total = sum(dice_rolls)
        for dice_modifier in self.dice_modifiers:
            if dice_total <= dice_modifier[0]:
                return dice_modifier[1]
        return 0
    