from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from .tree import Tree
from .firefighter import FireFighter

class ForestFire(Model):

    def __init__(self, height, width, density_trees, max_burn_rate, ignition_prob, max_hp):
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

        self.grid = MultiGrid(height, width, torus=False)
        self.trees = []
        self.firefighters = []

        self.schedule_Tree = RandomActivation(self)
        self.schedule_FireFighter = RandomActivation(self)

        self.density_trees = density_trees
        self.max_burn_rate = max_burn_rate
        self.ignition_prob = ignition_prob
        self.max_hp = max_hp

        self.datacollector = DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On fire"),
                "Burned": lambda m: self.count_type(m, "Burned")
            }
        )
        self._init_trees()
        self._init_fire()
        self._init_firefighter()

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
        print(tree.unique_id, tree.pos)
        tree._ignite(start=True)

    def _init_firefighter(self, N=100):
        """
        Init firefighters on the grid. Randomly or on a line.
        """
        for _ in range(N):
            # x, y = self.random.randint(0, self.height - 1), self.random.randint(0, self.width -1)
            x, y = 3, self.random.randint(0, self.width -1)
            firefighter = FireFighter(self.next_id(), (x, y), self, extg_strength=20)
            self.grid._place_agent((x,y), firefighter)
            self.firefighters.append(firefighter)
            self.schedule_FireFighter.add(firefighter)

    def step(self):
        """
        Method to move one step forward. 
        """

        self.schedule_Tree.step()
        self.schedule_FireFighter.step()

        self.datacollector.collect(self)
        
        if self.count_type(self, 'On fire') == 0:
            self.running = False

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


