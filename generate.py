import csv
import openai
import os
import sys
import yaml

from dice_roller import DiceRoller
from feature_type import FeatureType
from feature import Feature
from bonus import Bonus

# Define bonus categories
bonus_categories = ['Farms', 'Fisheries', 'Logging', 'Mines']
cost_categories = ['Exploration Time', 'Clear', 'Road Cost']

# Initialize bonuses dictionary
bonuses = {category: 0 for category in bonus_categories}
costs = {category: 0 for category in cost_categories}



# Read the dice modifier values from the CSV file
with open('dice_table.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    dice_modifiers = [(int(row[0]), int(row[1])) for row in reader]

# Initialize dice roller
dice_roller = DiceRoller(dice_modifiers)



# Get YAML file name from the arguments; otherwise, use the default
yaml_file_name = sys.argv[1] if len(sys.argv) > 1 else 'hex_attributes_default.yaml'

# Open and load the YAML file
with open(yaml_file_name) as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

# For each feature type, create a FeatureType object
feature_types = {}
for feature_type_name, feature_type_data in data['Feature Types'].items():
    feature_types[feature_type_name] = FeatureType(feature_type_name, dice_roller)

    # For each feature, create a Feature object and add it to the FeatureType object
    for feature_name, feature_data in feature_type_data['Features'].items():
        feature = Feature(feature_name)

        # If bonus data is present, add it to the Feature object
        bonus_data = feature_data.get('Bonuses', {})
        if bonus_data is not None:
            for bonus_category, bonus_value in bonus_data.items():
                feature.addBonus(Bonus(bonus_category, bonus_value))

        # Add the Feature object to the FeatureType object
        feature_types[feature_type_name].add_feature(feature)
    
    # Add the default feature to the FeatureType object
    feature_types[feature_type_name].set_default_feature_name(feature_type_data['Default'])

    # If the feature type is variable, set the variable flag
    if feature_type_data.get('Variable', False):
        feature_types[feature_type_name].set_variable(True)
    
    # Add the FeatureType object to the feature_types dictionary
    feature_types[feature_type_name] = feature_types[feature_type_name]

selected_feature_names = {}
# For each Feature Type, get the rolled feature and add the bonuses to the bonuses dictionary, with a minimum of 0
for feature_type in feature_types.values():
    feature = feature_type.get_feature()
    selected_feature_names = {**selected_feature_names, **{feature_type.name: feature.name}}
    for bonus_category in bonus_categories:
        bonuses[bonus_category] += max(0, feature.get_bonus(bonus_category))
    for cost_category in cost_categories:
        costs[cost_category] += max(0, feature.get_bonus(cost_category))

# Create a single string with blank lines at the start and end
output_string = "\n\n"

# Add the selected feature names to the output string
for feature_type_name, feature_name in selected_feature_names.items():
    output_string += f'{feature_type_name}: {feature_name}\n'

# Add a blank line between the selected feature names and the bonuses dictionary output
output_string += "\n"

def get_descriptive_bonus_value(value):
    if value == 0:
        return "None"
    elif value == 1:
        return "Some"
    elif value == 2:
        return "Moderate"
    elif value == 3:
        return "Abundant"
    elif value == 4:
        return "Very Abundant"
    else:
        return "Extremely Abundant"
    
def get_descriptive_cost_value(value):
    if value == 0:
        return "None"
    elif value == 1:
        return "Small"
    elif value == 2:
        return "Moderate"
    elif value == 3:
        return "Expensive"
    elif value == 4:
        return "Very Abundant"
    else:
        return "Exorbitant"

# Add the bonuses dictionary to the output string
for bonus_category, bonus_value in bonuses.items():
    descriptive_value = get_descriptive_bonus_value(bonus_value)
    output_string += f'{bonus_category}: {bonus_value} ({descriptive_value})\n'

# Add a blank line between the bonuses dictionary and the costs dictionary output
output_string += "\n"

# Add the costs dictionary to the output string
for cost_category, cost_value in costs.items():
    descriptive_value = get_descriptive_cost_value(cost_value)
    output_string += f'{cost_category}: {cost_value} ({descriptive_value})\n'

# Check for magical features
magic_modifier = dice_roller.roll_dice()
magic_description = "No magical features."
if magic_modifier == -3:
    magic_description = "The region is cursed, or has some other magical effect that negatively impacts industry and habitation."
elif magic_modifier == -3:
    magic_description = "The region is blessed, or has some other magical effect that positively impacts industry and habitation and natural beauty."

# Add the magic description to the output string
output_string += f'\nMagic: {magic_description}\n'

# Add a blank line at the end of the output string
output_string += "\n"

# Print the output string
print(output_string)

# OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')

system_message = """
    You are a Game Master for a roleplaying game. You describe everything in-character, in order for players to immerse themselves in the descriptions and vivid imagery you provide.

    Setting: Middle Earth, Fourth Age
    Style: J.R.R Tolkien
    Length: 1 concise paragraph
    Notes: You sometimes use the languages of Middle Earth, such as Sindarin and Westron for place names. You value the integrity of the story and prose above rules details."""

instruction = """
    The following is a list of features and their bonuses for a geographical region on a map. This region exist within the forest of Mirkwood in the Fourth Age of Middle Earth, long after the events of the Lord of the Rings. It is a region of wilderness that is not yet settled and has little to no population. The bonuses represent the potential of the region, not the actual state of the region.
    
    This region will have various terrain features and associated bonuses which will impact industry, construction, and exploration in that region. A value of 0 means that industry cannot exist in the region. A value of 1 or 2 represents some potential, while 3 or higher represents a very abundant resource.

    Output: Please use the supplied features and bonuses to generate a name for the region and a 1-paragraph description of the description.
"""

prompt = f"{system_message}\n\n{instruction}"

messages = [
    {"role": "system", "content": prompt},
    {"role": "user", "content": output_string}
]

completion_parameters = {
    "messages": messages,
    "model": "gpt-3.5-turbo-0613",
    "max_tokens": 500,
    "temperature": 0.7,
}

# Get and print completion message
completion = openai.ChatCompletion.create(**completion_parameters)
completion_message = completion.choices[0].message.content
print(completion_message)
