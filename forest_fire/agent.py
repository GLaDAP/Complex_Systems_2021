from mesa import Agent
import random


class Tree(Agent):
    """
    A tree cell.

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "On Fire", or "Burned Out"
        unique_id: (x,y) tuple.

    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    """

    def __init__(self, pos, model):
        """
        Create a new tree.
        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.name = "Tree"
        self.pos = pos
        self.condition = "Fine"

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """
        if self.condition == "On Fire":
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                if neighbor.condition == "Fine":
                    neighbor.condition = "On Fire"
            self.condition = "Burned Out"

class FireFighter(Agent):
    """
    A FireFighter agent.

    Attributes:
        x, y: Grid coordinates
        condition: Can be 'inactive', 'active'
        unique_id: (x,y) tuple
    """

    def __init__(self, pos, model):
        """
        Create a firefighter tree.
        Args:
            pos: The firefighter's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.name = "FireFighter"
        self.pos = pos

    def step(self):
        """
        If the firefighter is inactive it looks in a range of 3 for a fire.
        """
        neighbors = self.random.shuffle(self.model.grid.neightbor_iter(self.pos))
        exth = False
        for neighbor in neighbors:
            if neighbor.name == 'Tree':
                if neighbor.condition == 'On Fire':
                    neighbor.condition = 'Fine'
                    exth = True
                    break
        if exth == False:
            self.move()

    def move(self):
        """
        If the FireFighter does not extinguish a fire it is able to move to a next spot.
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False
        )

        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

            

        


