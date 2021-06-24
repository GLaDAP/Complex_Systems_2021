"""

"""
import json
import pandas as pd
from forest_fire.model import ForestFire
import multiprocessing

def calculate_model(config_tuple):
    strategy, max_steps, n_fighters,ext_strength, CONFIG, i = config_tuple
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
        extg_strength = ext_strength #CONFIG['model']['extg_strength']
    )
    model_reporting_dicts = []
    while max_steps > 0:
        statistics = model.step()
        if statistics['On fire'] == 0:
            break
        model_reporting_dicts.append(statistics)
        max_steps -=1
    statistics_df = pd.DataFrame(model_reporting_dicts)
    statistics_df.to_csv(f'data/new_data/statistics_{strategy}_nfighters_{n_fighters}_ext_strength_{ext_strength}_{i}.csv')

    return 0

if __name__ == "__main__":
    with open('forest_fire/config.json') as json_file:
        CONFIG = json.load(json_file)
        json_file.close()
    max_steps = 5000

    configuration_list = []
    # 30 simulations
    for n_fighters in [100, 300, 500, 700, 900]:
        for ext_strength in [10]:
            for i in range(10):
                configuration_list.append(('random', max_steps, n_fighters, ext_strength, CONFIG, i))
                configuration_list.append(('closest', max_steps, n_fighters, ext_strength, CONFIG, i))
                configuration_list.append(('biggest', max_steps, n_fighters, ext_strength, CONFIG, i))

    # 12 simulations
    for ext_strength in [2, 4, 6, 8]:
        for i in range(10):
            configuration_list.append(('random', max_steps, 100, ext_strength, CONFIG, i))
            configuration_list.append(('closest', max_steps, 100, ext_strength, CONFIG, i))
            configuration_list.append(('biggest', max_steps, 100, ext_strength, CONFIG, i))

    with multiprocessing.Pool() as pool:
        outputs = pool.map(calculate_model, configuration_list)
