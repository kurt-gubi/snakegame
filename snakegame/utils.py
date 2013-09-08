try:
    from collections import OrderedDict as MaybeOrderedDict
except ImportError:
    MaybeOrderedDict = dict

def scale_aspect(source_size, target_size):
    source_width, source_height = source_size
    target_width, target_height = target_size
    source_aspect = float(source_width) / source_height
    target_aspect = float(target_width) / target_height
    if source_aspect > target_aspect:
        # restrict width
        width = target_width
        height = float(width) / source_aspect
    else:
        # restrict height
        height = target_height
        width = height * source_aspect
    return (width, height)

