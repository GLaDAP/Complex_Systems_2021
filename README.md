# **Forest-fire behavior under varying firefighting strategies** 

Repository of Group 18 for the course Complex System Simulation (5284COSS6Y), June 2021.

## Summary

This model is used to analyze dynamics of a forest fire under varying firefighting strategies. The forest is initialized with static Tree agents and dynamic Firefighter agents, both initialized randomly over the grid: the trees with a predefined density (0.9 at default settings) and the firefighters with a given amount (default is 100). Fire is started by setting 1 tree in state "On fire", from which it spreads through the lattice using Von-Neumann neighborhood. When a Tree is burned down, it is removed from the system. Each time step new trees are grown on random free spots in the lattice. The firefighters try to extinguish the fire with a strategy defined before running the model. The strategies are: 

- **Closest fire:** Agent moves to the closest fire in a given radius
- **Biggest fire:** Firefighter moves to the biggest fire; tree which is on fire and has the highest burn rate 
- **Earliest**: Move to the tree with the most HP left
- **Random**: Fire fighters will extinguish randomly the fires by extinguishing a fire when they encounter one.

When there are no firefighters deployed (number of firefighters is equal to 0) or the random or closest strategy is used , the fire in the system will percolate.

### Entities Variables

The model consists of two different types of entities: individual agents and spatial units. Each entity contain state variables or attributes creating the functionality in the model.

- **Individual Agents:** Two agent types are present in the forest fire model: a Tree agent and a Firefighter agent. The Tree agent is a static and is explained under *spatial units*.  Firefighter agents move through the grid with a fixed radius (default 5), using the Von Neumann neighborhood. The firefighter will move to a fire in the radius (when one is present) depending on the strategy used. It then extinguish the fire at a certain rate per timestep and moves to the next fire depending on the strategy.
- **Spatial Units:** The model uses a multi-grid space system provided by the Mesa framework. The spatial unit are the trees, which are static agents on the lattice. The trees can be 'Fine', 'On fire' or 'Burned', with the latter resulting in removal of the tree from the grid. Trees regrow with a fixed rate each timestep and are regrown with full HP. Firefighters have direct impact on this spatial unit since they interact with burning trees.

### Process Overview

At each timestep, first the tree agents are activated in random order to update the burn rate of the tree, if the tree is on fire. When the tree is on fire, at each time step the tree burns with a fixed burn rate. When a tree has zero HP left, the tree is removed from the grid. If a tree on fire is extinguished, no HP is regenerated. After all the trees are updated, the firefighters are randomly activated. Depending on the strategy used, the firefighter will move towards a fire and try to extinguish it with a predefined extinguish rate.

On each time step, new trees are added to the system on empty random grid cells in the system.

### Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```

The dependencies are as follows:

- Mesa: to run the actual model
- pandas: to save the results from runs in a csv
- matplotlib: to plot the results
- jupyter: to use the visualization functions found in the notebook.

- scipy: `scipy.ndimage` is used in the model for cluster size detection

## How to Run

To run the model interactively, run ``python run.py`` in this directory. e.g.

```
    $ python run.py
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run. 

To view visualizations used in the presentation, use the ``Figures.ipynb`` Notebook using ``jupyter notebook``.

## Files

- `forest_fire/data/*`: contains two folders with csv-output from previous simulations for different configurations
- `forest_fire/figures/*`: contains images used in the presentation and analysis of the model
- `forest_fire/config.json`: contains default parameter settings used to run the model
- `forest_fire/firefighter.py`: Defines the Firefighter agent
- `forest_fire/model.py`: Defines the ForestFire model
- `forest_fire/server.py`: contains definitions to start the interactive mesa visualization server
- `forest_fire/tree.py`: Defines the Tree agent
- `forest_fire/Walker.py`: contains definitions used by `firefighter.py` for walking using different strategies
- `run_model.py`: Helper file to run the model multiple times in parallel with different configurations and store statistics
- `run.py`: Launches a model visualization server provided by Mesa

## Further Reading

Read about the Forest Fire model on Wikipedia: http://en.wikipedia.org/wiki/Forest-fire_model

This example is based on the existing Mesa example for simulating a forest fire, found here: [ForestFire model](https://github.com/projectmesa/mesa/tree/main/examples/forest_fire)

most of the code is however rewritten, with only using small part of the code from Mesa.

## References

- Dorrer, G. A., & Yarovoy, S. V. (2020, April). Description of wildfires spreading and extinguishing with the aid of agent-based models. In *IOP Conference Series: Materials Science and Engineering* (Vol. 822, No. 1, p. 012010). IOP Publishing.
- Hu, X., & Sun, Y. (2007, December). Agent-based modeling and simulation of wildland fire suppression. In *2007 Winter Simulation Conference* (pp. 1275-1283). IEEE.
- Malamud, B. D., & Turcotte, D. L. (1999). Self-organized criticality applied to natural hazards. *Natural Hazards*, *20*(2), 93-116.

- Kazil, J., Masad, D., & Crooks, A. (2021). *projectmesa/mesa*. Utilizing Python for Agent-Based Modeling: The Mesa Framework. https://github.com/projectmesa/mesa/tree/main/examples/forest_fire.
