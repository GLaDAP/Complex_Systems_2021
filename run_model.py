import json
import pandas as pd

from forest_fire.model import ForestFire
"""
File to start the model without using the server.

"""

if __name__ == "__main__":
    """
    1. Initialize the object using the config file.
    """
    max_steps = 1000

    model_reporting_dicts = []

    with open('forest_fire/config.json') as json_file:
        CONFIG = json.load(json_file)
        json_file.close()

    model = ForestFire(
        height = CONFIG['grid']['height'],
        width = CONFIG['grid']['width'],
        density_trees = CONFIG['model']['density_trees'],
        max_burn_rate = CONFIG['model']['max_burn_rate'
        ],
        ignition_prob = CONFIG['model']['ignition_prob'],
        max_hp = CONFIG['agents']['tree']['max_hp'],
        max_iter = max_steps,
        regrowth_rate = CONFIG['model']['regrowth_rate'],
        N_firefighters = CONFIG['model']['N_firefighters'],
        strategy = CONFIG['agents']['fighter']['strategy'],
        extg_strength = CONFIG['agents']['fighter']['extg_strength']#, choices=['no_fighters','random', 'closest', 'biggest', 'call_plane'])
    )

    while max_steps > 0:
        # 
        statistics = model.step()
        model_reporting_dicts.append(statistics)
        max_steps -=1
    statistics_df = pd.DataFrame(model_reporting_dicts)
    statistics_df.to_csv('statistics.csv')