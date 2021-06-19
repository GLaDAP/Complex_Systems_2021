from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import ForestFire
from .new_tree import Tree

from colour import Color
import json

with open('forest_fire2/config.json') as json_file:
    CONFIG = json.load(json_file)
    json_file.close()

def model_portrayal(agent):

    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = agent._get_pos()
    portrayal["x"] = x 
    portrayal["y"] = y
    colour_range = [_.hex for _ in list(Color(CONFIG['model']['colors']['Burned']).range_to(Color(CONFIG['model']['colors']['On fire']), 101))]

    if isinstance(agent, Tree):
        if agent.condition == 'On fire':
            portrayal["Color"] = colour_range[agent.hp]
        else:    
            portrayal["Color"] = CONFIG['model']['colors'][agent.condition]
    return portrayal

print(CONFIG)
canvas_element = CanvasGrid(model_portrayal, 
                            CONFIG['grid']['width'], 
                            CONFIG['grid']['height'], 
                            500, 500)

model_parameters = {
    'width': CONFIG['grid']['width'],
    'height': CONFIG['grid']['height'],
    'density_trees': CONFIG['model']['density_trees'],
    'burn_rate': CONFIG['model']['burn_rate'],
    'ignition_prob': CONFIG['model']['ignition_prob'],
    'max_hp': CONFIG['agents']['tree']['max_hp']
}

server = ModularServer(ForestFire, [canvas_element], "Forest Fire", model_parameters)


