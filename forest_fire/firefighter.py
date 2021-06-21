"""
GROUP:       CSS_18
DATE:        17-06-2021
AUTHOR(S):   Sam Kuilboer
DESCRIPTION: FireFighter class with functions to extinguish fires. 
             This class inherits the walker class.
"""
from .tree import Tree
from .walker import Walker

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

    def __init__(self, unique_id, pos, model, extg_strength):
        super().__init__(unique_id, pos, model)
        self.extg_strength = extg_strength
        self.fires_extg = 0

    def _get_pos(self):
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
        else:
            self.random_move()

