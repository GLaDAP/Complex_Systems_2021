"""

"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

from forest_fire.model import ForestFire

if __name__ == "__main__":

    with open('forest_fire/config.json') as json_file:
        CONFIG = json.load(json_file)
        json_file.close()

    for strategy in ['no_fighters','random', 'closest', 'biggest', 'call_plane']:
        max_steps = 11000
        model_reporting_dicts = []
        model = ForestFire(
            height = 128,
            width = 128,
            density_trees = CONFIG['model']['density_trees'],
            max_burn_rate = CONFIG['model']['max_burn_rate'],
            ignition_prob = CONFIG['model']['ignition_prob'],
            max_hp = CONFIG['agents']['tree']['max_hp'],
            max_iter = max_steps,
            regrowth_rate = CONFIG['model']['regrowth_rate'],
            N_firefighters = CONFIG['model']['N_firefighters'],
            strategy = CONFIG['agents']['fighter']['strategy']
        )

        while max_steps > 0:
            statistics = model.step()
            model_reporting_dicts.append(statistics)
            max_steps -=1
        
        statistics_df = pd.DataFrame(model_reporting_dicts)
        statistics_df.to_csv('statistics_{strategy}.csv')
