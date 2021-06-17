from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation

import numpy as np

from .tree import Tree

class ForestFire(Model):
    """
    Simple Forest Fire model.
    """

    def __init__(
        self,
        height=128,
        width=128,
        density_trees=0.65,
        growth_rate=10,
        burn_speed=10
    ):
        """
        Create a new forest fire model.

        Args:
            height, width: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(height, width, torus=False)
        self.growth_rate = growth_rate
        self.burn_speed = burn_speed
        self.datacollector = DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
            }
        )

        # Place a tree in each cell with Prob = density
        # print(self.grid.x)
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density_trees:
                # Create a tree
                initial_hp = np.random.randint(10,100)
                new_tree = Tree((x, y), self, initial_hp)
                # Set all trees in the first column on fire.
                if self.random.random() < 0.001:
                    new_tree.condition = "On Fire"
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count
