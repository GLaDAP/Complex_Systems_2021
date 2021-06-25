"""
GROUP:       CSS_18
DATE:        17-06-2021
AUTHOR(S):   Sam Kuilboer, David Puroja, Jorrim Prins
DESCRIPTION: Script responsible for setting up the model and the agents. 
"""
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import ForestFire
from .tree import Tree
from .firefighter import FireFighter

from colour import Color
import json

# Open the config file to easily reuse certain configurations.
with open('forest_fire/config.json') as json_file:
    CONFIG = json.load(json_file)
    COLOUR_HP = [_.hex for _ in list(Color(CONFIG['model']['colors']['Burned']).range_to(Color(CONFIG['model']['colors']['On fire']), 101))]
    json_file.close()

def model_portrayal(agent):
    """
    Function for portraying the information of the model on a grid.

    :param agent: Agent which can be either a tree or a firefighter.
    """

    if isinstance(agent, Tree):
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        (x, y) = agent._get_pos()
        portrayal["x"] = x 
        portrayal["y"] = y

        if agent.condition == 'On fire':
            portrayal["Color"] = COLOUR_HP[agent.hp]
        else:    
            portrayal["Color"] = CONFIG['model']['colors'][agent.condition]
        return portrayal

    elif isinstance(agent, FireFighter):
        portrayal = {"Shape": 'circle', 'r': 0.9, 'Filled': 'true', 'Layer': 1}
        (x, y) = agent._get_pos()
        portrayal["x"] = x 
        portrayal["y"] = y
        portrayal["Color"] = CONFIG['model']['colors']['FireFighter']
        return portrayal

# The grid
canvas_element = CanvasGrid(model_portrayal, 
                            CONFIG['grid']['width'], 
                            CONFIG['grid']['height'], 
                            500, 500)

tree_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in CONFIG['agents']['tree']['colors'].items()]
)

# Parameters for the forest_fire model
model_parameters = {
    'width': CONFIG['grid']['width'],
    'height': CONFIG['grid']['height'],
    'density_trees': UserSettableParameter("slider", "Tree density", CONFIG['model']['density_trees'], 0.01, 1.0, 0.01),
    'max_burn_rate': UserSettableParameter("slider", "Max burnrate", CONFIG['model']['max_burn_rate'], 1, 100, 1),
    'ignition_prob': UserSettableParameter("slider", "Ingnition probability", CONFIG['model']['ignition_prob'], 0.01, 1.0, 0.01),
    'max_hp': UserSettableParameter("slider", "Max HP", CONFIG['agents']['tree']['max_hp'], 1, 100, 1),
    'max_iter': 1000,
    'regrowth_rate': UserSettableParameter('slider', 'Regrowth Rate', CONFIG['model']['regrowth_rate'], 5, 50, 5),
    'N_firefighters': UserSettableParameter('slider', 'N Firefighters', CONFIG['model']['N_firefighters'], 10, 1000, 10),
    'strategy': UserSettableParameter('choice', 'Strategy', CONFIG['agents']['fighter']['strategy'], choices=['no_fighter','random', 'closest', 'biggest','earliest']),
    'extg_strength': UserSettableParameter('slider', 'Extinguish strength', CONFIG['agents']['fighter']['extg_strength'], 10, 100,10)
}

# Start the server
server = ModularServer(ForestFire, [canvas_element, tree_chart], "Forest Fire", model_parameters)


