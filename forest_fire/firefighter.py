"""
GROUP:       CSS_18
DATE:        17-06-2021
AUTHOR(S):   Sam Kuilboer, David Puroja, Jorrim Prins
DESCRIPTION: Firefighter class, based on the walker class and used its functions
             to move over the grid. This class consists of extinghuish functions
             and step method to proceed a step during an iteration.
"""
from .Walker import Walker
from .tree import Tree

class FireFighter(Walker):
    """
    FireFighter class able of extinguishing fires.

    Attributes:
        unique_id: int
        pos: tuple(x, y)
        model: grid
        moore: boolean
        extg_strength: int within range [0, 100]
    """

    def __init__(self, unique_id, pos, model, extg_strength,strategy):
        super().__init__(unique_id, pos, model)
        self.extg_strength = extg_strength
        self.fires_extg = 0
        self.strategy = strategy

    def _get_pos(self):
        """
        Gets the coordinate of the agent.
        """
        return self.pos

    def step(self):
        """
        If the firefighter is near a fire it will try to extinguish it,
        if not, it will move randomly.
        """
        neighbors = self.model.grid.get_neighbors(
            pos = self.pos,
            moore = False,
            include_center = False,
            radius = 1
        )
        neighbouring_trees = [agent for agent in neighbors if isinstance(agent, Tree)]
        burning_trees = [tree for tree in neighbouring_trees if tree.condition == 'On fire']

        if len(burning_trees) > 0:
            burning_tree = self.random.choice(burning_trees)
            burning_tree._extinguish(firefighter=self)
            self.fires_extg += 1
        elif self.strategy == 'closest':
            self.move_towards_closest_fire()
        elif self.strategy == 'biggest':
            self.move_towards_biggest_fire()
        elif self.strategy == 'earliest':
            self.move_towards_hp_fire()
        else:
            self.random_move()
