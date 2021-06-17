from mesa import Agent

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