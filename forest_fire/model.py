import time
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from numpy.core import numeric

from .tree import Tree
from .firefighter import FireFighter

import numpy as np
from scipy import ndimage


class ForestFire(Model):

    def __init__(self, height, width, density_trees, max_burn_rate, ignition_prob,
                 max_hp, max_iter, regrowth_rate, N_firefighters,strategy, extg_strength):
        """
        Create a forest fire ABM model.

        :param height: Height of the grid.
        :param width: Width of the the grid.
        :parm density_trees: The density of trees on the grid.
        :param max_burn_rate: The maximum speed on which a tree burns.
        :param ignition_prob: The probability that a tree ignites when a neighbour is on fire.
        :param max_hp: The maximum hp of a tree.
        """
        super().__init__()

        self.height = height
        self.width = width
        self.current_step = 0

        self.grid = MultiGrid(height, width, torus=False)
        self.trees = []
        self.firefighters = []

        self.schedule_Tree = RandomActivation(self)
        self.schedule_FireFighter = RandomActivation(self)

        self.density_trees = density_trees
        self.max_burn_rate = max_burn_rate
        self.ignition_prob = ignition_prob
        self.max_hp = max_hp
        self.regrowth_rate = regrowth_rate
        self.N_firefighters = N_firefighters
        self.strategy = strategy
        self.extg_strength = extg_strength

        self.max_iter = max_iter

        self.datacollector = DataCollector(
            {
                "Density Trees": lambda m: len(m.trees)/(self.width * self.height),
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On fire": lambda m: self.count_type(m, "On fire"),
                "Burned": lambda m: self.count_type(m, "Burned"),
                # # Using the model reporter is very inefficient. Maybe implement this in the step function
                # # and keep it separate ?
                # "Nf": len(self.get_fire_areas()),
                # "Ns": self.current_step,
                # "percentage_on_fire": lambda m: self.count_type(m, "On fire")/(self.width * self.height),
                # "total_area": self.width * self.height,
                # "min_fire_area": lambda m: np.min(self.get_fire_areas()),
                # "max_fire_area": lambda m: np.max(self.get_fire_areas()),
                # "median_fire_area": lambda m: np.median(self.get_fire_areas()),
                # "mean_fire_area": lambda m: np.mean(self.get_fire_areas())
            }
        )
        self._init_trees()
        self._init_fire()
        if self.strategy != "no_fighters":
            self._init_firefighters()

        self.running = True

    def _init_trees(self):
        """
        Init trees on every coordinate under a certain probability. 
        """
        for (_, x, y) in self.grid.coord_iter():
            if self.random.random() < self.density_trees:

                new_tree = Tree(self.next_id(), (x, y), self)
                self.grid._place_agent((x,y), new_tree)
                self.trees.append(new_tree)
                self.schedule_Tree.add(new_tree)
        print('Done planting trees')

    def _init_fire(self):
        """
        Init a fire on a random spot on the field.
        """
        tree = self.random.choice(self.trees)
        tree._ignite(start=True)

    def _init_firefighters(self):
        """
        Init firefighters on the grid. Randomly or on a line.
        """
        for _ in range(self.N_firefighters):
            # x, y = self.random.randint(0, self.height - 1), self.random.randint(0, self.width -1)
            x, y = self.random.randint(0, self.height-1), self.random.randint(0, self.width -1)
            firefighter = FireFighter(self.next_id(), (x, y), self, extg_strength=self.extg_strength, strategy=self.strategy)
            self.grid._place_agent((x,y), firefighter)
            self.firefighters.append(firefighter)
            self.schedule_FireFighter.add(firefighter)

    def plant_new_trees(self, regrowth_rate):
        """
        At every time step, plant an random amount of new trees.
        """
        for _ in range(regrowth_rate):
            # if self.grid.exists_empty_cells == True:
            random_coord = self.grid.find_empty()
            if random_coord is not None:
                new_tree = Tree(self.next_id(),
                                random_coord,
                                self)
                self.grid._place_agent(random_coord, new_tree)
                self.trees.append(new_tree)
                self.schedule_Tree.add(new_tree)

    def step(self):
        """
        Method to move one step forward. 
        """
        self.current_step += 1
        if (self.current_step % 1000 == 0):
                print(self.current_step)
        self.schedule_Tree.step()
        if self.strategy != "no_fighters":
            self.schedule_FireFighter.step()

        self.plant_new_trees(self.regrowth_rate)

        self.datacollector.collect(self)
        
        if (self.current_step > self.max_iter) or self.count_type(self, 'On fire') == 0:
            # df = self.datacollector.get_model_vars_dataframe()
            # datestring = time.ctime()[4:7]+'-'+time.ctime()[8:10]+'-'+time.ctime()[11:16]
            # df.to_csv('{}-report-{}.csv'.format(datestring,self.strategy)) ### This gives an error, can u check?
            self.running = False

        return self.get_statistics()

    def get_fire_areas(self):
        """
        Calculates the fire areas.
        """
        # Convert to numeric representation:
        numeric_grid = self.get_numeric_representation_of_grid()
        labels, _ = ndimage.label(numeric_grid)
        surface_areas = np.bincount(labels.flat)[1:]
        return surface_areas

    def get_numeric_representation_of_grid(self):
        numeric_grid = np.zeros((self.width, self.height), dtype=np.int8)
        trees = [agent for agent in self.schedule_Tree.agents if isinstance(agent, Tree)]
        for tree in trees:
            if (tree.condition == "On fire"):
                numeric_grid[tree.pos] = 1
        return numeric_grid

    def get_statistics(self):
        """
        Get burned area
        Parameters to collect:
        - AF: Number of trees burned in each fire
        - Nf are the number of fires
        - Ns the time steps
        """
        trees_on_fire = self.count_type(self, "On fire")
        total_area = self.width * self.height
        percentage_on_fire = trees_on_fire / total_area
        n_s = self.current_step
        fire_areas = self.get_fire_areas()
        return {
            "Nf": len(fire_areas),
            "Ns": n_s,
            "percentage_on_fire": percentage_on_fire,
            "trees_on_fire": trees_on_fire,
            "total_area": total_area,
            "min_fire_area": np.min(fire_areas) if len(fire_areas) > 0 else 0,
            "max_fire_area": np.max(fire_areas) if len(fire_areas) > 0 else 0,
            "median_fire_area": np.median(fire_areas) if len(fire_areas) > 0 else 0,
            "mean_fire_area": np.mean(fire_areas) if len(fire_areas) > 0 else 0,
            "Density Trees": len(self.trees)/(self.width * self.height),
            "Fine": self.count_type(self, "Fine"),
            "On fire": trees_on_fire,
        }

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        trees = [agent for agent in model.schedule_Tree.agents if isinstance(agent, Tree)]
        for tree in trees:
            if tree.condition == tree_condition:
                count += 1
        return count


