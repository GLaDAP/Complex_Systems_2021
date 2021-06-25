"""
GROUP:       CSS_18
DATE:        25-6-2021
AUTHOR(S):   Sam Kuilboer, David Puroja, Jorrim Prins
DESCRIPTION: File containing functions to parallelize simulations.
"""

import json
import pandas as pd
from forest_fire.model import ForestFire
import multiprocessing

def calculate_model(config_tuple):
    """
    Worker function executing the simulation.

    :param config_tuple: tuple containing the parameters for the strategy to
                         use, maximum amount of steps, number of fire fighters,
                         extinguishing strength, CONFIG object with loaded
                         config from json file and the iteration id.
    """
    strategy, max_steps, n_fighters,ext_strength, CONFIG, i = config_tuple
    model = ForestFire(
        height = CONFIG['grid']['height'],
        width = CONFIG['grid']['width'],
        density_trees = CONFIG['model']['density_trees'],
        max_burn_rate = CONFIG['model']['max_burn_rate'],
        ignition_prob = CONFIG['model']['ignition_prob'],
        max_hp = CONFIG['agents']['tree']['max_hp'],
        max_iter = max_steps,
        regrowth_rate = CONFIG['model']['regrowth_rate'],
        N_firefighters = n_fighters,
        strategy = strategy,
        extg_strength = ext_strength
    )

    model_reporting_dicts = []

    while max_steps > 0:
        statistics = model.step()
        if statistics['On fire'] == 0:
            break
        model_reporting_dicts.append(statistics)
        max_steps -=1
    statistics_df = pd.DataFrame(model_reporting_dicts)
    statistics_df.to_csv(f'statistics_strat{strategy}_nfighters-{n_fighters}_ext_strength-{ext_strength}_{i}.csv')
    
    return 0

if __name__ == "__main__":
    """
    Load the config file with the base configuration
    """
    with open('forest_fire/config.json') as json_file:
        CONFIG = json.load(json_file)
        json_file.close()
    
    max_steps = 5000
    configuration_list = []
    """
    Create the computation configurations and add them to the list.
    """
    for i in range(5):
        # Random model without fire fighters
        configuration_list.append(('random', max_steps, 0, 0, CONFIG, i))

        # Setup models with fire fighters and different number of 
        # fighters/extinguishing strength
        for n_fighters in [100, 300, 500, 700, 900]:
            for ext_strength in [4,10]:
                configuration_list.append(
                    ('random', max_steps, n_fighters, ext_strength, CONFIG, i)
                )
                configuration_list.append(
                    ('closest', max_steps, n_fighters, ext_strength, CONFIG, i)
                )
                configuration_list.append(
                    ('biggest', max_steps, n_fighters, ext_strength, CONFIG, i)
                )
                configuration_list.append(
                    ('earliest', max_steps, n_fighters, ext_strength, CONFIG, i)
                )

        for ext_strength in [2, 4, 6, 8]:
            configuration_list.append(
                ('random', max_steps, 100, ext_strength, CONFIG, i)
            )
            configuration_list.append(
                ('closest', max_steps, 100, ext_strength, CONFIG, i)
            )
            configuration_list.append(
                ('biggest', max_steps, 100, ext_strength, CONFIG, i)
            )
            configuration_list.append(
                ('earliest', max_steps, 100, ext_strength, CONFIG, i)
            )

    # Start the computations in parallel.
    with multiprocessing.Pool() as pool:
        outputs = pool.map(calculate_model, configuration_list)
