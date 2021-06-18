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
        burn_rate=10,
        initial_fire_size=5,
        ignition_threshold=5,
        new_trees_per_step=500,
        max_trees_hp=100
    ):
        """
        Create a new forest fire model.

        Args:
            height, width: The size of the grid to model
            density_trees:  What fraction of grid cells have a tree in them in
                            the initial phase
            growth_rate (int): The growth rate of a tree when it does not have
                            all the health_points
            burn_rate (int): The rate a tree burns once it is set on fire.
                             This increases at each time step
            new_trees_per_step (int): The amount of trees to plant at each time
                                      step.
            ignition_threshold (int): The threshold before a fire spreads to
                                      another tree.
            max_trees_hp (int): The maximum amount of health a tree can have.
        """
        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(height, width, torus=False)
        # Width parameter used to set a boundary value for random generation
        # of coordinates
        self.width = width
        # Rates used by Tree
        self.growth_rate = growth_rate
        self.burn_rate = burn_rate
        self.new_trees_per_step = new_trees_per_step

        self.initial_fire_size = initial_fire_size
        # Threshold when a fire spreads to another tree
        self.ignition_threshold = ignition_threshold
        # Maximum health points a tree can have
        self.max_trees_hp = max_trees_hp

        self.datacollector = DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
            }
        )

        # Place a tree in each cell with Prob = density
        # print(self.grid.x)
        for (_, x, y) in self.grid.coord_iter():
            if self.random.random() < density_trees:
                # Create a tree
                initial_hp = np.random.randint(10, self.max_trees_hp)
                new_tree = Tree((x, y), self, initial_hp)
                # Set all trees in the first column on fire.
                # if self.random.random() < 0.001:
                #     new_tree.condition = "On Fire"
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)
        self.initialize_fire_area()
        self.running = True
        self.datacollector.collect(self)

    def initialize_fire_area(self):
        """
        Initialize fire area in the model after creation of the forest.
        """
        # 1. Select random point on the grid where a tree is present
        coordinates = np.random.randint(
            0,
            self.width,
            (100, 2)
        )
        cells = self.grid.get_cell_list_contents(coordinates)
        # Take the first one from the list
        previous_trees = []
        tree_object = cells.pop()
        # Get the radius as long as not 
        total_fires = 0
        while tree_object is not None and total_fires < self.initial_fire_size:
            previous_trees.append(tree_object)
            print(f"Set tree on fires {total_fires}")
            agents_in_radius = self.grid.get_neighbors(
                tree_object.pos,
                moore=True, # Only direct neighbours, no diagonals
                include_center=False,
                radius=1
            )
            print(tree_object.pos)
            tree_object.set_on_fire()
            total_fires += 1
            if agents_in_radius:
                while tree_object in previous_trees and agents_in_radius:
                    tree_object = np.random.choice(agents_in_radius)
                    agents_in_radius.remove(tree_object)
                    print("Tree in list")
            else:
                print("No agents in radius")
                tree_object = None

    def plant_new_trees(self):
        """
        Plant each timestep new trees (or at least attempt)
        """
        coordinates = np.random.randint(
            0,
            self.width,
            (self.new_trees_per_step, 2)
        )
        # Loop over the coordinates. This is required since getting all the
        # coordinates at once gives a whole list pack of all agents, with the
        # nones skipped.
        for coordinate in coordinates:
            this_cell = self.grid.get_cell_list_contents([coordinate])
            if not this_cell:
                x, y = coordinate
                # Cell is empty, add a tree
                initial_hp = np.random.randint(10, self.max_trees_hp)
                new_tree = Tree((x, y), self, initial_hp)
                # Set all trees in the first column on fire.
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        # With a given probability, plant new trees at random locations:
        self.plant_new_trees()
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
