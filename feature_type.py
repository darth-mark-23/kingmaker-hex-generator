from dataclasses import dataclass, field

from dice_roller import DiceRoller
from feature import Feature

class FeatureType:
    features: list = field(default_factory=list)
    default_feature_name: str = None
    variable: bool = False

    """Class to represent a feature type."""
    def __init__(self, name, dice_roller: DiceRoller):
        self.name = name
        self.dice_roller = dice_roller
        self.features = []

    def add_feature(self, feature: Feature):
        self.features.append(feature)

    def set_default_feature_name(self, feature_name: str):
        # Verify that the default feature name is valid
        if feature_name not in [feature.name for feature in self.features]:
            raise ValueError(f'Invalid default feature name: {feature_name}')
        
        self.default_feature_name = feature_name

    def set_variable(self, variable: bool):
        self.variable = variable
    
    def get_feature(self) -> Feature:
        """Returns the feature for this feature type based on the dice roll modifier."""

        # Get the dice roll modifier; if the feature type is variable, roll the dice; otherwise, use 0
        dice_roll_modifier = self.dice_roller.roll_dice() if self.variable else 0

        # Get the index of the default feature
        default_feature_index = self.features.index([feature for feature in self.features if feature.name == self.default_feature_name][0])

        # Calculate the index of the feature to use
        selected_feature_index = max(0, min((default_feature_index + dice_roll_modifier), len(self.features) - 1))
        
        # Get the feature to use
        selected_feature = self.features[selected_feature_index]
        
        return selected_feature