import forest_fire
from forest_fire.firefighter import FireFighter
from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import ForestFire

from forest_fire.tree import Tree
from forest_fire.Walker import Walker

COLORS = {"Fine": "#00AA00", 
          "On Fire": "#880000", 
          "Burned Out": "#000000",
          "FireFighter": "blue"}


def forest_fire_portrayal(agent):

    # if empty
    if agent is None:
        return
    elif isinstance(agent, Tree):
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        (x, y) = agent.pos
        portrayal["x"] = x
        portrayal["y"] = y
        portrayal["Color"] = COLORS[agent.condition]
        return portrayal
    elif isinstance(agent, FireFighter):
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        (x, y) = agent.pos
        portrayal["x"] = x
        portrayal["y"] = y
        portrayal["Color"] = COLORS["FireFighter"]
        return portrayal


canvas_element = CanvasGrid(forest_fire_portrayal, 128, 128)
tree_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)
pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

model_params = {
    "height": 128,
    "width": 128,
    "density_trees": UserSettableParameter("slider", "Tree density", 0.65, 0.01, 1.0, 0.01),
    "growth_rate": UserSettableParameter("slider", "Growth rate", 10, 0, 25, 5),
    "burn_rate": UserSettableParameter("slider", "Burn rate", 10, 0, 50, 5),
    "ignition_threshold": UserSettableParameter("slider", "Ignition threshold", 5, 0, 50, 5),
    "new_trees_per_step": UserSettableParameter("slider", "New trees per step", 100, 0, 1000, 25),
    "initial_fire_size": UserSettableParameter("slider", "Initial Fire size", 5, 1, 50, 1)
}
server = ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire", model_params
)
