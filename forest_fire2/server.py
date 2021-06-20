from forest_fire2.firefighter import FireFighter
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import ForestFire
from .tree import Tree

from colour import Color
import json

with open('forest_fire2/config.json') as json_file:
    CONFIG = json.load(json_file)
    COLOUR_HP = [_.hex for _ in list(Color(CONFIG['model']['colors']['Burned']).range_to(Color(CONFIG['model']['colors']['On fire']), 101))]
    json_file.close()

def model_portrayal(agent):

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

canvas_element = CanvasGrid(model_portrayal, 
                            CONFIG['grid']['width'], 
                            CONFIG['grid']['height'], 
                            500, 500)

model_parameters = {
    'width': CONFIG['grid']['width'],
    'height': CONFIG['grid']['height'],
    'density_trees': CONFIG['model']['density_trees'],
    'max_burn_rate': CONFIG['model']['max_burn_rate'],
    'ignition_prob': CONFIG['model']['ignition_prob'],
    'max_hp': CONFIG['agents']['tree']['max_hp']
}

server = ModularServer(ForestFire, [canvas_element], "Forest Fire", model_parameters)


