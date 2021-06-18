"""
GROUP:       CSS_18
DATE:        17-06-2021
AUTHOR(S):   Sam Kuilboer
DESCRIPTION: Walker class, with functions to move agents in a certain manner:
                - random
                - radius
                - organized << is not yet implemented
"""

from forest_fire.tree import Tree
from mesa import Agent
import heapq

class Walker(Agent):
    """
    A class for an agent which is able to walk.

    Attributes:
        unique_id: int
        pos: tuple(x, y)
        model: grid
    
    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    """

    def __init__(self, unique_id, pos, model, moore=False):
        """
        Initialize Walker class
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    def random_move(self):
        """
        Method for randomly moving the agent over the grid
        """
        possible_moves = self.model.grid.get_neigborhood(
            pos = self.pos,
            moore = self.moore,
            include_center = False
        )
        move = self.random.choice(possible_moves)
        self.model.grid.move_agent(self, move)

    def move_towards_closest_fire(self, radius=3):
        """
        The agent moves to the closest fire. If none is spotted it 
        moves to a random spot.

        Attributes:
            radius: int=3
        """

        neighbours = self.model.grid.get_neighbors(
            pos = self.pos,
            moore = True,
            include_center = False,
            radius = radius
        )
        neighbouring_trees = [agent for agent in neighbours if isinstance(agent, Tree)]
        burning_trees = [tree for tree in neighbouring_trees if tree.condition == 'On fire']
        if burning_trees > 0:
            ordered_trees = self.__get_closest_tree(burning_trees)
            self.model.grid.move_agent(self, ordered_trees[1].pos)
        else:
            self.random_move()

    def __get_closest_tree(self, trees):
        """
        Select the closest tree

        Attributes:
            trees: list of agents to detect which is closest
        Returns:
            Ordered list of closest objects
        """
        heap = []
        [
            heapq.heappush(
                heap,
                (
                    (
                        abs(self.pos[0] - tree.pos[0]),
                        abs(self.pos[1] - tree.pos[1])
                    ), 
                    tree
                )
            ) for tree in trees
        ]
        return heapq.heappop(heap)


