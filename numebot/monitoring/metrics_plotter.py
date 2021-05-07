from itertools import cycle
import matplotlib.pyplot as plt
import pandas as pd

from numebot.data.data_constants import NC
from numebot.utils import listify


def get_color_dict(list_of_items):
    model_colors_list = ['r', 'g', 'b', 'yellow', 'gray', 'm', 'c']
    colors_dict = {model_name: color 
                   for model_name, color 
                   in zip(list_of_items, cycle(model_colors_list))}
    
    return colors_dict


def round_line_style(round_number):
    line_style_loop = ['-', '--', '-.', ':']
    return line_style_loop[round_number%len(line_style_loop)]


def round_marker(round_number):
    markers_loop = ['o', 'x', 's', '*']
    return markers_loop[round_number%len(markers_loop)]


def plot_round_details(round_details_df: pd.DataFrame, model_names=(), rounds=(), ax=None):
    model_names = listify(model_names)
    rounds = listify(rounds)

    if ax is None:
        plt.figure(figsize=(15,5))
        ax = plt.subplot(1, 1, 1)
    
    all_model_names = list(round_details_df[NC.model_name].unique())
    colors_dict = get_color_dict(all_model_names)

    for model_name, model_df in round_details_df.groupby(NC.model_name):
        if len(model_names) > 0 and model_name not in model_names:
            continue
            
        for round_number, round_df in model_df.groupby(NC.round):
            if len(rounds) > 0 and round_number not in rounds:
                continue
                
            plt.plot(round_df[NC.date], round_df[NC.correlation], 
                    label=f'{model_name} - r{round_number}',
                    color=colors_dict[model_name],
                    linestyle=round_line_style(round_number),
                    marker=round_marker(round_number))

    ax.axhline(0.0, color='k', linewidth=1)
    ax.set_ylabel('Correlation')
    plt.legend()
    
    return ax
