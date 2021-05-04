def to_camel_case(snake_str):
    # We capitalize the first letter of each component with the 'title' method and join them 
    # together.
    components = snake_str.split('_')
    
    return ''.join(x.title() for x in components)
