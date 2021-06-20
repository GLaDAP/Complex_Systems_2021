from mesa import Agent

class Tree(Agent):

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.condition = "Fine"
        self.hp = model.max_hp
        self.burn_rate = 0
        self.being_extinghuished = False

    def _ignite(self, start=False):

        if start == True:
            self.condition = "On fire"
        if self.model.random.random() < self.model.ignition_prob:
            self.condition = "On fire"
            self.burn_rate = self.random.choice(range(1, self.model.max_burn_rate))
    
    def _extinguish(self, firefighter):
        
        self.burn_rate -= firefighter.extg_strength
        if self.burn_rate <= 0:
            self.burn_rate = 0
            self.condition = 'Fine'

    def _get_pos(self):
        return self.pos
        
    def step(self):

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




            
