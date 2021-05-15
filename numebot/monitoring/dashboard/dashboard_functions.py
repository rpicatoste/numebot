from itertools import cycle

from numebot.monitoring.dashboard.dashboard_constants import PLOTLY_COLORS, PLOTLY_SHAPES, PLOTLY_SHAPES_N


def get_color_dict(list_of_items):
    colors_dict = {model_name: color 
                   for model_name, color 
                   in zip(list_of_items, cycle(PLOTLY_COLORS))}
    
    return colors_dict
    
    
def get_shape_dict(list_of_items):
    shape_dict = {round_number: PLOTLY_SHAPES[idx%PLOTLY_SHAPES_N] 
                  for idx, round_number in enumerate(list_of_items)}
    
    return shape_dict
