"""
GROUP:       CSS_18
DATE:        17-06-2021
AUTHOR(S):   Sam Kuilboer
DESCRIPTION: Walker class, with functions to move agents in a certain manner:
                - random
                - radius
                - organized << is not yet implemented
"""

from .tree import Tree
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

    def __init__(self, unique_id, pos, model, moore=True):
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
        move = self.random.choice(self.__check_possible_moves())
        self.model.grid.move_agent(self, move)

    def move_towards_closest_fire(self, radius=5):
        """
        The agent moves to the closest fire. If none is spotted it 
        moves to a random spot.

        Attributes:
            radius: int=5
        """

        neighbours = self.model.grid.get_neighbors(
            pos = self.pos,
            moore = True,
            include_center = False,
            radius = radius
        )
        neighbouring_trees = [agent for agent in neighbours if isinstance(agent, Tree)]
        burning_trees = [tree for tree in neighbouring_trees if tree.condition == 'On fire']
        if len(burning_trees) > 0:
            ordered_trees = self.__get_closest_tree(burning_trees)
            self.model.grid.move_agent(self, ordered_trees[1].pos)
        else:
            self.random_move()

    def move_towards_biggest_fire(self, radius=5):
        """
        The agent moves to the biggest fire based on burn rte. If none is spotted it
        moves to a random spot.

        Attributes:
            radius: int=5
        """

        neighbours = self.model.grid.get_neighbors(
            pos = self.pos,
            moore = True,
            include_center = False,
            radius = radius
        )
        neighbouring_trees = [agent for agent in neighbours if isinstance(agent, Tree)]
        burning_trees = [tree for tree in neighbouring_trees if tree.condition == 'On fire']
        if len(burning_trees) > 0:
            max_index = self.__get_most_burning_tree(burning_trees)
            self.model.grid.move_agent(self, burning_trees[max_index].pos)
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


    def __get_most_burning_tree(self, trees):
        """
        Select the most burning tree

        Attributes:
            trees: list of agents to detect which is most burning
        Returns:
            List of objects sorted by burn rate
        """
        burn_rates = [tree.burn_rate for tree in trees]
        return burn_rates.index(max(burn_rates))
        # heap = []
        # [
        #     heapq.heappush(
        #         heap,
        #         (
        #             (
        #                 tree.burn_rate
        #             ),
        #             tree
        #         )
        #     ) for tree in trees
        # ]
        # return heapq.heappop(heap)

    def __check_possible_moves(self):

        coords = self.model.grid.get_neighborhood(
            pos = self.pos,
            moore = self.moore,
            include_center = True
        )
        possible_moves = []
        for coord in coords:
            tree = [agent for agent in self.model.grid.get_cell_list_contents(coord) if isinstance(agent, Tree)]
            if len(tree) == 0:
                possible_moves.append(coord)
            elif tree[0].condition != 'On fire':
                possible_moves.append(coord)

        return possible_moves



