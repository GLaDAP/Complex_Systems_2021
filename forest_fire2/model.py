from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from .new_tree import Tree

class ForestFire(Model):

    def __init__(self, height, width, density_trees, burn_rate, ignition_prob, max_hp):
        super().__init__()

        self.height = height
        self.width = width

        self.grid = MultiGrid(height, width, torus=False)
        self.trees = []

        self.schedule_Tree = RandomActivation(self)
        self.schedule_FireFighter = RandomActivation(self)

        self.density_trees = density_trees
        self.burn_rate = burn_rate
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


        self.running = True

    def _init_trees(self):

        for (_, x, y) in self.grid.coord_iter():
            if self.random.random() < self.density_trees:

                new_tree = Tree(self.next_id(), (x, y), self)
                self.grid._place_agent((x,y), new_tree)
                self.trees.append(new_tree)
                self.schedule_Tree.add(new_tree)

    def _init_fire(self):
        tree = self.random.choice(self.trees)
        print(tree.unique_id, tree.pos)
        tree._ignite(start=True)

    def step(self):

        self.schedule_Tree.step()
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


