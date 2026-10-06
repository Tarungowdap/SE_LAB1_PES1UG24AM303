"""
catch: hook-vs-fish catch detection.
"""


def check_catch(hook, fish_list):
    """
    Returns the first fish whose rectangle overlaps the hook's rectangle,
    or None. Both horizontal and vertical position are taken into account.
    """
    hook_rect = hook.get_rect()
    for fish in fish_list:
        if hook_rect.colliderect(fish.get_rect()):
            return fish
    return None
