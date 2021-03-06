"""
GROUP:       CSS_18
DATE:        17-06-2021
AUTHOR(S):   Sam Kuilboer, David Puroja
DESCRIPTION: Tree class, based on the agent class of the MESA Framework.
             The class consists of multiple methods repsonsible for either
             igniting trees or extinghuishing them. 
             The step method proceeds the agent one step in the model.
"""
from mesa import Agent

class Tree(Agent):

    def __init__(self, unique_id, pos, model):
        """
        Class which represents a tree agent

        :param unique_id: Unique id for every agent, model.next_id().
        :param pos: Position of the tree on the grid
        :param model: The forest_fire model
        """

        super().__init__(unique_id, model)
        self.pos = pos
        self.condition = "Fine"
        self.hp = model.max_hp
        self.burn_rate = 0
        self.being_extinghuished = False

    def _ignite(self, start=False):
        """
        Method for igniting a tree

        :param start: When starting no probability is applied.
        """

        if start == True:
            self.condition = "On fire"
        if self.model.random.random() < self.model.ignition_prob:
            self.condition = "On fire"
            self.burn_rate = self.random.choice(range(1, self.model.max_burn_rate))
    
    def _extinguish(self, firefighter):
        """
        Method for extinghuising a tree

        :param firefighter: The firefighter which is currently extinghuising 
                            the tree.
        """
        if firefighter.strategy != 'call_plane':
            self.burn_rate -= firefighter.extg_strength
        else:
            self.burn_rate -= firefighter.extg_strength*5
        if self.burn_rate <= 0:
            self.burn_rate = 0
            self.condition = 'Fine'
    
    def _killed(self):
        """
        Remove burned trees from the grid.
        """
        self.model.grid._remove_agent(self.pos, self)
        self.model.schedule_Tree.remove(self)
        self.model.trees.remove(self)

    def _get_pos(self):
        """
        Method which returns the position
        """
        return self.pos
        
    def step(self):
        """
        Method for proceeding one step in the model. 
        """

        # If burned, remove from the grid
        if self.condition == "Burned":
            self._killed()

        # if on fire
        if self.condition == "On fire":

            # 1. ignite neighbors
            trees = [agent for agent in self.model.grid.get_neighbors(self.pos, 
                                                                      moore=False, 
                                                                      radius=1) if isinstance(agent, Tree)]
            for tree in trees:
                if tree.condition == 'Fine':
                    tree._ignite()

            # 2. drop hp
            if self.hp > 0:
                self.hp = self.hp - self.burn_rate
                if self.hp <= 0:
                    self.hp = 0
                    self.condition = "Burned"
            else:
                self.condition = "Burned"




            
