"""

"""
import time
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

from forest_fire.model import ForestFire

if __name__ == "__main__":

    with open('forest_fire/config.json') as json_file:
        CONFIG = json.load(json_file)
        json_file.close()

    for strategy in ['no_fighter','random', 'closest', 'biggest', 'call_plane']:
        for n_fighters in [100, 300]:
            for i in range(10):
                start_time = time.time()
                print(f'{strategy}_{n_fighters}_{i}')
                max_steps = 5000
                model_reporting_dicts = []
                model = ForestFire(
                    height = 100,
                    width = 100,
                    density_trees = CONFIG['model']['density_trees'],
                    max_burn_rate = CONFIG['model']['max_burn_rate'],
                    ignition_prob = CONFIG['model']['ignition_prob'],
                    max_hp = CONFIG['agents']['tree']['max_hp'],
                    max_iter = max_steps,
                    regrowth_rate = CONFIG['model']['regrowth_rate'],
                    N_firefighters = n_fighters,
                    strategy = strategy,
                    extg_strength = CONFIG['agents']['fighter']['extg_strength']
                )

                while max_steps > 0:
                    statistics = model.step()
                    if statistics['On fire'] == 0:
                        print('Quitted due none percolating system')
                        break
                    model_reporting_dicts.append(statistics)
                    max_steps -=1
                print(f'Time for current param setting: {(time.time()-start_time)/60} minutes.')
                statistics_df = pd.DataFrame(model_reporting_dicts)
                statistics_df.to_csv(f'statistics_{strategy}_{n_fighters}fighters_{i}strength.csv')
