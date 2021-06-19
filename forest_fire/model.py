from forest_fire.firefighter import FireFighter
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
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
        max_trees_hp=100,
        initial_firefighters=1,
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
        super().__init__()
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(height, width, torus=False)
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
                new_tree = Tree(self.next_id(), (x, y), self, initial_hp)
                # Set some random trees on fire
                if self.random.random() < 0.001:
                    new_tree.condition = "On Fire"
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)
        
        # Place N firefighters on the grid
        for _ in range(initial_firefighters):
            coord = (self.random.randint(0, width-1),
                     self.random.randint(0, height-1))
            new_firefigher = FireFighter(self.next_id(), coord, self, self.random.randint(50,100))
            self.grid._place_agent(coord, new_firefigher)
            self.schedule.add(new_firefigher) 
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
                new_tree = Tree(
                    unique_id=self.next_id(),
                    pos=(x, y), 
                    model=self, 
                    initial_hp=initial_hp)
                # Set all trees in the first column on fire.
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)

    def ignite_random_tree(self, chance=0.0001):
        """
        Ignites a random tree during a step
        """
        coordinates = np.random.randint(
            0,
            self.width,
            (self.new_trees_per_step, 2)
        )
        trees = self.grid.get_neighbors(
            pos = self.random.choice(coordinates),
            moore = False,
            include_center = True,
            radius = 1
        )
        trees = [tree for tree in trees if isinstance(tree, Tree)]
        if self.random.random() < chance:
            for tree in trees:
                tree.set_on_fire()

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
        trees = [agent for agent in model.schedule.agents if isinstance(agent, Tree)]
        for tree in trees:
            if tree.condition == tree_condition:
                count += 1
        return count
